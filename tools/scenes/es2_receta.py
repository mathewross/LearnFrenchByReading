import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

ABUELA = dict(coat="#c9783a", hair="#d8d8d8", style="bun", pants=C["plum"], cheeks=True)
NIETA = dict(coat=C["teal"], hair="#5a3a2a", style="bob", pants="#6f8790", cheeks=True)
APRON = "#f6f1e4"


def kitchen_bg():
    b = [rect(0, 0, W, H, "#f3e7c9"), rect(0, 150, W, 150, "#e9d6a9")]
    for yy in range(150, 300, 30):
        b.append(line(0, yy, W, yy, "#f6efd9", 3))
    for xx in range(0, W, 30):
        b.append(line(xx, 150, xx, 300, "#f6efd9", 3))
    b.append(rect(0, 300, W, 100, "#b9735a") + rect(0, 296, W, 6, "#a15f49"))
    return b


def egg(x, y, r=9, col="#f4e7cf"):
    return ell(x, y, r * .82, r, col) + ell(x - r * .25, y - r * .3, r * .2, r * .3, "#fff", 'opacity=".5"')


def onion(x, y, r=14):
    return (ell(x, y, r, r * .9, "#c98a62") + poly([(x - 4, y - r * .8), (x + 4, y - r * .8), (x + 1, y - r * 1.5)], "#d9b78a") + path(f"M{n(x - r * .4)},{n(y - r * .7)} q-4,{r * .8} 0,{r * 1.5}", "none", 'stroke="#a9683a" stroke-width="1.6"')
            + path(f"M{n(x + r * .4)},{n(y - r * .7)} q4,{r * .8} 0,{r * 1.5}", "none", 'stroke="#a9683a" stroke-width="1.6"'))


def potato(x, y, r=13):
    return ell(x, y, r * 1.2, r * .85, "#c9a468") + circ(x - r * .4, y - r * .2, 1.8, "#9a7a44") + circ(x + r * .3, y + r * .2, 1.8, "#9a7a44")


def pan(x, y, rx=110, ry=26, fill="#3a3f45"):
    return (rect(x + rx - 6, y - 8, 120, 14, "#2a2f33", rx=7) + ell(x, y + 10, rx + 6, ry + 4, "#2a2f33") + ell(x, y, rx + 6, ry + 4, fill) + ell(x, y + 2, rx - 6, ry - 4, "#c9a345"))


