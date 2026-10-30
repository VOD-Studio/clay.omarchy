#!/usr/bin/env python3
"""Exercise installed Omarchy templates in a disposable, headless home.

The complete working tree, including its real .git directory, is copied so
Omarchy applies the restrictions used for installed repository themes. The
light variant is linked from that copy's light/ directory, matching the
documented `ln -s` installation.
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


REPOSITORY = "clay.omarchy"
THEMES = {"dark": REPOSITORY, "light": "clay-light"}


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


def preview(source, output, variant):
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
        themes = home / ".config/omarchy/themes"
        shutil.copytree(source, themes / REPOSITORY, symlinks=True)
        (themes / THEMES["light"]).symlink_to(themes / REPOSITORY / "light")
        theme_name = THEMES[variant]
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
        result = subprocess.run([str(command), theme_name], cwd=home, env=env,
                                capture_output=True, text=True)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        if result.returncode:
            raise RuntimeError(f"omarchy-theme-set exited with status {result.returncode}")
        print(f"PASS {variant}: installed headless theme pipeline for {theme_name} (isolated HOME and runtime)")

        current = home / ".local/state/omarchy/current"
        theme = current / "theme"
        mode = tomllib.loads((theme / "colors.toml").read_text()).get("mode")
        require(mode == variant, f"Staged colors.toml has mode {mode!r}, expected {variant!r}")
        lua_files = []
        for template in templates:
            generated = theme / template.name.removesuffix(".tpl")
            require(generated.is_file(), f"Missing generated template output: {generated.name}")
            text = generated.read_text()
            require("{{" not in text, f"Unresolved template token in {generated.name}")
            if generated.suffix == ".toml":
                tomllib.loads(text)
            elif generated.suffix == ".json":
                json.loads(text)
            elif generated.suffix == ".lua":
                lua_files.append(generated)
        print(f"PASS {variant}: {len(templates)} installed template outputs; tokens and TOML/JSON syntax")

        compiler = shutil.which("luac", path=env["PATH"])
        if compiler:
            for path in lua_files:
                result = subprocess.run([compiler, "-p", str(path)], cwd=home,
                                        env=env, capture_output=True, text=True)
                require(result.returncode == 0,
                        f"Lua syntax error in {path.name}: {result.stderr.strip()}")
            print(f"PASS {variant}: Lua syntax ({len(lua_files)} files, luac -p)")
        else:
            print("SKIP Lua syntax: luac is not installed")

        background = current / "background"
        require(background.is_symlink(), "Pipeline did not select a background")
        check_png(background.resolve(strict=True))
        print(f"PASS {variant}: selected background resolves to a valid PNG header")
        count = sum(path.is_file() for path in theme.rglob("*"))
        if output is not None:
            # copytree refuses existing destinations, including a concurrent
            # creation after argument validation. Dereference the background.
            shutil.copytree(current, output, symlinks=False)
            print(f"PASS {variant}: {count} theme files; exported current/ to {output}")
        else:
            print(f"PASS {variant}: {count} theme files; temporary preview removed on exit (no export)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=("dark", "light", "both"), default="both",
                        help="theme to stage (default: both)")
    parser.add_argument("--output", type=Path, metavar="DIRECTORY",
                        help="export current/ to a new directory outside the project")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    output = args.output.absolute().resolve() if args.output is not None else None
    variants = ("dark", "light") if args.variant == "both" else (args.variant,)
    try:
        if output is not None:
            require(len(variants) == 1, "--output needs a single --variant")
            require(not output.is_relative_to(source), "Output must be outside the source tree")
            require(not os.path.lexists(args.output.absolute()), "Output path already exists")
        for variant in variants:
            preview(source, output, variant)
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
