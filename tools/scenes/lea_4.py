import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *


def heart(x, y, s, color="#e58f86"):
    return path(f"M{n(x)},{n(y + s * .9)} C{n(x - s * 1.6)},{n(y - s * .2)} {n(x - s * .7)},{n(y - s * 1.2)} {n(x)},{n(y - s * .4)} "
                f"C{n(x + s * .7)},{n(y - s * 1.2)} {n(x + s * 1.6)},{n(y - s * .2)} {n(x)},{n(y + s * .9)} Z", color)


def night_city(x, y, w, h):
    """Skyline with a lit Eiffel tower, drawn inside a window rect at (x, y, w, h)."""
    o = [rect(x, y, w, h, "#27345a")]
    rnd = random.Random(4)
    for _ in range(26):
        o.append(circ(x + rnd.uniform(6, w - 6), y + rnd.uniform(6, h * .5), rnd.uniform(1, 2.2), "#f3e3b0", 'opacity=".9"'))
    o.append(circ(x + w * .18, y + h * .2, 20, "#f3e3b0") + circ(x + w * .18 + 8, y + h * .2 - 4, 18, "#27345a"))
    for bx, bw, bh in [(0, 50, 70), (46, 40, 100), (86, 55, 60), (w - 90, 50, 80), (w - 48, 48, 110)]:
        o.append(rect(x + bx, y + h - bh, bw, bh, "#1b2442"))
        for k in range(int(bh / 24)):
            o.append(rect(x + bx + 8, y + h - bh + 10 + k * 24, 7, 9, "#f0c75e"))
    o.append(tower(x + w * .55, y + h, h * .8, "#e0b04c"))
    return "".join(o)


def lea_4_1():
    b = [rect(0, 0, W, H, "#e8dfc8"), rect(0, 280, W, 120, "#c9ae88")]
    b.append(rect(40, 40, 170, 150, "#fffdf8", rx=8) + night_city(50, 50, 150, 130) + rect(121, 50, 8, 130, "#fffdf8"))
    b.append(rect(448, 120, 100, 14, "#7a5c47") + rect(456, 134, 8, 70, "#7a5c47"))
    # bed head and Léa
    b.append(rect(190, 130, 260, 150, "#8a6b52", rx=14))
    b.append(person(320, 322, h=250, coat=C["sage_d"], look=0, mood="open", cheeks=True, show_legs=False, arms=((276, 250), (352, 138))))
    b.append(rect(346, 128, 14, 26, C["dgrey"], rx=4))
    b.append(rect(190, 270, 260, 90, C["terra"], rx=10) + rect(190, 270, 260, 14, C["terra_d"]))
    b.append(rect(176, 350, 288, 22, "#7a5c47", rx=6))
    b.append(rect(226, 262, 70, 24, C["white"], rx=10))
    # nightstand lamp
    b.append(rect(490, 270, 110, 100, C["brown"], rx=6) + rect(500, 296, 90, 4, "#4f3629"))
    b.append(rect(541, 224, 8, 46, C["dgrey"]) + poly([(516, 226), (574, 226), (558, 190), (532, 190)], C["mustard"]))
    b.append(ell(545, 232, 60, 14, "#f6dc86", 'opacity=".35"'))
    # mother thought bubble
    b.append(circ(425, 100, 5, C["white"], f'stroke="{C["lgrey"]}" stroke-width="2"') + circ(412, 120, 3, C["white"], f'stroke="{C["lgrey"]}" stroke-width="2"'))
    b.append(ell(470, 70, 60, 36, C["white"], f'stroke="{C["lgrey"]}" stroke-width="2"') + heart(470, 66, 15))
    return wrap(b)


def lea_4_2():
    b = [rect(0, 0, W, H, "#cdbfa5")]
    b.append(rect(150, 18, 360, 290, "#fffdf8", rx=10) + night_city(166, 34, 328, 258) + rect(326, 34, 8, 258, "#fffdf8") + rect(166, 160, 328, 8, "#fffdf8"))
    b.append(rect(130, 300, 400, 20, "#a98466", rx=4))
    b.append(rect(0, 320, W, 80, "#b49670"))
    # curtains
    b.append(path("M0,0 H170 Q150,150 176,320 H0 Z", C["terra"]) + path("M640,0 H480 Q500,150 474,320 H640 Z", C["terra"]))
    b.append(path("M60,0 Q50,160 70,320", "none", f'stroke="{C["terra_d"]}" stroke-width="6"') + path("M580,0 Q590,160 570,320", "none", f'stroke="{C["terra_d"]}" stroke-width="6"'))
    b.append(person(120, 400, h=250, coat=C["sage_d"], look=1, cheeks=True, arms=((82, 300), (190, 258))))
    b.append(mug(540, 318, 30))
    return wrap(b)


SCENES = {"lea-4-1": lea_4_1, "lea-4-2": lea_4_2}
