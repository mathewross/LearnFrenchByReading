import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

MARTA = dict(coat="#f3efe3", hair="#3a2e28", style="bun", cheeks=True)


def pendant(x, y, color):
    return line(x, 0, x, y, C["ink"], 2) + path(f"M{n(x - 16)},{n(y + 18)} q16,-30 32,0 Z", color) + circ(x, y + 20, 4, "#f6e49a")


def hot_cup(x, y, kind):
    """kind: choc (milky brown, big) or coffee (small dark)."""
    if kind == "choc":
        return cup(x, y, 30, "#fffdf8") + ell(x, y - 21, 13, 3, "#8a5a3a") + path(f"M{n(x - 6)},{n(y - 30)} q-4,-7 0,-12 q4,-6 0,-12", "none", 'stroke="#fff" stroke-width="2.5" stroke-linecap="round"')
    return cup(x, y, 22, "#fffdf8") + ell(x, y - 15, 9, 2.6, "#3a2a22") + path(f"M{n(x - 4)},{n(y - 22)} q-4,-6 0,-10 q4,-5 0,-10", "none", 'stroke="#fff" stroke-width="2.5" stroke-linecap="round"')


def cafe_bg():
    b = [rect(0, 0, W, H, "#efe0c0"), rect(0, 250, W, 150, "#c9ae88"), rect(0, 238, W, 14, "#a98466")]
    b.append(rect(0, 150, W, 100, "#d9a357", extra='opacity=".35"'))
    return b


def cafe_1():
    b = cafe_bg()
    b.append(rect(40, 40, 150, 130, C["white"], rx=6) + rect(50, 50, 130, 110, "#f9e6a8") + sun(115, 112, 24) + rect(111, 50, 8, 110, C["white"]))
    for k in range(3):
        b.append(rect(430, 80 + k * 50, 190, 6, "#a98466") + "".join(cup(448 + j * 34, 78 + k * 50, 20, [C["white"], C["terra"], C["sage"]][(j + k) % 3]) for j in range(5)))
    for xx, c_ in ((230, C["red"]), (320, C["mustard"]), (410, C["teal"])):
        b.append(pendant(xx, 70, c_))
    b.append(person(300, 346, h=250, arms=((250, 250), (370, 232)), show_legs=False, look=-1, mood="smile", **MARTA, pants=C["navy"]))
    b.append(rect(300, 244, 70, 60, "#d9d1c0", rx=6) + rect(312, 232, 46, 14, "#9aa3a6", rx=3) + rect(306, 296, 58, 8, C["dgrey"]))
    b.append(rect(60, 262, 520, 22, "#8a6248", rx=4) + rect(70, 284, 500, 116, C["brown"]) + rect(70, 284, 500, 10, "#00000022"))
    b.append(rect(110, 246, 50, 16, "#e6c590", rx=8) + baguette(140, 250, 80, -6, 12) + "".join(cup(420 + k * 40, 262, 22, C["white"]) for k in range(3)))
    for k in range(4):
        b.append(circ(150 + k * 90, 316, 16, "#6f4a38"))
    return wrap(b)


def tables(b):
    for tx in (160, 480):
        b.append(ell(tx, 300, 90, 22, "#d0c7b3") + ell(tx, 294, 90, 22, C["white"]) + rect(tx - 7, 314, 14, 86, C["brown"]))


def cafe_2():
    b = cafe_bg()
    tables(b)
    b.append(person(160, 392, h=240, coat=C["navy"], hair="#9aa3a6", style="short", mood="sad", look=1, arms=((124, 296), (200, 292)), show_legs=False))
    b.append(person(480, 392, h=232, coat=C["terra"], hair="#cfd5d6", style="bob", mood="sad", look=-1, cheeks=True, arms=((440, 292), (520, 290)), show_legs=False))
    b.append(rect(112, 296, 96, 6, "#00000000") + hot_cup(130, 304, "choc") + hot_cup(500, 304, "coffee"))
    b.append(rect(250, 118, 140, 10, "#a98466", extra='opacity="0"'))
    b.append(person(320, 392, h=262, arms=((290, 286), (370, 270)), look=1, mood="open", **MARTA, pants=C["navy"]))
    b.append(rect(280, 276, 110, 8, "#b9bfc1", rx=4) + hot_cup(300, 276, "coffee") + hot_cup(360, 276, "choc"))
    b.append(circ(190, 104, 14, "#f6e49a", 'opacity="0"'))
    return wrap(b)


def cafe_3():
    b = cafe_bg()
    b.append(ell(320, 312, 170, 34, "#d0c7b3") + ell(320, 304, 170, 34, C["white"]) + rect(312, 330, 16, 70, C["brown"]))
    b.append(person(210, 392, h=250, coat=C["navy"], hair="#9aa3a6", style="short", mood="open", look=1, arms=((180, 290), (270, 292)), show_legs=False))
    b.append(person(430, 392, h=240, coat=C["terra"], hair="#cfd5d6", style="bob", mood="open", look=-1, cheeks=True, arms=((380, 292), (470, 292)), show_legs=False))
    b.append(ell(320, 306, 40, 10, "#f3efe3") + churro(300, 296, -12, 56) + churro(334, 296, 14, 56) + churro(318, 288, 2, 56))
    b.append(hot_cup(250, 306, "choc") + hot_cup(400, 306, "coffee"))
    b.append(person(570, 392, h=200, coat="#6f8f6a", hair="#2b2622", style="short", mood="smile", look=-1))
    b.append(person(66, 392, h=214, coat=C["white"], hair="#3a2e28", style="bun", mood="smile", cheeks=True, look=1, **{"pants": C["navy"]}))
    return wrap(b)


SCENES = {"es-la-cafeteria-1": cafe_1, "es-la-cafeteria-2": cafe_2, "es-la-cafeteria-3": cafe_3}
