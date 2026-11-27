import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

DANIEL = dict(coat="#6a8f7b", hair="#3a2e28", style="short", pants=C["navy"])
NARR = dict(coat=C["terra"], hair="#6b4a3a", style="bun", pants="#6f8790", cheeks=True)
JEFE = dict(coat=C["navy"], hair="#9aa3a6", style="short", pants="#3a4250", skin=C["skin2"])
COL1 = dict(coat=C["mustard"], hair="#2b2622", style="short", pants=C["dgrey"])
COL2 = dict(coat=C["plum"], hair="#4a3a32", style="bob", pants=C["navy"], cheeks=True)


def office_bg(fy=300):
    b = [rect(0, 0, W, H, "#ece6d6"), rect(0, fy, W, H - fy, "#b9a98c"), rect(0, fy - 8, W, 8, "#a69676")]
    for k in range(0, W, 128):
        b.append(rect(k, 0, 3, fy - 8, "#e0d9c6"))
    return b


def office_window(x, y, w, h):
    o = [rect(x - 6, y - 6, w + 12, h + 12, "#fffdf8", rx=4), rect(x, y, w, h, "#cfe3e6")]
    for k, (bx, bh) in enumerate(((6, 40), (34, 62), (66, 34), (96, 52))):
        if bx + 24 < w:
            o.append(rect(x + bx, y + h - bh, 24, bh, "#a9bcc0"))
    o.append(rect(x + w / 2 - 3, y, 6, h, "#fffdf8"))
    return "".join(o)


def desk(x, y, w=170, laptop=True, plant=False):
    o = [rect(x, y, w, 12, "#c99a5b", rx=3), rect(x + 8, y + 12, 8, 70, "#a98466"), rect(x + w - 16, y + 12, 8, 70, "#a98466")]
    if laptop:
        o.append(rect(x + w / 2 - 28, y - 38, 56, 36, "#2f3b3d", rx=4) + rect(x + w / 2 - 24, y - 34, 48, 28, "#9fc7d0", rx=2) + rect(x + w / 2 - 36, y - 3, 72, 5, "#b9bfc1", rx=2))
    if plant:
        o.append(rect(x + w - 44, y - 20, 22, 20, C["terra"], rx=3) + circ(x + w - 33, y - 30, 12, "#6a8f7b") + circ(x + w - 42, y - 22, 8, "#8fae9a"))
    return "".join(o)


def bear(x, y, s=1.0):
    o = [circ(x - 24 * s, y - 70 * s, 11 * s, "#8a5a3a"), circ(x + 24 * s, y - 70 * s, 11 * s, "#8a5a3a"),
         ell(x, y - 30 * s, 36 * s, 32 * s, "#8a5a3a"), circ(x, y - 62 * s, 28 * s, "#8a5a3a"), ell(x, y - 54 * s, 14 * s, 10 * s, "#d9b88a"),
         circ(x - 10 * s, y - 68 * s, 3 * s, C["ink"]), circ(x + 10 * s, y - 68 * s, 3 * s, C["ink"]), ell(x, y - 56 * s, 4.5 * s, 3 * s, C["ink"]),
         path(f"M{n(x - 7 * s)},{n(y - 48 * s)} q{n(7 * s)},{n(6 * s)} {n(14 * s)},0", "none", f'stroke="{C["ink"]}" stroke-width="{n(2 * s)}" stroke-linecap="round"'),
         rect(x - 18 * s, y - 12 * s, 14 * s, 14 * s, "#6e4a30", rx=5 * s), rect(x + 4 * s, y - 12 * s, 14 * s, 14 * s, "#6e4a30", rx=5 * s),
         ell(x, y - 26 * s, 20 * s, 18 * s, "#d9b88a")]
    return "".join(o)


def giraffe(x, y, s=1.0):
    o = [rect(x - 11 * s, y - 120 * s, 22 * s, 100 * s, "#e8c15a", rx=8 * s), ell(x, y - 24 * s, 32 * s, 22 * s, "#e8c15a"),
         ell(x + 4 * s, y - 132 * s, 22 * s, 16 * s, "#e8c15a"), ell(x + 18 * s, y - 128 * s, 12 * s, 9 * s, "#f0d88a"),
         rect(x - 8 * s, y - 154 * s, 4 * s, 14 * s, "#a9783a") + circ(x - 6 * s, y - 155 * s, 3.5 * s, "#a9783a"),
         rect(x + 6 * s, y - 154 * s, 4 * s, 14 * s, "#a9783a") + circ(x + 8 * s, y - 155 * s, 3.5 * s, "#a9783a"),
         circ(x + 2 * s, y - 135 * s, 2.6 * s, C["ink"])]
    for dx, dy, r_ in ((-4, -100, 5), (4, -80, 5), (-3, -60, 4), (-18, -26, 6), (10, -32, 6), (22, -22, 4), (0, -42, 4)):
        o.append(circ(x + dx * s, y + dy * s, r_ * s, "#a9783a"))
    o.append(rect(x - 20 * s, y - 8 * s, 8 * s, 10 * s, "#a9783a") + rect(x + 14 * s, y - 8 * s, 8 * s, 10 * s, "#a9783a"))
    return "".join(o)


