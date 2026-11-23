import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *


def keys(x, y, s=1.0):
    return ("<g>" + circ(x, y, 11 * s, "none", f'stroke="{C["mustard"]}" stroke-width="{n(5 * s)}"') + rect(x + 8 * s, y - 3 * s, 32 * s, 6 * s, C["mustard"], rx=2)
            + rect(x + 30 * s, y + 2 * s, 5 * s, 10 * s, C["mustard"]) + rect(x + 38 * s, y + 2 * s, 5 * s, 8 * s, C["mustard"]) + "</g>")


def flat():
    b = [rect(0, 0, W, H, "#8a9a9d")]
    top, fl = 40, 330
    rooms = [(14, 214, "#8fb4d4"), (214, 426, "#f1e3a8"), (426, 626, "#a9cfa8")]
    for a, z, col in rooms:
        b.append(rect(a, top, z - a, fl - top, col))
        b.append(rect(a, fl, z - a, 40, "#c9ae88"))
    for a in (214, 426):
        b.append(rect(a - 4, top, 8, 330 - top + 40, "#6b7478"))
    b.append(rect(8, 28, 624, 14, "#5c6568") + rect(8, 28, 8, 342, "#5c6568") + rect(624, 28, 8, 342, "#5c6568") + rect(8, 366, 624, 8, "#5c6568"))
    # living room: sofa, tv, table
    b.append(rect(30, 250, 130, 80, "#7f8a93", rx=10) + rect(30, 236, 130, 28, "#6b7680", rx=10) + rect(22, 252, 18, 78, "#6b7680", rx=7) + rect(150, 252, 18, 78, "#6b7680", rx=7))
    b.append(rect(60, 100, 96, 60, "#2b3340", rx=5) + rect(66, 106, 84, 48, "#7fb3c7", rx=3))
    # kitchen: fridge, table, small window
    b.append(rect(236, 160, 38, 38, "#fffdf8") + rect(240, 164, 30, 30, "#cfe8ee"))
    b.append(rect(370, 130, 44, 200, "#fffdf8", rx=6) + rect(370, 200, 44, 5, "#c9c9c0") + rect(404, 160, 4, 26, C["grey"]) + rect(404, 216, 4, 40, C["grey"]))
    b.append(rect(290, 280, 66, 8, "#7a5c47") + rect(298, 288, 6, 42, "#7a5c47") + rect(342, 288, 6, 42, "#7a5c47"))
    # bedroom: bed, window, lamp
    b.append(rect(476, 82, 90, 90, "#fffdf8") + rect(484, 90, 74, 74, C["sky"]) + rect(517, 90, 8, 74, "#fffdf8"))
    b.append(rect(444, 250, 130, 80, C["terra"], rx=8) + rect(444, 226, 24, 104, "#7a5c47", rx=6) + rect(468, 242, 36, 18, C["white"], rx=8))
    b.append(rect(588, 270, 32, 60, C["brown"]) + rect(600, 232, 6, 40, C["dgrey"]) + poly([(588, 236), (618, 236), (610, 210), (596, 210)], C["mustard"]))
    return b


def flat_1():
    b = flat()
    b.append(person(214, 330, h=215, coat=C["white"], hair="#3a2e28", style="short", mood="flat", arms=(None, (232, 218)), look=1))
    return wrap(b)


def flat_2():
    b = [rect(0, 0, W, H, "#f1e3a8"), rect(0, 330, W, 70, "#d8cdb0"), rect(0, 322, W, 8, "#c4b88f")]
    b.append(rect(480, 80, 120, 110, "#fffdf8", rx=4) + rect(490, 90, 100, 90, C["sky"]) + rect(535, 90, 8, 90, "#fffdf8"))
    # fridge open
    b.append(rect(120, 40, 190, 292, "#e8efee", rx=10))
    b.append(rect(132, 54, 166, 264, "#f7fbfb", rx=6))
    for yy in (130, 210, 276):
        b.append(rect(132, yy, 166, 7, "#bfe0ea"))
    # milk
    b.append(rect(144, 66, 38, 64, C["white"], rx=3, extra=f'stroke="{C["lgrey"]}" stroke-width="2"') + poly([(144, 66), (182, 66), (172, 52), (154, 52)], "#4a77a8") + rect(144, 84, 38, 20, "#4a77a8"))
    b.append(circ(214, 118, 12, C["red"]) + circ(236, 120, 12, C["red"]) + circ(260, 118, 10, "#cfd36a"))
    b.append(ell(160, 198, 18, 11, "#f3e3b0") + ell(190, 200, 18, 11, "#f3e3b0") + ell(220, 198, 18, 11, "#f3e3b0"))
    # keys on the middle shelf, big
    b.append(keys(208, 180, 1.9))
    b.append(rect(150, 224, 60, 44, "#e7c1b7", rx=4) + rect(222, 232, 60, 36, "#cfd36a", rx=4))
    # door open to the left
    b.append(poly([(120, 40), (70, 66), (70, 300), (120, 332)], "#d5dedd"))
    b.append(rect(80, 150, 8, 50, C["grey"]))
    # Théo
    b.append(person(430, 392, h=250, coat="#7fa6c9", hair="#3a2e28", style="short", mood="open", cheeks=True, arms=((380, 270), (484, 168))))
    b.append(rect(476, 132, 26, 36, "#e6f3f6", rx=4, extra=f'stroke="#9cc3cc" stroke-width="2"') + rect(478, 146, 22, 20, C["white"]))
    return wrap(b)


SCENES = {"mon-appartement-1": flat_1, "mon-appartement-2": flat_2}
