import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *


def balcony(x, y, w, color="#35595e"):
    o = [rect(x, y, w, 5, color)]
    for k in range(int(w / 9) + 1):
        o.append(rect(x + k * 9, y - 18, 2.5, 18, color))
    o.append(rect(x, y - 19, w, 3, color))
    return "".join(o)


def facade(x, base, w, h, fill, shutter, cols=2, rows=4):
    o = [rect(x, base - h, w, h, fill), rect(x, base - h, w, 8, "#00000012")]
    cw = w / cols
    for r_ in range(rows):
        wy = base - h + 26 + r_ * (h - 40) / rows
        for c_ in range(cols):
            wx = x + c_ * cw + cw / 2 - 12
            o.append(rect(wx - 8, wy, 8, 36, shutter) + rect(wx + 24, wy, 8, 36, shutter) + rect(wx, wy, 24, 36, "#cfe3e6", rx=2))
            if r_ > 0:
                o.append(balcony(wx - 8, wy + 36, 40))
    return "".join(o)


def madrid_1():
    b = [rect(0, 0, W, H, "#f3e6c8"), sun(80, 70, 24), cloud(430, 60, .8)]
    b.append(facade(0, 330, 150, 270, "#e0b983", "#7a8f6f"))
    b.append(facade(150, 330, 130, 230, "#d99f90", "#4f7c82"))
    b.append(facade(360, 330, 150, 280, "#efe2c4", "#a15f49"))
    b.append(facade(510, 330, 140, 240, "#c98a62", "#6a8f7b"))
    b.append(rect(0, 330, W, 70, "#b9b2a1") + rect(0, 326, W, 8, "#a39c8b"))
    for xx in range(-20, W, 90):
        b.append(rect(xx, 360, 50, 6, "#a39c8b", extra='opacity=".6"'))
    b.append(rect(300, 150, 6, 180, C["ink"]) + circ(303, 146, 11, "#f6e49a", f'stroke="{C["ink"]}" stroke-width="3"'))
    b.append(suitcase(380, 392, 70, 100))
    b.append(person(300, 392, h=250, coat="#c24a3f", hair="#3a2e28", style="bun", mood="smile", cheeks=True, look=1, arms=((262, 300), (356, 300))))
    b.append(rect(262, 232, 34, 62, "#c24a3f", rx=8, extra='stroke="#9d3a31" stroke-width="3"') + rect(268, 262, 22, 14, "#9d3a31", rx=3))
    return wrap(b)


def madrid_2():
    b = [rect(0, 0, W, H, "#e9ddc0"), rect(0, 316, W, 84, "#b9735a"), rect(0, 308, W, 10, "#a15f49")]
    for xx in range(0, W, 64):
        b.append(rect(xx, 330, 32, 32, "#c4826a", extra='opacity=".5"'))
        b.append(rect(xx + 32, 362, 32, 32, "#c4826a", extra='opacity=".5"'))
    b.append(rect(440, 60, 150, 260, C["brown"], rx=4) + rect(452, 72, 126, 248, "#f6dc86"))
    b.append(rect(452, 72, 126, 248, "#fff0c0", extra='opacity=".6"') + rect(488, 72, 8, 248, "#e8cf7a"))
    b.append(rect(60, 70, 90, 120, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(70, 80, 70, 100, C["sky"]) + rect(100, 80, 8, 100, "#fffdf8"))
    b.append(suitcase(110, 392, 64, 92, C["red"]))
    b.append(person(210, 392, h=240, coat="#c24a3f", hair="#3a2e28", style="bun", mood="smile", look=1, cheeks=True, arms=((180, 296), (330, 290))))
    b.append(person(380, 392, h=236, coat=C["plum"], hair="#cfd5d6", style="bun", mood="smile", cheeks=True, look=-1, pants="#5c6568", arms=((350, 262), (415, 262))))
    b.append(cat(382, 286, .5, fur="#3a3f41", belly="#4a5053", eyes="#e8c547", look=-1, tail=False))
    return wrap(b)


def madrid_3():
    b = [rect(0, 0, W, H, "#efe3c9"), rect(0, 300, W, 100, "#c9ae88"), rect(0, 292, W, 8, "#b49670")]
    b.append(rect(210, 30, 220, 190, C["white"], rx=8) + rect(222, 42, 196, 166, "#cfe8ee"))
    for bx, bw, bh, f in [(224, 50, 80, "#d99f90"), (280, 40, 110, "#e0b983"), (326, 60, 70, "#efe2c4"), (392, 24, 100, "#c98a62")]:
        b.append(rect(bx, 208 - bh, bw, bh, f) + "".join(rect(bx + 8 + (k % 2) * 20, 208 - bh + 10 + (k // 2) * 26, 10, 14, "#9fb6bb") for k in range(6)))
    b.append(sun(380, 78, 14) + rect(318, 42, 8, 166, C["white"]) + rect(222, 120, 196, 8, C["white"]))
    b.append(rect(130, 300, 80, 40, C["terra"], rx=6) + rect(130, 300, 14, 8, C["terra_d"]))
    b.append(rect(60, 290, 110, 12, "#a98466", rx=3))
    b.append(rect(470, 250, 110, 12, "#a98466", rx=3) + rect(480, 262, 8, 70, "#a98466") + rect(562, 262, 8, 70, "#a98466"))
    b.append(cup(500, 250, 28) + cup(545, 250, 28) + ell(522, 246, 20, 5, "#e6c590"))
    b.append(rect(60, 300, 320, 70, C["terra"], rx=14) + rect(60, 340, 320, 30, C["terra_d"], rx=10))
    b.append(person(320, 404, h=250, coat="#c24a3f", hair="#3a2e28", style="bun", mood="smile", look=1, cheeks=True, show_legs=False, arms=((278, 290), (380, 280))))
    b.append(ell(110, 306, 40, 12, C["white"]) + ell(110, 303, 36, 9, "#f6f1e4"))
    b.append(cat(430, 340, .9, fur="#3a3f41", belly="#4a5053", eyes="#e8c547", look=-1))
    return wrap(b)


SCENES = {"es-ana-en-madrid-1": madrid_1, "es-ana-en-madrid-2": madrid_2, "es-ana-en-madrid-3": madrid_3}
