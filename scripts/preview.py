#!/usr/bin/env python3
"""Exercise installed Omarchy templates in a disposable, headless home.

The complete working tree, including its real .git directory, is copied so
Omarchy applies the restrictions used for installed repository themes.
--output exports current/ with background links dereferenced, so the exported
configs and chosen image remain usable after the temporary home is removed.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import tomllib
import zlib


THEME = "clay.omarchy"
CLAY = "#d97757"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_png(path):
    require(path.is_file(), f"Chosen background does not resolve to a file: {path}")
    with path.open("rb") as stream:
        header = stream.read(33)
    require(len(header) == 33 and header[:8] == b"\x89PNG\r\n\x1a\n",
            "Chosen background has no valid PNG signature")
    length, kind, width, height, depth, color, compression, filtering, interlace, crc = (
        struct.unpack(">I4sIIBBBBBI", header[8:])
    )
    depths = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8),
              4: (8, 16), 6: (8, 16)}
    require(length == 13 and kind == b"IHDR" and width > 0 and height > 0
            and depth in depths.get(color, ()) and compression == filtering == 0
            and interlace in (0, 1) and zlib.crc32(header[12:29]) == crc,
            "Chosen background has an invalid PNG IHDR header")


def preview(source, output):
    omarchy = Path(os.environ.get("OMARCHY_PATH", "/usr/share/omarchy")).resolve()
    command = Path("/usr/bin/omarchy-theme-set")
    require(command.is_file(), f"Installed theme command not found: {command}")
    templates = sorted((omarchy / "default/themed").glob("*.tpl"))
    require(templates, f"No installed templates found under {omarchy}/default/themed")
    require((source / ".git").is_dir() and not (source / ".git").is_symlink(),
            "Initialize this project's .git directory before running preview")

    # An explicit /tmp base prevents an inherited TMPDIR inside the repository
    # from causing a recursive copy of the sandbox into itself.
    with tempfile.TemporaryDirectory(prefix="clay-omarchy-", dir="/tmp") as temporary:
        sandbox = Path(temporary)
        home = sandbox / "home"
        runtime = sandbox / "runtime"
        runtime.mkdir(mode=0o700)
        installed = home / ".config/omarchy/themes" / THEME
        shutil.copytree(source, installed, symlinks=True)
        env = {
            "PATH": "/usr/bin:/bin",
            "HOME": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_STATE_HOME": str(home / ".local/state"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "XDG_DATA_HOME": str(home / ".local/share"),
            "XDG_RUNTIME_DIR": str(runtime),
            "TMPDIR": str(sandbox),
            "OMARCHY_PATH": str(omarchy),
            "OMARCHY_THEME_HEADLESS": "1",
            "LC_ALL": "C.UTF-8",
        }
        result = subprocess.run([str(command), THEME], cwd=home, env=env,
                                capture_output=True, text=True)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        if result.returncode:
            raise RuntimeError(f"omarchy-theme-set exited with status {result.returncode}")
        print("PASS installed headless theme pipeline (isolated HOME and runtime)")

        current = home / ".local/state/omarchy/current"
        theme = current / "theme"
        parsed = {}
        lua_files = []
        for template in templates:
            generated = theme / template.name.removesuffix(".tpl")
            require(generated.is_file(), f"Missing generated template output: {generated.name}")
            text = generated.read_text()
            require("{{" not in text, f"Unresolved template token in {generated.name}")
            if generated.suffix == ".toml":
                parsed[generated.name] = tomllib.loads(text)
            elif generated.suffix == ".json":
                parsed[generated.name] = json.loads(text)
            elif generated.suffix == ".lua":
                lua_files.append(generated)
        print(f"PASS {len(templates)} installed template outputs; tokens and TOML/JSON syntax")

        shell = parsed["shell.toml"]
        for key in ("focus-color", "focus-border", "selected-color"):
            require(shell["controls"][key] == CLAY,
                    f"Generated shell controls.{key} must be {CLAY}")
        print("PASS generated shell keyboard-focus and selection overrides")

        compiler = shutil.which("luac", path=env["PATH"])
        if compiler:
            for path in lua_files:
                result = subprocess.run([compiler, "-p", str(path)], cwd=home,
                                        env=env, capture_output=True, text=True)
                require(result.returncode == 0,
                        f"Lua syntax error in {path.name}: {result.stderr.strip()}")
            print(f"PASS Lua syntax ({len(lua_files)} files, luac -p)")
        else:
            print("SKIP Lua syntax: luac is not installed")

        background = current / "background"
        require(background.is_symlink(), "Pipeline did not select a background")
        check_png(background.resolve(strict=True))
        print("PASS selected background resolves to a valid PNG header")
        count = sum(path.is_file() for path in theme.rglob("*"))
        if output is not None:
            # copytree refuses existing destinations, including a concurrent
            # creation after argument validation. Dereference the background.
            shutil.copytree(current, output, symlinks=False)
            print(f"PASS {count} theme files; exported current/ to {output}")
        else:
            print(f"PASS {count} theme files; temporary preview removed on exit (no export)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, metavar="DIRECTORY",
                        help="export current/ to a new directory outside the project")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    output = args.output.absolute().resolve() if args.output is not None else None
    try:
        if output is not None:
            require(not output.is_relative_to(source), "Output must be outside the source tree")
            require(not os.path.lexists(args.output.absolute()), "Output path already exists")
        preview(source, output)
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
