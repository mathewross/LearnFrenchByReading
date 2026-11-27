import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

HOST = dict(coat=C["teal"], hair="#3a2e28", style="short", pants=C["navy"])
MARTA = dict(coat=C["pink"], hair="#6b4a3a", style="bob", pants="#6f8790", cheeks=True)


def key(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({n(x)},{n(y)}) rotate({n(rot)}) scale({n(s)})">' + circ(0, 0, 9, C["mustard"], 'stroke="#b98a2e" stroke-width="2"') + circ(0, 0, 3, "#efe3c9")
            + rect(8, -2.5, 30, 5, C["mustard"]) + rect(30, 0, 5, 9, C["mustard"]) + rect(22, 0, 4, 7, C["mustard"]) + "</g>")


def casa_1():
    b = [rect(0, 0, W, H, "#efe3c9"), rect(0, 292, W, 108, "#c9ae88"), rect(0, 284, W, 8, "#b49670")]
    b.append(rect(300, 50, 150, 130, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(312, 62, 126, 106, C["sky"]) + rect(371, 62, 8, 106, "#fffdf8") + tree(410, 168, 90))
    b.append(rect(60, 60, 80, 100, "#fffdf8", extra='stroke="#a98466" stroke-width="5"') + rect(70, 70, 60, 80, "#e7c1b7"))
    b.append(ell(300, 372, 200, 24, "#b9735a", 'opacity=".5"'))
    b.append(rect(200, 232, 250, 80, "#4a82b8", rx=18) + rect(190, 250, 44, 62, "#3a6a9c", rx=12) + rect(416, 250, 44, 62, "#3a6a9c", rx=12) + rect(236, 224, 80, 36, "#6fa0d2", rx=12) + rect(330, 224, 80, 36, "#6fa0d2", rx=12))
    b.append(rect(480, 290, 90, 10, "#a98466", rx=3) + rect(490, 300, 8, 60, "#a98466") + rect(552, 300, 8, 60, "#a98466") + ell(525, 282, 22, 8, "#f6f1e4") + circ(525, 262, 12, C["pink"]) + rect(518, 270, 14, 14, C["terra"]))
    b.append(person(100, 392, h=250, arms=((60, 300), (160, 260)), look=1, mood="smile", **HOST))
    b.append(person(560, 392, h=240, arms=((520, 300), (595, 300)), look=-1, mood="smile", **MARTA))
    return wrap(b)


def casa_2():
    b = [rect(0, 0, W, H, "#f6f1e4"), rect(0, 300, W, 100, "#d8cdb0"), rect(0, 292, W, 8, "#e6dcc3")]
    for k in range(5):
        b.append(rect(20 + k * 126, 0, 2, 292, "#e9e3d2"))
    b.append(rect(40, 40, 180, 90, "#fffdf8", rx=6) + rect(54, 54, 76, 62, "#d6dad6") + rect(142, 54, 64, 62, "#d6dad6") + circ(120, 85, 4, C["grey"]))
    b.append(rect(240, 60, 150, 120, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(252, 72, 126, 96, C["sky"]) + rect(311, 72, 8, 96, "#fffdf8") + tree(350, 168, 70))
    b.append(rect(0, 200, 230, 14, "#ecd8b0") + rect(0, 214, 230, 86, "#fffdf8", extra='opacity="0"'))
    b.append(rect(420, 200, 200, 100, "#fffdf8", extra='stroke="#cfd5d6" stroke-width="3"') + rect(420, 200, 200, 14, "#e6dcc3"))
    b.append(rect(0, 214, 230, 86, "#f0ebdc", extra='stroke="#cfd5d6" stroke-width="2"'))
    # table, chairs
    for cx in (230, 390):
        b.append(rect(cx - 22, 300, 44, 8, C["brown"], rx=3) + rect(cx - 22, 256, 6, 44, C["brown"]) + rect(cx - 22, 256, 44, 8, C["brown"], rx=3))
    b.append(ell(310, 318, 150, 34, "#a98466") + ell(310, 310, 150, 34, "#c99a5b") + rect(300, 330, 20, 70, "#a98466"))
    b.append(baguette(280, 296, 78, -8, 13) + "".join(apple(330 + k * 22, 296, 10) for k in range(3)) + pear(402, 300, 10))
    b.append(basket(110, 290, 60, 38, False) + "".join(orange(86 + k * 22, 266, 10) for k in range(3)))
    b.append(person(90, 392, h=250, arms=((130, 270), (60, 300)), look=1, mood="smile", **HOST))
    b.append(person(530, 392, h=236, arms=((490, 300), (580, 290)), look=-1, mood="smile", **MARTA))
    b.append(ell(310, 372, 70, 10, "#00000012"))
    return wrap(b)


def casa_3():
    b = [rect(0, 0, W, H, "#d8cdb0"), rect(0, 330, W, 70, "#a98466")]
    b.append(rect(230, 20, 190, 320, "#6b4a3a", rx=6) + rect(244, 34, 162, 292, C["terra"]) + rect(260, 52, 130, 110, C["terra_d"], rx=4) + rect(260, 182, 130, 110, C["terra_d"], rx=4))
    b.append(circ(390, 200, 8, "#e6c590") + rect(380, 218, 18, 30, "#e6c590", rx=4))
    b.append(key(392, 250, 1.3, 70) + circ(386, 224, 5, "#b98a2e"))
    b.append(key(420, 244, 1.0, 30))
    b.append(rect(170, 340, 300, 14, "#c9ae88", rx=3))
    b.append(person(130, 394, h=250, arms=((100, 300), (230, 100)), look=1, mood="open", **HOST))
    b.append(path("M96,130 q-12,-6 -4,-20", "none", f'stroke="{C["ink"]}" stroke-width="3" stroke-linecap="round" opacity="0"'))
    b.append(person(520, 394, h=240, arms=((480, 300), (560, 90)), look=-1, mood="open", **MARTA))
    b.append(path("M170,86 q20,-16 40,0", "none", 'stroke="#fff" stroke-width="3" stroke-linecap="round" opacity="0"'))
    return wrap(b)


SCENES = {"es-mi-casa-1": casa_1, "es-mi-casa-2": casa_2, "es-mi-casa-3": casa_3}
