import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *

CLAIRE = dict(coat="#4f7c9a", hair="#5a3a2a", style="bob")


def loaf(x, y, w=44, h=26, color="#d9a357"):
    return ell(x, y, w / 2, h / 2, color) + "".join(line(x - w * .25 + k * w * .25, y - h * .25, x - w * .15 + k * w * .25, y + h * .15, "#b9792f", 2.5) for k in range(3))


def bread_1():
    b = [rect(0, 0, W, H, "#e9ddc0"), rect(0, 330, W, 70, "#b9b2a1"), rect(0, 326, W, 8, "#a39c8b")]
    # shopfront
    b.append(rect(120, 40, 400, 290, "#d9a357"))
    b.append(rect(120, 40, 400, 56, "#f6f1e4"))
    b.append(ell(320, 68, 60, 14, "#d9a357") + baguette(320, 68, 120, -8, 12) )
    for i in range(10):
        a = 120 + i * 40
        b.append(path(f"M{a},96 h40 q-20,22 -40,0 Z", C["red"] if i % 2 == 0 else C["cream"]))
        b.append(rect(a, 80, 40, 16, C["red"] if i % 2 == 0 else C["cream"]))
    b.append(rect(150, 140, 150, 140, "#fff6dc", rx=6, extra=f'stroke="{C["brown"]}" stroke-width="8"'))
    b.append(rect(158, 148, 134, 124, "#fdebb5"))
    b.append(rect(158, 238, 134, 10, "#a98466"))
    for k, xx in enumerate((190, 218, 246, 270)):
        b.append(loaf(xx, 226, 40, 24))
    for k in range(4):
        b.append(baguette(184 + k * 22, 190, 70, 70, 11))
    b.append(croissant(250, 188, 30))
    b.append(rect(330, 140, 150, 190, C["brown"], rx=4) + rect(340, 150, 130, 180, "#f6dc86"))
    b.append(rect(340, 150, 130, 180, "#fff0c0", extra='opacity=".5"'))
    b.append(circ(458, 240, 5, C["brown"]))
    b.append(person(520, 396, h=250, mood="smile", cheeks=True, look=-1, arms=((482, 300), (574, 300)), **CLAIRE))
    return wrap(b)


def bread_2():
    b = [rect(0, 0, W, H, "#f1e2c0"), rect(0, 316, W, 84, "#c9ae88")]
    b.append(rect(0, 40, W, 190, "#e9d3a0"))
    for k in range(8):
        b.append(rect(20 + k * 78, 58 + (k % 2) * 4, 66, 8, "#a98466"))
    # shelf with bread behind
    b.append(rect(0, 150, W, 8, "#a98466"))
    for k in range(7):
        b.append(baguette(34 + k * 18, 120, 74, 74, 11))
    for k in range(4):
        b.append(loaf(300 + k * 52, 138, 44, 26))
    b.append(rect(0, 238, W, 8, "#a98466"))
    # baker
    b.append(person(340, 330, h=270, coat=C["white"], hair="#3a2e28", style="short", mood="smile", show_legs=False, arms=((290, 262), (396, 250))))
    b.append(rect(316, 54, 48, 8, C["white"]) )
    b.append(rect(298, 66, 84, 14, "#fffdf8", rx=6) + rect(306, 60, 68, 16, "#fffdf8", rx=7))
    # bag in hand + counter
    b.append(rect(404, 232, 40, 36, "#d9b77a", rx=3) + path("M404,232 l8,-8 h24 l8,8 Z", "#c49a5a"))
    b.append(rect(120, 268, 540, 22, "#a98466"))
    b.append(rect(130, 290, 520, 110, C["brown"]))
    b.append(croissant(200, 262, 34) + croissant(250, 262, 34) + ell(310, 260, 24, 10, "#6b4a3a") + ell(310, 254, 24, 10, "#7a4a35"))
    b.append(circ(520, 282, 8, C["mustard"], f'stroke="#b98a2e" stroke-width="2"') + circ(542, 284, 8, C["mustard"], f'stroke="#b98a2e" stroke-width="2"'))
    # Claire
    b.append(person(110, 408, h=268, mood="smile", cheeks=True, look=1, arms=((70, 318), (190, 275)), **CLAIRE))
    return wrap(b)


def bread_3():
    b = [rect(0, 0, W, H, "#bfd3d6"), rect(0, 300, W, 100, "#6b7478")]
    # bus window with city
    b.append(rect(30, 40, 580, 220, "#cfe8ee", rx=14))
    for bx, bw, bh, f in [(60, 90, 100, "#e7d6b0"), (170, 70, 120, "#d99f90"), (260, 90, 90, "#efe2c4"), (370, 80, 130, "#c98a62"), (470, 100, 100, "#e5d3ae")]:
        b.append(rect(bx, 240 - bh, bw, bh, f) + "".join(rect(bx + 12 + (k % 3) * 26, 240 - bh + 14 + (k // 3) * 32, 14, 18, "#9fb6bb") for k in range(6)))
    b.append(rect(30, 240, 580, 20, "#9fc09a") + sun(560, 80, 22))
    b.append(rect(30, 40, 580, 220, "none", rx=14, extra=f'stroke="{C["deep"]}" stroke-width="10"'))
    b.append(rect(316, 40, 10, 220, C["deep"]))
    # seat
    b.append(rect(120, 230, 360, 100, C["terra"], rx=18))
    b.append(person(300, 360, h=250, mood="smile", cheeks=True, show_legs=False, look=0, arms=((250, 250), (338, 150)), **CLAIRE))
    b.append(rect(120, 300, 360, 70, C["terra_d"], rx=12))
    # croissant at mouth, bag on seat
    b.append(croissant(350, 130, 34))
    b.append(rect(416, 286, 56, 54, "#d9b77a", rx=3) + baguette(440, 268, 90, 70, 12))
    # pole
    b.append(rect(520, 40, 12, 330, "#b9bfc1") + rect(520, 40, 4, 330, "#dfe3e4"))
    return wrap(b)


SCENES = {"boulangerie-1": bread_1, "boulangerie-2": bread_2, "boulangerie-3": bread_3}