def companero_1():
    b = office_bg()
    b.append(office_window(40, 50, 170, 150) + office_window(430, 50, 170, 150))
    b.append(cloud(250, 60, .6, "#fffdf8"))
    # chatty group on the left/back
    b.append(person(90, 360, h=215, show_legs=False, look=1, mood="open", arms=((130, 268), (50, 270)), **COL2))
    b.append(desk(20, 296, 150, laptop=True))
    b.append(person(246, 360, h=215, show_legs=False, look=-1, mood="smile", arms=((210, 268), (286, 270)), **COL1))
    b.append(desk(175, 296, 150, laptop=True, plant=True))
    # boss
    b.append(person(540, 392, h=240, look=-1, mood="smile", arms=((500, 280), (586, 210)), **JEFE))
    # Daniel alone, shy, at his own desk
    b.append(person(395, 366, h=225, show_legs=False, look=0, mood="flat", arms=((372, 292), (420, 292)), **DANIEL))
    b.append(desk(320, 300, 160, laptop=True))
    b.append(rect(336, 292, 30, 6, "#00000000"))
    return wrap(b)


def companero_2():
    b = office_bg()
    b.append(office_window(450, 40, 150, 130))
    b.append(rect(30, 70, 150, 100, "#f6f1e4", rx=3, extra='stroke="#cfd5d6" stroke-width="3"') + circ(55, 94, 7, C["mustard"]) + circ(80, 94, 7, C["pink"]) + circ(105, 94, 7, C["sage"]))
    b.append(person(200, 372, h=235, show_legs=False, look=1, mood="smile", arms=((238, 290), (300, 270)), **NARR))
    b.append(person(430, 372, h=235, show_legs=False, look=-1, mood="smile", arms=((400, 296), (360, 290)), **DANIEL))
    b.append(rect(130, 306, 420, 14, "#c99a5b", rx=4) + rect(150, 320, 10, 80, "#a98466") + rect(520, 320, 10, 80, "#a98466"))
    # open sketchbook with drawings
    b.append(rect(252, 244, 176, 74, "#fffdf8", rx=3, extra='stroke="#cfd5d6" stroke-width="2"') + rect(338, 244, 4, 74, "#cfd5d6") + rect(248, 318, 184, 6, C["brown"], rx=2))
    k = f'stroke="{C["ink"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
    b.append(path("M270,298 q-2,-24 16,-26 l4,-8 l6,8 l6,-8 l4,8 q18,2 14,26 z", "#c9783a", k))
    b.append(path("M356,300 v-34 h22 v34 M388,300 v-48 h26 v48 M352,300 h66", "none", k))
    b.append(rect(366, 274, 6, 6, C["mustard"]) + rect(396, 262, 6, 6, C["mustard"]) + rect(396, 280, 6, 6, C["mustard"]))
    b.append(circ(276, 284, 2, C["ink"]) + circ(298, 284, 2, C["ink"]))
    b.append(path("M60,200 l0,0", "none"))
    b.append(rect(484, 296, 24, 10, C["mustard"], rx=2) + circ(300, 270, 0, C["ink"]))
    b.append(mug(120, 306, 26, C["terra"]))
    return wrap(b)


def companero_3():
    b = office_bg()
    # big poster on wall
    b.append(rect(190, 24, 270, 250, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(200, 34, 250, 230, "#f9ecc4"))
    b.append(ell(325, 262, 110, 6, "#00000012"))
    b.append(bear(270, 252, 1.5))
    b.append(giraffe(372, 252, 1.0))
    b.append(circ(432, 70, 14, "#f0c75e") + circ(220, 70, 8, "#e7a9a0", 'opacity=".7"'))
    b.append(rect(176, 20, 14, 14, C["red"], rx=7) + rect(448, 20, 14, 14, C["red"], rx=7))
    # people laughing
    b.append(person(95, 394, h=240, look=1, mood="open", arms=((50, 290), (140, 220)), **COL2))
    b.append(person(590, 394, h=240, look=-1, mood="open", arms=((548, 220), (632, 290)), **JEFE))
    b.append(person(170, 396, h=225, look=1, mood="open", arms=((140, 290), (205, 290)), **COL1))
    b.append(person(490, 396, h=230, look=-1, mood="open", arms=((460, 290), (525, 290)), **NARR))
    b.append(person(325, 398, h=235, look=0, mood="smile", arms=((290, 292), (360, 236)), **DANIEL))
    return wrap(b)


SCENES = {"es-el-nuevo-companero-1": companero_1, "es-el-nuevo-companero-2": companero_2, "es-el-nuevo-companero-3": companero_3}
