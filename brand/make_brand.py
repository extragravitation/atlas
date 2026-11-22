"""Build the Atlas of Extra Gravitation identity files (logo G1).

Run from the repository root:  python3 brand/make_brand.py
Writes SVG masters to brand/svg/, raster files to brand/png/ (needs
rsvg-convert, ImageMagick `convert`, and the Inter Tight and Source Code Pro
fonts installed locally for the lockups), and the site's icons to
site/public/.

The mark is drawn, not plotted from data. The line stands for Newtonian
gravity on detected matter; five circles leave it in a shallow arc, growing as
they go. Colour shows position along the sweep and never stands for a dataset.
"""
import math, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = os.path.join(ROOT, "brand", "svg")
PNG = os.path.join(ROOT, "brand", "png")
PUB = os.path.join(ROOT, "site", "public")

DARK = dict(bg="#07090D", ink="#F2F4F7", sub="#9AA6B2", accent="#FFB454",
            circles=["#5CC8FF", "#A8D084", "#F5D90A", "#FAC62F", "#FFB454"])
LIGHT = dict(bg="#FFFFFF", ink="#0B0D12", sub="#4A4F59", accent="#C2410C",
             circles=["#1F5FA8", "#3B7D52", "#8A6A00", "#B0520A", "#C2410C"])

# ---- geometry (64-unit grid) ------------------------------------------------
RADII = [2, 2.8, 4, 5.6, 7.6]
S, C, E = (53, 17), (36, 13), (16, 26)        # quadratic curve the circles sit on
LINE = ((58, 12), (22, 48))                    # the reference line
GAP = 1.6                                      # gap between neighbouring circles


def _bez(t):
    return ((1 - t) ** 2 * S[0] + 2 * (1 - t) * t * C[0] + t * t * E[0],
            (1 - t) ** 2 * S[1] + 2 * (1 - t) * t * C[1] + t * t * E[1])


def _chain():
    pts = [_bez(i / 2000) for i in range(2001)]
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.dist(pts[i], pts[i - 1]))
    need = sum(RADII[i] + RADII[i + 1] for i in range(len(RADII) - 1))
    k = (cum[-1] - GAP * (len(RADII) - 1)) / need
    rs = [r * k for r in RADII]
    out, d = [], 0.0
    for i, r in enumerate(rs):
        if i:
            d += rs[i - 1] + r + GAP
        j = min(range(len(cum)), key=lambda q: abs(cum[q] - d))
        out.append((pts[j][0], pts[j][1], r))
    return out


def _sd(x, y):
    (x0, y0), (x1, y1) = LINE
    n = math.dist(LINE[0], LINE[1])
    nx, ny = (y1 - y0) / n, -(x1 - x0) / n
    if -nx - ny < 0:
        nx, ny = -nx, -ny
    return (x - x0) * nx + (y - y0) * ny, ny


def layout(small):
    """Circles moved straight up until the first clears the line, then centred."""
    w = 3.9 if small else 2.6
    clear = w / 2 + (1.6 if small else 1.1)
    circ = [(x, y, max(r, 2.6) if small else r) for x, y, r in _chain()]
    d, ny = _sd(circ[0][0], circ[0][1])
    dy = (circ[0][2] + clear - d) / ny
    circ = [(x, y + dy, r) for x, y, r in circ]
    (x0, y0), (x1, y1) = LINE
    lo = min(min(y - r for x, y, r in circ), y0, y1)
    hi = max(max(y + r for x, y, r in circ), y0, y1)
    sh = (64 - (hi - lo)) / 2 - lo
    return w, [(x, y + sh, r) for x, y, r in circ], ((x0, y0 + sh), (x1, y1 + sh))


def mark_body(theme, small=False, mono=None):
    w, circ, ((ax, ay), (bx, by)) = layout(small)
    ink = mono or theme["ink"]
    cols = [mono] * 5 if mono else theme["circles"]
    out = [f'<line x1="{ax:.2f}" y1="{ay:.2f}" x2="{bx:.2f}" y2="{by:.2f}" stroke="{ink}" stroke-width="{w:.2f}" stroke-linecap="round"/>']
    out += [f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{c}"/>' for (x, y, r), c in zip(circ, cols)]
    return "".join(out)


def mark_svg(theme, small=False, bg=True, mono=None, radius=0):
    rect = f'<rect width="64" height="64" rx="{radius}" fill="{theme["bg"]}"/>' if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" '
            f'aria-label="Atlas of Extra Gravitation">{rect}{mark_body(theme, small, mono)}</svg>\n')


def lockup_svg(theme, subtitle=True):
    h = 120 if subtitle else 96
    sub = (f'<text x="128" y="88" font-family="Inter Tight, sans-serif" font-size="20" fill="{theme["sub"]}">'
           'The acceleration discrepancy, from star clusters to galaxy clusters</text>') if subtitle else ""
    ty = 58 if subtitle else 60
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {h}" role="img" aria-label="Atlas of Extra Gravitation">'
            f'<rect width="760" height="{h}" fill="{theme["bg"]}"/>'
            f'<g transform="translate(16 {(h - 96) / 2}) scale(1.5)">{mark_body(theme)}</g>'
            f'<text x="128" y="{ty}" font-family="Inter Tight, sans-serif" font-weight="700" font-size="40" letter-spacing="-0.8" fill="{theme["ink"]}">Atlas of Extra Gravitation</text>'
            f'{sub}</svg>\n')


