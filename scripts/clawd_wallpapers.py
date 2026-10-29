"""Render the Clawd wallpaper series: TYPE-17-style framed panels in the Clay palette.

Unofficial fan art of Anthropic's Clawd mascot, redrawn as a 16x8 pixel sprite.
Writes 3840x2160 PNGs 02-06 to backgrounds/ by default.
Needs rsvg-convert plus the JetBrainsMono Nerd Font and Noto Sans CJK JP fonts.
"""
import argparse, random, subprocess, tempfile
from pathlib import Path

W, H = 3840, 2160
BG = "#111315"
CLAY = "#d97757"
CLAY_HI = "#e8977b"
CLAY_MID = "#b86347"
CLAY_DK = "#7c3f2d"
LINE = "#cccccc"
MUTED = "#7a7a7a"
SUBTLE = "#2a2a2a"
FONT = "JetBrainsMono Nerd Font"

# Frame geometry follows TYPE-17: a centred panel ~53% x 46% of the canvas.
FX, FY, FW, FH = 906, 576, 2028, 1004

# Clawd sprite on a 16x8 grid: body, side arms, four legs, two eye holes.
BODY = {(x, y) for x in range(2, 14) for y in range(0, 6)}
EYES = {(4, 1), (4, 2), (11, 1), (11, 2)}
ARMS = {(0, 3), (1, 3), (14, 3), (15, 3)}
LEGS = {(x, y) for x in (3, 5, 10, 12) for y in (6, 7)}
SPRITE = (BODY - EYES) | ARMS | LEGS


