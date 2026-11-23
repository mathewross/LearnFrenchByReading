import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *


def awning(x0, x1, y, h, c1, c2, stripes=8):
    o = []
    sw = (x1 - x0) / stripes
    for i in range(stripes):
        a = x0 + i * sw
        o.append(poly([(a + 6, y), (a + sw + 6, y), (a + sw, y + h), (a - 0, y + h)], c1 if i % 2 == 0 else c2))
    for i in range(stripes):
        a = x0 + i * sw
        o.append(path(f"M{n(a)},{n(y + h)} h{n(sw)} q{n(-sw / 2)},14 {n(-sw)},0 Z", c1 if i % 2 == 0 else c2))
    return "".join(o)


def crate(x, y, w, h, items):
    return rect(x, y, w, h, "#b98a5a", rx=3) + rect(x, y + h * .35, w, 4, "#9a6f45") + items


def apples_row(x, y, count, r=11, color=None):
    return "".join(apple(x + i * r * 1.9, y, r, color) for i in range(count))


def market_1():
    b = [rect(0, 0, W, H, "#f1e8d2"), rect(0, 262, W, 138, "#ddd0b2")]
    # trees and buildings behind
    b.append(tree(40, 250, 150))
    b.append(tree(600, 250, 150))
    for bx, bw, bh, f in [(110, 90, 120, "#e7d6b0"), (210, 70, 100, "#efe2c4"), (440, 90, 118, "#e5d3ae"), (540, 60, 100, "#efe2c4")]:
        b.append(building(bx, 250, bw, bh, f, "#9fb6bb", cols=2, rows=3, roof="#7f8c93"))
    # background stalls
    for sx, c1 in ((10, C["teal"]), (460, C["mustard"])):
        b.append(awning(sx, sx + 170, 150, 34, c1, C["cream"], 6))
        b.append(rect(sx + 8, 184, 6, 90, C["brown"]) + rect(sx + 156, 184, 6, 90, C["brown"]))
        b.append(rect(sx + 6, 250, 158, 38, C["brown"]))
    # people in the crowd
    b.append(person(165, 322, h=150, coat=C["plum"], hair="#2f2622", mood="flat"))
    b.append(person(468, 328, h=155, coat=C["terra"], hair="#cfcfcf", style="bun", mood="flat"))
    b.append(person(398, 318, h=140, coat=C["navy"], hair="#4a3a32", style="short", skin=C["skin2"], mood="flat"))
    # main stall
    b.append(awning(200, 440, 78, 52, C["red"], C["cream"], 8))
    b.append(rect(210, 130, 8, 170, C["brown"]) + rect(422, 130, 8, 170, C["brown"]))
    b.append(person(320, 300, h=215, coat="#6f8f6a", hair="#4a3a32", style="short", skin=C["skin2"], mood="smile", show_legs=False,
                    arms=((282, 262), (358, 262))))
    b.append(rect(200, 262, 240, 18, "#a98466"))
    b.append(rect(204, 280, 232, 120, C["brown"]))
    b.append(crate(222, 232, 92, 36, apples_row(232, 238, 4, 10)))
    b.append(crate(330, 232, 92, 36, "".join(pear(342 + i * 21, 240, 10) for i in range(4))))
    b.append(circ(222, 244, 10, C["red"]) + circ(420, 246, 9, "#cfd36a"))
    b.append(person(110, 398, h=250, coat=C["sage_d"], look=1, cheeks=True, arms=((74, 300), (176, 300))))
    return wrap(b)


def market_2():
    b = [rect(0, 0, W, H, "#f1e8d2")]
    b.append(awning(0, 640, 0, 84, C["red"], C["cream"], 10))
    b.append(rect(0, 100, W, 160, "#e7dcc0"))
    for sx in (90, 470):
        b.append(rect(sx, 120, 80, 100, "#f6f1e4", rx=6))
    b.append(rect(0, 262, W, 138, "#ddd0b2"))
    # seller
    b.append(person(330, 330, h=270, coat="#6f8f6a", hair="#4a3a32", style="short", skin=C["skin2"], mood="open", show_legs=False,
                    arms=((278, 255), (410, 235))))
    # counter
    b.append(rect(80, 268, 480, 22, "#a98466"))
    b.append(rect(90, 290, 460, 110, C["brown"]))
    b.append(crate(104, 236, 112, 40, apples_row(116, 244, 5, 10)))
    b.append(crate(470, 236, 82, 40, "".join(pear(484 + i * 20, 244, 10) for i in range(3))))
    b.append(rect(246, 214, 80, 60, "#efe5cd", rx=6) + path("M254,214 q4,-20 18,-20 q14,0 18,20", "none", 'stroke="#c9b88a" stroke-width="4"')
             + apple(272, 246, 11) + apple(296, 250, 11))
    # Léa
    b.append(person(130, 408, h=255, coat=C["sage_d"], mood="open", cheeks=True, look=1, arms=((96, 300), (200, 270))))
    # coins
    b.append(circ(430, 262, 7, C["mustard"], f'stroke="#b98a2e" stroke-width="2"') + circ(448, 264, 7, C["mustard"], f'stroke="#b98a2e" stroke-width="2"'))
    b.append(circ(410, 236, 9, C["skin2"]))
    return wrap(b)


SCENES = {"lea-3-1": market_1, "lea-3-2": market_2}
