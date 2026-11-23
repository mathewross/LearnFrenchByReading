import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *


def sparkle_drops(cx, cy, k=7, r=60):
    o = []
    for i in range(k):
        a = -math.pi * (i / (k - 1)) - .1
        o.append(f'<path d="M{n(cx + math.cos(a) * r)} {n(cy + math.sin(a) * r)} q4,-8 8,0 q-4,8 -8,0Z" fill="#9cc3cc"/>')
    return "".join(o)


def bird(x, y, s=1.0):
    return ("<g>" + ell(x, y, 15 * s, 11 * s, "#4a82b8") + circ(x + 13 * s, y - 8 * s, 8 * s, "#4a82b8") + poly([(x + 20 * s, y - 9 * s), (x + 28 * s, y - 6 * s), (x + 20 * s, y - 4 * s)], C["mustard"])
            + circ(x + 15 * s, y - 10 * s, 1.8 * s, C["ink"]) + poly([(x - 12 * s, y), (x - 30 * s, y + 6 * s), (x - 12 * s, y + 8 * s)], "#3a6a9c") + ell(x - 2 * s, y + 2 * s, 8 * s, 5 * s, "#6fa0d2") + "</g>")


def max_1_window():
    b = [rect(0, 0, W, H, "#efe3c9"), rect(0, 292, W, 108, "#c9ae88")]
    wx, wy, ww, wh = 300, 40, 300, 230
    b.append(rect(wx - 12, wy - 12, ww + 24, wh + 24, C["white"], rx=8) + rect(wx, wy, ww, wh, "#cfe8ee"))
    b.append(sun(560, 80, 20) + cloud(330, 90, .7))
    b.append(rect(wx, 222, ww, 48, "#9fc09a"))
    b.append(tree(450, 262, 230))
    b.append(line(470, 120, 540, 140, C["brown"], 7))
    b.append(bird(526, 124, 1.0))
    b.append(rect(wx + ww / 2 - 4, wy, 8, wh, C["white"]) + rect(wx, wy + wh / 2 - 4, ww, 8, C["white"]))
    b.append(rect(0, 270, 620, 26, "#a98466", rx=4))
    b.append(rect(0, 296, W, 104, "#b49670") + rect(0, 296, W, 6, "#9c7f58"))
    # Max on the table
    b.append(cat(250, 272, 1.7, look=1))
    b.append(ell(100, 270, 56, 10, "#d8d1c0") + rect(46, 240, 108, 30, C["teal"], rx=8) + ell(100, 240, 54, 8, "#bfe0ea"))
    return wrap(b)


def max_1_fall():
    b = [rect(0, 0, W, H, "#efe3c9"), rect(0, 290, W, 110, "#d8cdb0")]
    b.append(rect(30, 40, 220, 170, C["white"], rx=8) + rect(42, 52, 196, 146, "#cfe8ee") + rect(136, 52, 8, 146, C["white"]) + rect(42, 121, 196, 8, C["white"]))
    b.append(bird(190, 100, .8))
    b.append(rect(0, 200, W, 0, "#0000"))
    b.append(person(500, 394, h=260, coat="#e3b960", hair="#6b4a3a", style="bun", mood="open", cheeks=True, arms=((452, 280), (550, 300))))
    # bowl with wet Max
    b.append(cat(300, 330, 1.7, wet=True, tail=False, eyes="#7fb77e"))
    b.append(path("M190,300 H410 Q400,372 300,372 Q200,372 190,300 Z", C["teal"]) + ell(300, 300, 110, 12, "#bfe0ea") + rect(250, 366, 100, 10, C["deep"], rx=5))
    b.append(path("M200,304 H400 Q392,330 300,334 Q208,330 200,304 Z", "#bfe0ea", 'opacity=".9"'))
    b.append(sparkle_drops(300, 190, 9, 120))
    return wrap(b)


def max_2_watch():
    b = [rect(0, 0, W, H, "#f1e8d2"), rect(0, 270, W, 130, "#c9ae88"), rect(0, 262, W, 8, "#b49670")]
    for k in range(5):
        for j in range(3):
            b.append(rect(20 + k * 130, 30 + j * 56, 120, 48, "#e8dcc0" if (k + j) % 2 else "#ece3cc", rx=4))
    b.append(rect(120, 276, 440, 26, "#a98466", rx=4))
    b.append(cat(230, 278, 1.9, look=1))
    b.append(bowl_fish(450, 278, 170, 140))
    b.append(sparkle_drops(450, 100, 0, 0))
    return wrap(b)


def max_2_paw():
    b = [rect(0, 0, W, H, "#f1e8d2"), rect(0, 270, W, 130, "#c9ae88"), rect(0, 262, W, 8, "#b49670")]
    for k in range(5):
        for j in range(3):
            b.append(rect(20 + k * 130, 30 + j * 56, 120, 48, "#e8dcc0" if (k + j) % 2 else "#ece3cc", rx=4))
    b.append(rect(120, 276, 440, 26, "#a98466", rx=4))
    b.append(cat(210, 278, 1.9, look=1, tail=True))
    b.append(bowl_fish(450, 278, 170, 140))
    # reaching paw
    b.append(line(250, 195, 395, 200, "#8d979b", 24))
    b.append(circ(402, 202, 15, "#b7bfc2"))
    b.append(path("M375,192 q30,-10 60,0", "none", 'stroke="#fff" stroke-width="3" opacity=".7"'))
    b.append(sparkle_drops(402, 196, 5, 40))
    b.append(ell(402, 204, 40, 8, "#fff", 'opacity=".4"'))
    return wrap(b)


SCENES = {"max-1-1": max_1_window, "max-1-2": max_1_fall, "max-2-1": max_2_watch, "max-2-2": max_2_paw}
