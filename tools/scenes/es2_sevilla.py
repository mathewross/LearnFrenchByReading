import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

LUCAS = dict(coat=C["teal"], hair="#3a2e28", style="short", pants="#8a7a5a")
PILAR = dict(coat=C["terra"], hair="#cfcfcf", style="bun", pants=C["plum"], cheeks=True, scarf=C["mustard"])
HOMBRE = dict(coat="#8a8f5a", hair="#e0e0e0", style="short", pants=C["dgrey"], skin=C["skin2"])


def train_side(x, base, w, h, color):
    o = [rect(x, base - h, w, h - 12, color, rx=14), rect(x, base - h * .38, w, 8, "#fffdf8", extra='opacity=".85"'), rect(x, base - 16, w, 10, C["dgrey"])]
    xx = x + 14
    while xx + 56 < x + w:
        o.append(rect(xx, base - h + 16, 56, h * .42, "#cfe3e6", rx=6))
        xx += 72
    for wx in range(int(x + 40), int(x + w - 30), 110):
        o.append(circ(wx, base - 6, 11, C["ink"]) + circ(wx, base - 6, 4, C["lgrey"]))
    return "".join(o)


def olive_tree(x, base, s=60):
    return (rect(x - 3, base - s * .45, 6, s * .45, C["brown"]) + ell(x, base - s * .65, s * .42, s * .3, "#7e9a78") + ell(x - s * .18, base - s * .75, s * .24, s * .18, "#9db591"))


def balcony(x, y, w, flowers=True):
    o = [rect(x, y, w, 7, "#3a3f45"), rect(x, y + 7, w, 22, "none", extra='stroke="#3a3f45" stroke-width="2"')]
    for k in range(1, 6):
        o.append(rect(x + k * w / 6 - 1, y + 7, 2, 22, "#3a3f45"))
    if flowers:
        for k in range(5):
            o.append(circ(x + 10 + k * (w - 20) / 4, y - 3, 7, C["pink"] if k % 2 else C["red"]) + circ(x + 10 + k * (w - 20) / 4, y + 4, 5, "#5f8a66"))
    return "".join(o)


def sevilla_1():
    b = [rect(0, 0, W, H, "#cfe3e6"), sun(540, 60, 26), cloud(120, 64, .9), cloud(330, 40, .7)]
    # station hall back wall + arch roof
    b.append(rect(0, 120, W, 160, "#e6dcc3"))
    for k in range(5):
        b.append(rect(30 + k * 130, 130, 70, 120, "#cfe3e6", rx=30) + rect(30 + k * 130, 190, 70, 60, "#cfe3e6"))
    b.append(rect(0, 100, W, 26, C["deep"]))
    b.append(circ(320, 66, 36, C["white"], f'stroke="{C["deep"]}" stroke-width="8"') + line(320, 66, 320, 40, C["ink"], 4) + line(320, 66, 340, 66, C["ink"], 4) + circ(320, 66, 4, C["ink"]))
    b.append(train_side(300, 292, 380, 150, C["sage_d"]))
    b += [rect(0, 292, W, 108, "#d9cfb8"), rect(0, 292, W, 10, "#bfb396"), rect(0, 330, W, 6, C["mustard"])]
    # bench + other travellers
    b.append(person(110, 360, h=190, show_legs=False, coat=C["plum"], hair="#2b2622", style="bun", look=1, cheeks=True))
    b.append(rect(40, 318, 140, 10, "#a98466", rx=3) + rect(50, 328, 8, 36, "#a98466") + rect(162, 328, 8, 36, "#a98466") + rect(40, 262, 140, 8, "#a98466", rx=3))
    b.append(suitcase(420, 394, 70, 100, C["red"]))
    b.append(person(310, 396, h=250, mood="smile", look=1, arms=((276, 290), (360, 300)), **LUCAS))
    b.append(mug(276, 296, 24, C["white"]))
    b.append(circ(276, 290, 6, C["skin"]))
    b.append(rect(480, 316, 70, 78, C["navy"], rx=8) + rect(492, 300, 46, 20, "none", rx=8, extra=f'stroke="{C["ink"]}" stroke-width="4"'))
    return wrap(b)