def svg(title, body, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>{title}</title>
  <defs>
    <clipPath id="frame"><rect x="{FX}" y="{FY}" width="{FW}" height="{FH}"/></clipPath>
{defs}
  </defs>
  <rect width="{W}" height="{H}" fill="{BG}"/>
{body}
</svg>
'''


def frame(left, mid, right, stroke=LINE):
    x2, y2 = FX + FW, FY + FH
    ty = y2 + 46
    cap = f'font-family="{FONT}" font-size="25" letter-spacing="3" fill="{stroke}"'
    return f'''  <rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="none" stroke="{stroke}" stroke-width="2.5"/>
  <path d="M {FX-14},{FY-6} h 16 M {FX-6},{FY-14} v 16" stroke="{stroke}" stroke-width="2.5"/>
  <path d="M {x2-2},{y2+6} h 10 v -10" fill="none" stroke="{stroke}" stroke-width="2"/>
  <text x="{FX}" y="{ty}" {cap}>{left}</text>
  <text x="{FX+FW/2}" y="{ty}" text-anchor="middle" {cap}>{mid}</text>
  <text x="{x2}" y="{ty}" text-anchor="end" {cap}>{right}</text>
'''


def cells(cs, ox, oy, s, fill, extra=""):
    return "\n".join(
        f'<rect x="{ox+x*s}" y="{oy+y*s}" width="{s}" height="{s}" fill="{fill}" {extra}/>'
        for x, y in sorted(cs))


def outline(cs, ox, oy, s):
    """Union outline: emit each cell side that borders an empty cell."""
    segs = []
    for x, y in cs:
        X, Y = ox + x * s, oy + y * s
        if (x, y - 1) not in cs: segs.append(f"M{X},{Y}h{s}")
        if (x, y + 1) not in cs: segs.append(f"M{X},{Y+s}h{s}")
        if (x - 1, y) not in cs: segs.append(f"M{X},{Y}v{s}")
        if (x + 1, y) not in cs: segs.append(f"M{X+s},{Y}v{s}")
    return " ".join(segs)


# ---------------------------------------------------------------- 01 UNIT
def unit():
    """Giant mecha-panel Clawd, tilted and cropped by the frame like TYPE-17's hull."""
    s = 140
    ox, oy = FX + FW / 2 - 8 * s + 260, FY + FH / 2 - 4 * s + 40
    rect = lambda x, y, w, h, f, e="": f'<rect x="{ox+x*s}" y="{oy+y*s}" width="{w*s}" height="{h*s}" fill="{f}" {e}/>'
    P = lambda x, y: (ox + x * s, oy + y * s)
    parts = [
        rect(2, 0, 12, 6, CLAY),
        rect(0, 3, 2, 1, CLAY_MID), rect(14, 3, 2, 1, CLAY_MID),
        *(rect(x, 6, 1, 2, CLAY_MID) for x in (3, 5, 10, 12)),
        rect(4, 1, 1, 2, BG), rect(11, 1, 1, 2, BG),
    ]
    # Panel seams, rivets, vents and stencils give the flat sprite a machined surface.
    x0, y0 = P(2, 0)
    det = []
    det.append(f'<path d="M {x0},{y0+3.2*s} H {x0+12*s} M {x0+6.5*s},{y0} V {y0+3.2*s} M {x0+8.6*s},{y0+3.2*s} V {y0+6*s}" stroke="{CLAY_DK}" stroke-width="5" fill="none"/>')
    det.append(f'<path d="M {x0},{y0+0.35*s} H {x0+12*s}" stroke="{CLAY_HI}" stroke-width="10" opacity="0.7"/>')
    for i in range(9):
        cx = x0 + 0.5 * s + i * 1.375 * s
        det.append(f'<circle cx="{cx}" cy="{y0+3.45*s}" r="9" fill="{CLAY_DK}"/>')
    vx, vy = x0 + 9.1 * s, y0 + 4.0 * s
    for r in range(4):
        for c in range(7):
            det.append(f'<rect x="{vx+c*40}" y="{vy+r*30}" width="26" height="14" fill="{CLAY_DK}"/>')
    det.append(f'<text x="{x0+0.6*s}" y="{y0+5.45*s}" font-family="Noto Sans CJK JP" font-weight="500" font-size="190" fill="{CLAY_DK}" opacity="0.85">爪-01</text>')
    det.append(f'<text x="{x0+5.0*s}" y="{y0+1.0*s}" font-family="{FONT}" font-size="44" letter-spacing="6" fill="{CLAY_DK}">CLWD / MK.I</text>')
    det.append(f'<g fill="{CLAY_DK}">' + "".join(
        f'<path d="M {x0+5.2*s+i*70},{y0+2.7*s} l 40,0 l -25,-60 l -40,0 z"/>' for i in range(5)) + '</g>')
    # A broad diagonal shadow band, like a lit mecha hull.
    shade = f'<path d="M {x0+4.5*s},{y0-400} L {x0+7.8*s},{y0-400} L {x0+3.2*s},{y0+1800} L {x0-0.1*s},{y0+1800} Z" fill="#000" opacity="0.22"/>'
    body = "\n".join(parts + det + [shade])
    g = f'''  <g clip-path="url(#frame)">
    <g transform="rotate(-11 {FX+FW/2} {FY+FH/2})">
{body}
    </g>
  </g>
'''
    return svg("Clawd Unit", g + frame("CLAY-01", "CLAWD · UNIT 01", "CLAY.OMARCHY"))


# ----------------------------------------------------------- 02 SCHEMATIC
def schematic():
    s = 86
    sw, sh = 16 * s, 8 * s
    ox, oy = FX + (FW - sw) / 2 - 40, FY + (FH - sh) / 2 + 10
    grid = "".join(f'<path d="M {FX+i*48},{FY} V {FY+FH}"/>' for i in range(1, FW // 48 + 1))
    grid += "".join(f'<path d="M {FX},{FY+i*48} H {FX+FW}"/>' for i in range(1, FH // 48 + 1))
    hatch = "".join(f'<path d="M {ox+i*28},{oy} l -{sh},{sh}"/>' for i in range(0, int((sw + sh) / 28)))
    cellgrid = "\n".join(
        f'<rect x="{ox+x*s}" y="{oy+y*s}" width="{s}" height="{s}"/>' for x, y in sorted(SPRITE))
    D = LINE
    dim = f'''
    <g stroke="{MUTED}" stroke-width="2" fill="none">
      <path d="M {ox},{oy-70} H {ox+sw} M {ox},{oy-88} v 36 M {ox+sw},{oy-88} v 36"/>
      <path d="M {ox+sw+80},{oy} V {oy+sh} M {ox+sw+62},{oy} h 36 M {ox+sw+62},{oy+sh} h 36"/>
      <path d="M {ox+2*s},{oy-20} v -30 M {ox+14*s},{oy-20} v -30" stroke-dasharray="6 6"/>
    </g>
    <g font-family="{FONT}" font-size="26" letter-spacing="2" fill="{MUTED}">
      <text x="{ox+sw/2}" y="{oy-86}" text-anchor="middle">16 u</text>
      <text x="{ox+sw+104}" y="{oy+sh/2+9}">08 u</text>
    </g>'''
    def callout(px, py, tx, ty, label, anchor="start"):
        return (f'<circle cx="{px}" cy="{py}" r="7" fill="{CLAY}"/>'
                f'<path d="M {px},{py} L {tx},{ty} h {40 if anchor=="start" else -40}" stroke="{D}" stroke-width="1.6" fill="none"/>'
                f'<text x="{tx+(50 if anchor=="start" else -50)}" y="{ty+9}" text-anchor="{anchor}" font-family="{FONT}" font-size="26" letter-spacing="3" fill="{D}">{label}</text>')
    calls = "".join([
        callout(ox + 4.5 * s, oy + 2 * s, FX + 420, FY + 170, "A · OPTIC ×2", "end"),
        callout(ox + 0.5 * s, oy + 3.5 * s, FX + 420, FY + 800, "B · MANIPULATOR", "end"),
        callout(ox + 10.5 * s, oy + 7.5 * s, ox + 12.6 * s, FY + FH - 90, "C · LOCOMOTION ×4"),
        callout(ox + 8 * s, oy + 0.5 * s, ox + 11 * s, FY + 120, "D · HULL 12×6"),
    ])
    spec = f'''<g font-family="{FONT}" font-size="22" letter-spacing="3" fill="{MUTED}">
      <text x="{FX+FW-40}" y="{FY+FH-100}" text-anchor="end">SCALE 1:1 PX</text>
      <text x="{FX+FW-40}" y="{FY+FH-64}" text-anchor="end">COLOR #D97757</text>
      <text x="{FX+40}" y="{FY+60}">DWG NO. CL-002</text>
    </g>'''
    body = f'''  <g clip-path="url(#frame)">
    <g stroke="{SUBTLE}" stroke-width="1" opacity="0.7">{grid}</g>
    <clipPath id="sprite">{cellgrid}</clipPath>
    <g clip-path="url(#sprite)" stroke="{CLAY}" stroke-width="2" opacity="0.35">{hatch}</g>
    <g fill="none" stroke="#444444" stroke-width="1.5">{cellgrid}</g>
    <path d="{outline(SPRITE, ox, oy, s)}" stroke="{D}" stroke-width="4" fill="none" stroke-linecap="square"/>
{dim}
    {calls}
    {spec}
  </g>
'''
    return svg("Clawd Schematic", body + frame("CLAY-02", "CLAWD · GENERAL ARRANGEMENT", "CLAY.OMARCHY"))


# ------------------------------------------------------------- 03 HORIZON
def horizon():
    # Re-uses the theme's Clay Horizon ridge, scaled into the frame; Clawd stands on the summit.
    k = 0.62
    tx = FX + FW / 2 - 2010 * k
    ty = FY + FH - 2160 * k + 120
    ridge = f'''
      <path d="M 830,2290 C 1080,2030 1185,1640 1465,1320 C 1650,1108 1820,990 2010,990 C 2250,990 2410,1155 2570,1370 C 2800,1680 2970,2040 3300,2290 Z" fill="#1a1c1e"/>
      <path d="M 830,2290 C 1080,2030 1185,1640 1465,1320 C 1650,1108 1820,990 2010,990 C 2250,990 2410,1155 2570,1370 C 2800,1680 2970,2040 3300,2290" fill="none" stroke="#555" stroke-width="3"/>
      <g fill="none" stroke="#2f2f2f" stroke-width="3">
        <path d="M 1030,2290 C 1230,2050 1345,1720 1570,1440 C 1730,1240 1865,1130 2020,1130 C 2220,1130 2360,1295 2505,1490 C 2700,1755 2850,2070 3120,2290"/>
        <path d="M 1220,2290 C 1390,2070 1485,1795 1670,1560 C 1800,1395 1910,1270 2030,1270 C 2195,1270 2320,1435 2450,1610 C 2610,1825 2735,2100 2940,2290"/>
        <path d="M 1410,2290 C 1545,2100 1635,1870 1775,1680 C 1880,1540 1950,1410 2040,1410 C 2170,1410 2280,1575 2390,1730 C 2520,1915 2625,2130 2760,2290"/>
      </g>
      <path d="M -400,1835 C 525,1792 1005,1873 1490,1918 C 2055,1970 2590,1926 3070,1865 C 3360,1828 3615,1818 4300,1846 L 4300,2400 L -400,2400 Z" fill="{BG}"/>
      <path d="M -400,1835 C 525,1792 1005,1873 1490,1918 C 2055,1970 2590,1926 3070,1865 C 3360,1828 3615,1818 4300,1846" fill="none" stroke="#333" stroke-width="2.5"/>'''
    s = 9
    peak_x, peak_y = tx + 2010 * k, ty + 990 * k
    cx, cy = peak_x - 8 * s, peak_y - 8 * s + 1
    random.seed(17)  # Fixed star field keeps rebuilt PNGs identical.
    stars = "".join(
        f'<circle cx="{FX+random.random()*FW:.0f}" cy="{FY+random.random()*FH*0.55:.0f}" r="{random.choice([1.5,2,2.5])}" fill="#7a7a7a" opacity="{random.choice([0.35,0.5,0.7])}"/>'
        for _ in range(70))
    moon = f'<circle cx="{FX+FW*0.78}" cy="{FY+210}" r="64" fill="none" stroke="{CLAY}" stroke-width="3" opacity="0.8"/>'
    glow = f'<ellipse cx="{peak_x}" cy="{peak_y}" rx="260" ry="70" fill="url(#glow)"/>'
    body = f'''  <g clip-path="url(#frame)">
    {stars}
    {moon}
    <g transform="translate({tx} {ty}) scale({k})">{ridge}
    </g>
    {glow}
    {cells(SPRITE, cx, cy, s, CLAY)}
  </g>
'''
    defs = f'''    <radialGradient id="glow"><stop offset="0" stop-color="{CLAY}" stop-opacity="0.22"/><stop offset="1" stop-color="{CLAY}" stop-opacity="0"/></radialGradient>'''
    return svg("Clawd Horizon", body + frame("CLAY-03", "CLAWD · SUMMIT", "CLAY.OMARCHY"), defs)


# ------------------------------------------------------------ 04 TERMINAL
def terminal():
    # The CLI mark decoded from its quadrant block glyphs into an 18x6 pixel grid.
    rows = [" ▐▛███▜▌", "▝▜█████▛▘", "  ▘▘ ▝▝"]
    quad = {"█": "1111", "▐": "0101", "▌": "1010", "▛": "1110", "▜": "1101",
            "▝": "0100", "▘": "1000", " ": "0000"}  # TL TR BL BR
    px = set()
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            q = quad[ch]
            for i, bit in enumerate(q):
                if bit == "1":
                    px.add((c * 2 + i % 2, r * 2 + i // 2))
    s = 48
    ox = FX + 170
    oy = FY + (FH - 6 * s) / 2 - 30
    mono = f'font-family="{FONT}" letter-spacing="1"'
    tx = ox + 18 * s + 140
    lines = [
        (CLAY, 64, "✻ Clawd"),
        (MUTED, 28, "/help for help · /status for your setup"),
        (MUTED, 28, "cwd: ~/clay.omarchy"),
    ]
    txt = ""
    y = oy + 90
    for fill, size, t in lines:
        txt += f'<text x="{tx}" y="{y}" {mono} font-size="{size}" fill="{fill}">{t}</text>'
        y += size + 40
    prompt_y = FY + FH - 170
    prompt = (f'<path d="M {FX+80},{prompt_y-70} H {FX+FW-80} M {FX+80},{prompt_y+50} H {FX+FW-80}" stroke="#444" stroke-width="2"/>'
              f'<text x="{FX+110}" y="{prompt_y+12}" {mono} font-size="36" fill="{LINE}">&gt;</text>'
              f'<rect x="{FX+160}" y="{prompt_y-22}" width="22" height="42" fill="{LINE}"/>'
              f'<text x="{FX+FW-110}" y="{prompt_y+100}" text-anchor="end" {mono} font-size="24" fill="{MUTED}">? for shortcuts</text>')
    scan = "".join(f'<path d="M {FX},{FY+i*6} H {FX+FW}"/>' for i in range(0, FH // 6))
    body = f'''  <g clip-path="url(#frame)">
    {cells(px, ox, oy, s, CLAY)}
    {txt}
    {prompt}
    <g stroke="#000" stroke-width="2" opacity="0.1">{scan}</g>
  </g>
'''
    return svg("Clawd Terminal", body + frame("CLAY-04", "CLAWD · TTY", "CLAY.OMARCHY"))


# --------------------------------------------------------------- 05 MARCH
def march():
    s = 11
    sw, sh = 16 * s, 8 * s
    gx, gy = 236, 150
    cols = FW // gx + 2
    nrows = FH // gy + 2
    out = []
    for r in range(nrows):
        off = (gx / 2) if r % 2 else 0
        for c in range(cols):
            x = FX + 40 + c * gx + off - gx / 2
            y = FY + 34 + r * gy
            hi = (r, c) == (3, 5)
            fill = CLAY if hi else ("#2c2e30" if (r + c) % 3 else "#3a3a3a")
            out.append(cells(SPRITE, x, y, s, fill))
    body = f'''  <g clip-path="url(#frame)">
{chr(10).join(out)}
  </g>
'''
    return svg("Clawd March", body + frame("CLAY-05", "ONE OF MANY", "CLAY.OMARCHY"))


SERIES = [("02-clawd-unit", unit), ("03-clawd-schematic", schematic), ("04-clawd-horizon", horizon),
          ("05-clawd-terminal", terminal), ("06-clawd-march", march)]


def main():
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--output", type=Path, default=root / "backgrounds", help="PNG directory")
    ap.add_argument("--svg", type=Path, help="also keep the intermediate SVGs here")
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        svg_dir = args.svg or Path(tmp)
        svg_dir.mkdir(parents=True, exist_ok=True)
        for name, fn in SERIES:
            src = svg_dir / f"{name}.svg"
            src.write_text(fn())
            png = args.output / f"{name}.png"
            subprocess.run(["rsvg-convert", "--output", str(png), str(src)], check=True)
            print(png)


if __name__ == "__main__":
    main()
