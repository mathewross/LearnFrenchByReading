"""Shared props for the Spanish scene modules (dog, rabbit, oranges, hats, cones...). Defines no scenes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *  # noqa: F401,F403

SCENES = {}
ORANGE = "#e58a2c"


def dog(x, y, s=1.0, fur="#a8754f", dark="#7d5236", d=1, run=False, mouth=False):
    """Side-view dog facing right (d=1) or left (d=-1); feet at (x, y). s=1 is ~110 px long."""
    o = []
    for lx, dk in ((-32, 1), (-20, 0), (20, 0), (32, 1)):
        sw = 8 * s if not run else 0
        o.append(rect(x + d * lx * s - 4.5 * s, y - 32 * s, 9 * s, 31 * s, dark if dk else fur, rx=4 * s))
        o.append(ell(x + d * lx * s, y - 1.5 * s, 7 * s, 3.5 * s, C["ink"]))
    o.append(line(x - d * 38 * s, y - 46 * s, x - d * 56 * s, y - 72 * s, fur, 7 * s))
    o.append(ell(x, y - 42 * s, 44 * s, 21 * s, fur))
    o.append(ell(x + d * 4 * s, y - 34 * s, 30 * s, 9 * s, "#d4a97f"))
    o.append(circ(x + d * 46 * s, y - 62 * s, 18 * s, fur))
    o.append(ell(x + d * 63 * s, y - 55 * s, 12 * s, 8 * s, "#d4a97f"))
    o.append(circ(x + d * 71 * s, y - 59 * s, 3.4 * s, C["ink"]))
    if mouth:
        o.append(path(f"M{n(x + d * 58 * s)},{n(y - 50 * s)} q{n(d * 8 * s)},{n(8 * s)} {n(d * 16 * s)},{n(-2 * s)}", "none", f'stroke="{C["ink"]}" stroke-width="{n(2 * s)}" stroke-linecap="round"'))
    o.append(circ(x + d * 52 * s, y - 67 * s, 2.6 * s, C["ink"]))
    o.append(ell(x + d * 38 * s, y - 60 * s, 7 * s, 14 * s, dark, f'transform="rotate({-d * 12} {n(x + d * 38 * s)} {n(y - 70 * s)})"'))
    return "<g>" + "".join(o) + "</g>"


def rabbit(x, y, s=1.0, fur="#fffdf8"):
    """Sitting white rabbit, feet at (x, y)."""
    return ("<g>" + ell(x, y - 22 * s, 26 * s, 22 * s, fur) + ell(x - 14 * s, y - 3 * s, 14 * s, 6 * s, "#e6dcc3") + ell(x + 14 * s, y - 3 * s, 14 * s, 6 * s, "#e6dcc3")
            + circ(x - 25 * s, y - 24 * s, 7 * s, fur) + circ(x, y - 52 * s, 17 * s, fur)
            + ell(x - 8 * s, y - 82 * s, 6 * s, 20 * s, fur) + ell(x + 8 * s, y - 82 * s, 6 * s, 20 * s, fur)
            + ell(x - 8 * s, y - 80 * s, 2.6 * s, 14 * s, C["pink"]) + ell(x + 8 * s, y - 80 * s, 2.6 * s, 14 * s, C["pink"])
            + circ(x - 6 * s, y - 55 * s, 2.2 * s, C["ink"]) + circ(x + 6 * s, y - 55 * s, 2.2 * s, C["ink"])
            + circ(x, y - 49 * s, 2.6 * s, "#d98f8a") + "</g>")


def orange(x, y, r=11):
    return circ(x, y, r, ORANGE) + circ(x - r * .3, y - r * .3, r * .22, "#fff", 'opacity=".4"') + circ(x + r * .1, y - r * .95, r * .16, "#5f8a66")


def tomato(x, y, r=11):
    return circ(x, y, r, "#cf4a3b") + circ(x - r * .3, y - r * .3, r * .2, "#fff", 'opacity=".35"') + ell(x, y - r * .95, r * .45, r * .2, "#5f8a66")


def basket(x, y, w=70, h=44, handle=True, fill="#c99a5b"):
    o = []
    if handle:
        o.append(path(f"M{n(x - w * .42)},{n(y - h)} q{n(w * .42)},{n(-h * 1.1)} {n(w * .84)},0", "none", f'stroke="#a97a3f" stroke-width="5"'))
    o.append(path(f"M{n(x - w / 2)},{n(y - h)} h{n(w)} l{n(-w * .1)},{n(h)} h{n(-w * .8)} Z", fill))
    for k in (1, 2):
        o.append(line(x - w * .45 + k * w * .02, y - h + k * h / 3, x + w * .45 - k * w * .02, y - h + k * h / 3, "#a97a3f", 2))
    return "".join(o)


def sombrero(x, y, r=26, fill="#f2cc4a"):
    return ell(x, y, r * 1.5, r * .42, fill) + path(f"M{n(x - r * .85)},{n(y - 2)} q{n(r * .85)},{n(-r * 1.5)} {n(r * 1.7)},0 Z", fill) + rect(x - r * .85, y - r * .5, r * 1.7, r * .2, "#d9863e")


def cone(x, y, scoop="#fffdf8", s=1.0):
    return (poly([(x - 9 * s, y - 28 * s), (x + 9 * s, y - 28 * s), (x, y)], "#d9a357") + circ(x, y - 34 * s, 12 * s, scoop)
            + circ(x - 3 * s, y - 38 * s, 3 * s, "#fff", 'opacity=".5"'))


def balloon(x, y, color, r=18):
    return (line(x, y + r, x + 4, y + r + 60, "#9aa3a6", 1.5) + ell(x, y, r * .86, r, color) + poly([(x - 3, y + r - 1), (x + 3, y + r - 1), (x, y + r + 5)], color)
            + circ(x - r * .3, y - r * .35, r * .18, "#fff", 'opacity=".4"'))


def churro(x, y, ang=-15, ln=62):
    o = f'<g transform="translate({n(x)},{n(y)}) rotate({n(ang)})">' + rect(-ln / 2, -6, ln, 12, "#e0a84e", rx=6)
    o += "".join(line(-ln / 2 + 8 + k * 9, -5, -ln / 2 + 8 + k * 9, 5, "#b9792f", 1.8) for k in range(int(ln / 9) - 1))
    return o + rect(-ln / 2 + 6, -8, ln - 12, 3, "#fff", extra='opacity=".7"') + "</g>"


def grass(y=300, c="#a9c58f"):
    return [rect(0, y, W, H - y, c), rect(0, y, W, 6, "#8fae78")]


def cloudy(*pos):
    return "".join(cloud(x, y, s) for x, y, s in pos)