def receta_1():
    b = kitchen_bg()
    # window with plants, shelf
    b.append(rect(60, 36, 130, 104, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(70, 46, 110, 84, "#cfe8ee") + rect(121, 46, 8, 84, "#fffdf8") + tree(150, 130, 70))
    b.append(rect(48, 134, 154, 10, C["brown"], rx=3) + rect(70, 112, 24, 22, C["terra"], rx=3) + circ(82, 106, 12, "#6a8f7b") + rect(150, 114, 22, 20, C["mustard"], rx=3) + circ(161, 108, 10, "#8fae9a"))
    b.append(rect(400, 36, 200, 8, C["brown"], rx=3))
    for k in range(4):
        b.append(rect(412 + k * 46, 12, 32, 28, [C["terra"], C["sage"], C["mustard"], C["pink"]][k], rx=5) + rect(418 + k * 46, 8, 20, 6, C["white"], rx=3))
    # counter
    b.append(rect(0, 290, W, 22, "#c99a5b") + rect(0, 312, W, 88, "#a98466"))
    for xx in (110, 330, 540):
        b.append(rect(xx, 322, 100, 66, "#8d6a4f", rx=5) + circ(xx + 50, 340, 4, "#e6c590"))
    # ingredients
    b.append(basket(230, 290, 86, 36, False) + "".join(potato(200 + k * 24, 266 - (k % 2) * 6) for k in range(4)))
    b.append(basket(340, 290, 70, 30, False) + egg(318, 268, 11) + egg(340, 266, 11) + egg(362, 268, 11) + egg(330, 252, 11) + egg(352, 252, 11))
    b.append(onion(430, 276, 15) + onion(458, 278, 14) + rect(484, 242, 28, 48, "#d9b84a", rx=8) + rect(492, 226, 12, 18, "#d9b84a", rx=3) + rect(487, 262, 22, 14, "#fffdf8", rx=2))
    b.append(rect(530, 266, 22, 24, C["white"], rx=4) + rect(526, 260, 30, 8, C["lgrey"], rx=3))
    # people
    b.append(person(100, 390, h=238, look=1, mood="smile", arms=((150, 276), (70, 268)), **ABUELA))
    b.append(rect(76, 204, 48, 76, APRON, rx=8))
    b.append(person(580, 392, h=215, look=-1, mood="smile", arms=((540, 270), (610, 290)), **NIETA))
    return wrap(b)


def receta_2():
    b = kitchen_bg()
    b.append(rect(0, 290, W, 110, "#a98466") + rect(0, 282, W, 12, "#c99a5b", rx=4))
    # stove with big pan
    b.append(rect(190, 270, 270, 30, "#cfd5d6", rx=4) + rect(200, 296, 250, 8, "#9aa3a6"))
    b.append(pan(320, 272, 100, 24))
    for k, (px, py) in enumerate(((282, 266), (310, 262), (340, 268), (368, 262), (300, 276), (352, 276))):
        b.append(potato(px, py, 9))
    b.append(ell(260, 264, 12, 8, "#f6f1e4", 'opacity=".9"') + ell(386, 266, 11, 7, "#f6f1e4", 'opacity=".9"'))
    # smoke
    for k, (sx, sy, r_) in enumerate(((320, 196, 22), (342, 160, 28), (310, 126, 32), (338, 86, 36))):
        b.append(circ(sx, sy, r_, "#c9ced0", 'opacity=".6"'))
    # salt shaker pouring
    b.append(rect(96, 120, 38, 56, "#e8f1f3", rx=8) + rect(98, 112, 34, 14, "#cfd5d6", rx=5) + circ(108, 118, 2, C["ink"]) + circ(122, 118, 2, C["ink"]))
    for k in range(10):
        b.append(circ(104 + k * 3, 190 + k * 8, 2, "#fffdf8"))
    # abuela right with tears, nieta left
    b.append(person(110, 392, h=240, look=1, mood="open", arms=((140, 190), (80, 300)), **NIETA))
    b.append(person(530, 392, h=240, look=-1, mood="open", arms=((490, 290), (572, 300)), **ABUELA))
    b.append(rect(506, 206, 48, 76, APRON, rx=8))
    for sx, sy in ((86, 177), (136, 177), (506, 163), (554, 163)):
        b.append(path(f"M{sx},{sy} q4,8 0,12 q-4,-4 0,-12 Z", "#7fb3c7"))
    b.append(ell(180, 280, 36, 8, "#00000010"))
    return wrap(b)


def receta_3():
    b = kitchen_bg()
    b.append(rect(60, 40, 120, 90, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(70, 50, 100, 70, "#cfe8ee"))
    b.append(rect(0, 300, W, 100, "#c9ae88"))
    b.append(person(120, 392, h=290, look=1, mood="open", show_legs=False, arms=((164, 230), (88, 246)), **NIETA))
    b.append(ell(176, 216, 40, 12, "#3a3f45") + rect(100, 210, 64, 12, "#2a2f33", rx=6) + ell(176, 222, 36, 8, "#c9a345"))
    b.append(person(540, 392, h=290, look=-1, mood="open", show_legs=False, arms=((496, 300), (584, 300)), **ABUELA))
    b.append(rect(512, 184, 56, 130, APRON, rx=8))
    # table in front
    b.append(rect(0, 312, W, 88, "#d9ae6b") + rect(0, 312, W, 8, "#e6c590") + rect(0, 372, W, 28, "#a98466"))
    b.append(ell(300, 346, 120, 22, "#f6f1e4") + ell(300, 342, 120, 22, C["white"]))
    b.append(path("M222,342 a78,19 0 0 1 156,0 a78,19 0 0 1 -156,0 Z", "none", 'stroke="#e6dcc3" stroke-width="2"'))
    b.append(path("M232,342 a68,17 0 0 1 68,-17 v34 a68,17 0 0 1 -68,-17 Z", "#e6c14f") + ell(262, 338, 12, 4, "#f2dc7a"))
    for px, py, r_ in ((470, 350, 16), (508, 342, 12), (440, 362, 10), (540, 356, 9)):
        b.append(ell(px, py, r_, r_ * .55, "#e6c14f") + ell(px - 2, py - 1, r_ * .5, r_ * .25, "#f2dc7a"))
    b.append(rect(560, 326, 40, 34, C["white"], rx=4, extra='opacity="0"'))
    for sx, sy in ((200, 150), (70, 150), (470, 130), (610, 150)):
        b.append(path(f"M{sx},{sy} q8,-12 16,0 M{sx - 4},{sy + 14} q8,-10 16,0", "none", f'stroke="{C["mustard"]}" stroke-width="3.5" stroke-linecap="round"'))
    return wrap(b)


SCENES = {"es-la-receta-de-la-abuela-1": receta_1, "es-la-receta-de-la-abuela-2": receta_2, "es-la-receta-de-la-abuela-3": receta_3}