def sevilla_2():
    b = [rect(0, 0, W, H, "#efe3c9"), rect(0, 322, W, 78, "#8c9296")]
    # big window with landscape
    wx, wy, ww, wh = 150, 40, 360, 220
    b.append(f'<clipPath id="tw"><rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="10"/></clipPath>')
    b.append(rect(wx - 12, wy - 12, ww + 24, wh + 24, "#b9735a", rx=16))
    b.append('<g clip-path="url(#tw)">' + rect(wx, wy, ww, wh, "#cfe8ee") + sun(450, 90, 22) + cloud(220, 84, .8))
    b.append(ell(260, 220, 260, 70, "#d9c98a") + ell(480, 240, 220, 60, "#c9b66f") + rect(wx, 230, ww, 40, "#b9a45e"))
    for hx, hy_ in ((200, 200), (252, 190), (300, 205)):
        b.append(rect(hx, hy_, 34, 26, "#fffdf8") + poly([(hx - 3, hy_), (hx + 37, hy_), (hx + 28, hy_ - 12), (hx + 6, hy_ - 12)], C["terra"]) + rect(hx + 12, hy_ + 8, 10, 18, C["brown"]))
    b.append(rect(404, 160, 24, 56, "#fffdf8") + poly([(402, 160), (430, 160), (416, 140)], C["terra"]))
    for r_, yy in ((0, 232), (1, 250), (2, 268)):
        for k in range(9):
            b.append(olive_tree(wx + 20 + k * 42 + (r_ % 2) * 20, yy + 10, 36 + r_ * 8))
    b.append("</g>")
    b.append(rect(wx + ww / 2 - 4, wy, 8, wh, "#b9735a", extra='opacity="0"'))
    b.append(rect(wx, wy + wh, ww, 14, "#a98466") + rect(wx - 12, wy + wh, ww + 24, 4, "#8d6a4f"))
    # seats
    b.append(rect(60, 250, 520, 110, C["teal"], rx=16) + rect(60, 340, 520, 40, C["deep"], rx=10))
    # Pilar left talking, Lucas right
    b.append(person(250, 345, h=215, show_legs=False, look=1, mood="open", arms=((200, 292), (332, 244)), **PILAR))
    b.append(person(400, 345, h=215, show_legs=False, look=-1, mood="smile", arms=((370, 300), (440, 300)), **LUCAS))
    b.append(rect(60, 300, 520, 12, "#000000", extra='opacity="0"'))
    b.append(rect(412, 306, 76, 24, "#e0c9a0", rx=11) + rect(418, 310, 64, 6, "#8a9a5a", rx=3) + rect(420, 318, 60, 4, "#cf4a3b", rx=2))
    b.append(circ(434, 306, 7, C["skin"]) + circ(466, 306, 7, C["skin"]))
    b.append(suitcase(560, 396, 64, 90, C["red"]))
    b.append(ell(320, 362, 270, 10, "#00000014"))
    return wrap(b)


def sevilla_3():
    b = [rect(0, 0, W, H, "#bfe2ec"), sun(70, 64, 30, "#f6d46a")]
    # Giralda-like tower
    tx = 470
    b.append(rect(tx - 44, 40, 88, 270, "#d9b878") + rect(tx - 44, 40, 88, 270, "none", extra='stroke="#c4a05f" stroke-width="2"'))
    for k in range(6):
        b.append(rect(tx - 30, 90 + k * 36, 16, 22, "#8a6a4a", rx=8) + rect(tx + 14, 90 + k * 36, 16, 22, "#8a6a4a", rx=8))
    b.append(rect(tx - 36, 28, 72, 18, "#c4a05f") + rect(tx - 26, 4, 52, 26, "#d9b878") + poly([(tx - 18, 6), (tx + 18, 6), (tx, -12)], C["terra"]) + circ(tx, -14, 5, C["mustard"]))
    # white buildings with balconies both sides
    b.append(rect(0, 80, 260, 240, "#f6f1e4") + rect(0, 80, 260, 14, C["terra"]))
    for k in range(2):
        for r_ in range(2):
            wx_, wy_ = 24 + k * 118, 112 + r_ * 100
            b.append(rect(wx_, wy_, 62, 70, "#6f9aa0", rx=3) + rect(wx_ - 6, wy_ + 62, 74, 8, "#d9cfb8"))
            b.append(balcony(wx_ - 10, wy_ + 40, 82, flowers=True))
    b.append(rect(580, 110, 60, 210, "#f0dcc0"))
    b.append(rect(590, 130, 40, 60, "#6f9aa0", rx=3) + balcony(584, 170, 56, True))
    # street
    b.append(rect(0, 300, W, 100, "#e0c79a") + rect(0, 300, W, 8, "#cfb482"))
    b.append(poly([(150, 400), (470, 400), (400, 300), (210, 300)], "#d9b878", 'opacity=".5"'))
    # old man pointing
    b.append(person(520, 394, h=225, look=-1, mood="smile", arms=((486, 298), (440, 150)), **HOMBRE))
    b.append(person(250, 396, h=240, look=1, mood="open", arms=((212, 300), (320, 296)), **LUCAS))
    # suitcase held at left hand
    b.append(suitcase(200, 394, 66, 96, C["red"]))
    b.append(rect(188, 296, 48, 6, C["ink"], rx=3))
    # sweat drop + heat
    b.append(path("M286,152 q8,14 0,20 q-8,-6 0,-20 Z", "#7fb3c7"))
    return wrap(b)


SCENES = {"es-viaje-a-sevilla-1": sevilla_1, "es-viaje-a-sevilla-2": sevilla_2, "es-viaje-a-sevilla-3": sevilla_3}