def banner_svg():
    t = DARK
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3000 1000">'
            f'<rect width="3000" height="1000" fill="{t["bg"]}"/>'
            f'<g transform="translate(220 200) scale(9.375)">{mark_body(t)}</g>'
            f'<text x="1020" y="470" font-family="Inter Tight, sans-serif" font-weight="800" font-size="132" letter-spacing="-4" fill="{t["ink"]}">Atlas of Extra Gravitation</text>'
            f'<text x="1024" y="575" font-family="Inter Tight, sans-serif" font-size="58" fill="{t["sub"]}">The acceleration discrepancy, from star clusters to galaxy clusters</text>'
            f'<text x="1024" y="690" font-family="Source Code Pro, monospace" font-size="46" letter-spacing="3" fill="{t["accent"]}">extragravitation.org</text>'
            '</svg>\n')


def og_svg():
    t = DARK
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630">'
            f'<rect width="1200" height="630" fill="{t["bg"]}"/>'
            f'<g transform="translate(72 64) scale(1.75)"><rect width="64" height="64" rx="14" fill="#0E141C"/>{mark_body(t)}</g>'
            f'<text x="200" y="140" font-family="Inter Tight, sans-serif" font-weight="700" font-size="44" letter-spacing="-0.8" fill="{t["ink"]}">Atlas of Extra Gravitation</text>'
            f'<text x="72" y="430" font-family="Inter Tight, sans-serif" font-weight="700" font-size="56" letter-spacing="-1.2" fill="{t["ink"]}">Where the observed pull exceeds</text>'
            f'<text x="72" y="500" font-family="Inter Tight, sans-serif" font-weight="700" font-size="56" letter-spacing="-1.2" fill="{t["ink"]}">what detected matter predicts</text>'
            f'<text x="72" y="566" font-family="Source Code Pro, monospace" font-size="26" letter-spacing="1.5" fill="{t["accent"]}">extragravitation.org</text>'
            '</svg>\n')


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def raster(src, dst, w, h=None):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    cmd = ["rsvg-convert", "-w", str(w)] + (["-h", str(h)] if h else []) + ["-o", dst, src]
    subprocess.run(cmd, check=True)


def main():
    svgs = {
        "aeg-mark-dark.svg": mark_svg(DARK),
        "aeg-mark-light.svg": mark_svg(LIGHT),
        "aeg-mark-dark-transparent.svg": mark_svg(DARK, bg=False),
        "aeg-mark-light-transparent.svg": mark_svg(LIGHT, bg=False),
        "aeg-mark-mono-white.svg": mark_svg(DARK, mono="#FFFFFF", bg=False),
        "aeg-mark-mono-black.svg": mark_svg(LIGHT, mono="#000000", bg=False),
        "aeg-mark-small-dark.svg": mark_svg(DARK, small=True),
        "aeg-lockup-dark.svg": lockup_svg(DARK),
        "aeg-lockup-light.svg": lockup_svg(LIGHT),
        "aeg-lockup-dark-short.svg": lockup_svg(DARK, False),
        "aeg-lockup-light-short.svg": lockup_svg(LIGHT, False),
        "aeg-banner-3000x1000.svg": banner_svg(),
        "aeg-share-1200x630.svg": og_svg(),
    }
    for name, text in svgs.items():
        write(os.path.join(SVG, name), text)
    if "--svg-only" in sys.argv:
        return
    s = lambda n: os.path.join(SVG, n)
    p = lambda n: os.path.join(PNG, n)
    for size in (400, 1000):
        raster(s("aeg-mark-dark.svg"), p(f"aeg-avatar-dark-{size}.png"), size)
        raster(s("aeg-mark-light.svg"), p(f"aeg-avatar-light-{size}.png"), size)
    for size in (16, 32, 48):
        raster(s("aeg-mark-small-dark.svg"), p(f"aeg-favicon-{size}.png"), size)
    raster(s("aeg-mark-dark.svg"), p("aeg-icon-180.png"), 180)
    raster(s("aeg-mark-dark.svg"), p("aeg-icon-192.png"), 192)
    raster(s("aeg-mark-dark.svg"), p("aeg-icon-512.png"), 512)
    for n in ("aeg-lockup-dark", "aeg-lockup-light", "aeg-lockup-dark-short", "aeg-lockup-light-short"):
        raster(s(n + ".svg"), p(n + ".png"), 1520)
    raster(s("aeg-banner-3000x1000.svg"), p("aeg-banner-3000x1000.png"), 3000, 1000)
    raster(s("aeg-share-1200x630.svg"), p("aeg-share-1200x630.png"), 1200, 630)
    subprocess.run(["convert", p("aeg-favicon-16.png"), p("aeg-favicon-32.png"), p("aeg-favicon-48.png"),
                    p("aeg-favicon.ico")], check=True)
    # site icons
    shutil.copy(s("aeg-mark-small-dark.svg"), os.path.join(PUB, "favicon.svg"))
    shutil.copy(p("aeg-favicon.ico"), os.path.join(PUB, "favicon.ico"))
    shutil.copy(p("aeg-icon-180.png"), os.path.join(PUB, "apple-touch-icon.png"))
    shutil.copy(p("aeg-icon-192.png"), os.path.join(PUB, "icon-192.png"))
    shutil.copy(p("aeg-icon-512.png"), os.path.join(PUB, "icon-512.png"))
    shutil.copy(p("aeg-share-1200x630.png"), os.path.join(PUB, "og-image.png"))


if __name__ == "__main__":
    main()
