"""Shared props for the extra scene modules (cat, fruit, fish bowl, bread, mug...). Defines no scenes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from make_images import *  # noqa: F401,F403

SCENES = {}


def cat(x, y, s=1.0, fur="#8d979b", belly="#b7bfc2", look=0, wet=False, fat=1.0, tail=True, eyes="#7fb77e", sleepy=False):
    """Sitting cat, front view, feet at (x, y). s scales; fat widens the body."""
    if wet:
        fur, belly = "#6f787c", "#8c9598"
    o = []
    bw, bh = 34 * s * fat, 40 * s
    if tail:
        o.append(path(f"M{n(x + bw * .8)},{n(y - 6 * s)} q{n(46 * s)},{n(-4 * s)} {n(40 * s)},{n(-52 * s)}", "none",
                      f'stroke="{fur}" stroke-width="{n(11 * s)}" stroke-linecap="round"'))
    o.append(ell(x, y - bh * .95, bw, bh, fur))
    o.append(ell(x, y - bh * .75, bw * .55, bh * .62, belly))
    for sx in (-1, 1):
        o.append(ell(x + sx * bw * .38, y - 6 * s, 12 * s, 8 * s, belly))
    hr = 27 * s
    hy = y - bh * 1.95 - 8 * s
    for sx in (-1, 1):
        o.append(poly([(x + sx * hr * .95, hy - hr * .2), (x + sx * hr * .75, hy - hr * 1.3), (x + sx * hr * .2, hy - hr * .85)], fur))
        o.append(poly([(x + sx * hr * .8, hy - hr * .35), (x + sx * hr * .72, hy - hr * 1.0), (x + sx * hr * .35, hy - hr * .78)], "#e7a9a0"))
    o.append(circ(x, hy, hr, fur))
    ex = look * 3 * s
    for sx in (-1, 1):
        if sleepy:
            o.append(path(f"M{n(x + sx * hr * .42 - 6 * s)},{n(hy)} q{n(6 * s)},{n(6 * s)} {n(12 * s)},0", "none",
                          f'stroke="{C["ink"]}" stroke-width="{n(2 * s)}" stroke-linecap="round"'))
        else:
            o.append(circ(x + sx * hr * .42, hy, 7.5 * s, eyes))
            o.append(ell(x + sx * hr * .42 + ex, hy, 2.6 * s, 6 * s, C["ink"]))
    o.append(poly([(x - 4 * s, hy + 8 * s), (x + 4 * s, hy + 8 * s), (x, hy + 13 * s)], "#d98f8a"))
    sw = f'stroke="{C["ink"]}" stroke-width="{n(1.4 * s)}" stroke-linecap="round" opacity=".6"'
    for sx in (-1, 1):
        o.append(line(x + sx * 10 * s, hy + 12 * s, x + sx * 34 * s, hy + 8 * s, C["ink"], 1.4 * s, 'opacity=".5"'))
        o.append(line(x + sx * 10 * s, hy + 15 * s, x + sx * 34 * s, hy + 17 * s, C["ink"], 1.4 * s, 'opacity=".5"'))
    return "<g>" + "".join(o) + "</g>"


def apple(x, y, r=11, color=None):
    return circ(x, y, r, color or C["red"]) + line(x, y - r, x + 2, y - r - 5, C["brown"], 2) + circ(x - r * .35, y - r * .3, r * .22, "#fff", 'opacity=".35"')


def pear(x, y, s=12, color="#cfd36a"):
    return (circ(x, y + s * .35, s * .8, color) + circ(x, y - s * .55, s * .5, color)
            + line(x, y - s, x + 2, y - s - 6, C["brown"], 2))


def bowl_fish(x, y, w=150, h=120, water="#bfe0ea"):
    """Round glass fish bowl with a goldfish; (x, y) = bottom centre."""
    o = [ell(x, y - h * .5, w / 2, h / 2, "#e9f4f6", f'stroke="#9cc3cc" stroke-width="4"'),
         path(f"M{n(x - w / 2 + 3)},{n(y - h * .55)} A{n(w / 2 - 3)},{n(h / 2 - 3)} 0 0 0 {n(x + w / 2 - 3)},{n(y - h * .55)} Z", water, 'opacity=".95"'),
         ell(x, y - h * .55, w / 2 - 3, 4, "#d9eef2"),
         ell(x, y - h * .32, w * .22, h * .14, "#ee8f3e"),
         poly([(x + w * .18, y - h * .32), (x + w * .34, y - h * .46), (x + w * .34, y - h * .18)], "#ee8f3e"),
         circ(x - w * .12, y - h * .35, 3.6, C["white"]) + circ(x - w * .125, y - h * .35, 1.8, C["ink"]),
         circ(x - w * .3, y - h * .62, 4, "#fff", 'opacity=".7"'), circ(x - w * .24, y - h * .78, 3, "#fff", 'opacity=".7"'),
         ell(x, y - 4, w * .3, 6, "#9cc3cc")]
    return "<g>" + "".join(o) + "</g>"


def baguette(x, y, length=120, angle=-20, w=15, color="#d9a357"):
    cuts = "".join(line(-length * .3 + k * length * .2, -w * .35, -length * .3 + k * length * .2 + 6, w * .35, "#b9792f", 3) for k in range(4))
    return (f'<g transform="translate({n(x)},{n(y)}) rotate({n(angle)})">'
            + rect(-length / 2, -w / 2, length, w, color, rx=w / 2) + cuts + "</g>")


def mug(x, y, w=30, color=None, steam=True):
    color = color or C["white"]
    o = [rect(x - w / 2, y - w * .8, w, w * .8, color, rx=5),
         path(f"M{n(x + w / 2 - 1)},{n(y - w * .62)} q{n(w * .4)},{n(w * .08)} 0,{n(w * .4)}", "none", f'stroke="{color}" stroke-width="4"'),
         ell(x, y - w * .8, w / 2, 3.5, "#6b4a3a")]
    if steam:
        for dx in (-6, 6):
            o.append(path(f"M{n(x + dx)},{n(y - w)} q-5,-8 0,-15 q5,-8 0,-15", "none", 'stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"'))
    return "".join(o)


def box(x, y, w, h, color="#d2a46f", tape=True):
    o = [rect(x, y, w, h, color), rect(x, y, w, h * .14, "#bd8d57")]
    if tape:
        o.append(rect(x + w * .42, y, w * .16, h, "#e6c590", extra='opacity=".8"'))
    return "".join(o)


def floor_wall(wall, floor, fy=300, trim=None):
    return [rect(0, 0, W, fy, wall), rect(0, fy, W, H - fy, floor), rect(0, fy - 8, W, 8, trim or "#00000014")]


def window(x, y, w, h, sky="#cfe3e6", frame="#fffdf8", cross=True):
    o = [rect(x - 8, y - 8, w + 16, h + 16, frame, rx=6), rect(x, y, w, h, sky)]
    return "".join(o)


def window_cross(x, y, w, h, frame="#fffdf8"):
    return rect(x + w / 2 - 4, y, 8, h, frame) + rect(x, y + h / 2 - 4, w, 8, frame)


def tower(x, base, h, fill):
    """Eiffel tower silhouette; tip at (x, base - h)."""
    p = [(0, -1), (.05, -.62), (.1, -.4), (.2, 0), (.14, 0), (.07, -.16), (-.07, -.16), (-.14, 0), (-.2, 0), (-.1, -.4), (-.05, -.62)]
    return (poly([(x + a * h, base + b * h) for a, b in p], fill)
            + rect(x - .075 * h, base - .42 * h, .15 * h, .02 * h, fill) + rect(x - .055 * h, base - .64 * h, .11 * h, .02 * h, fill))
