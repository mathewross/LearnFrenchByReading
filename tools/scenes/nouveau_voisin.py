import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *


def stairwell():
    b = [rect(0, 0, W, H, "#e3d8c0"), rect(0, 0, W, 300, "#e9dfc7"), rect(0, 300, W, 100, "#b9b2a1"), rect(0, 292, W, 8, "#a39c8b")]
    b.append(rect(0, 0, W, 46, "#00000010"))
    b.append(rect(0, 200, W, 6, "#00000012"))
    # stairs going up on the left
    for i in range(6):
        b.append(rect(0, 300 - i * 38, 230 - i * 28, 38, "#cdbfa3" if i % 2 else "#d8cbb0") + rect(0, 300 - i * 38, 230 - i * 28, 5, "#b3a688"))
    b.append(poly([(0, 276), (0, 252), (190, 90), (190, 120)], "none") )
    b.append(line(250, 80, 250, 280, C["brown"], 5) + line(250, 82, 40, 232, C["brown"], 6) + line(210, 130, 210, 252, C["brown"], 4) + line(130, 170, 130, 246, C["brown"], 4))
    # doors
    b.append(rect(420, 70, 110, 230, C["terra"], rx=4) + rect(432, 84, 86, 100, C["terra_d"], rx=3) + circ(514, 200, 6, C["mustard"]))
    b.append(rect(560, 70, 90, 230, "#7f98a8", rx=4) + circ(572, 200, 5, C["mustard"]))
    b.append(rect(318, 60, 60, 80, C["white"], rx=3, extra=f'stroke="{C["brown"]}" stroke-width="5"') + rect(328, 70, 40, 60, "#e7c1b7"))
    # boxes
    b.append(box(350, 238, 90, 62) + box(358, 198, 74, 40, "#c79a62") + box(540, 252, 70, 48, "#d9ac76") + box(552, 218, 52, 34, "#c79a62"))
    return b


def voisin_1():
    b = stairwell()
    b.append(person(140, 262, h=195, coat=C["sage_d"], look=1, cheeks=True, arms=((106, 215), (184, 160))))
    b.append(person(480, 392, h=275, coat="#c98a62", hair="#2b2622", style="short", skin=C["skin2"], mood="smile", cheeks=False, arms=((436, 300), (540, 300))))
    b.append(box(430, 280, 120, 74, "#d2a46f") + rect(428, 288, 14, 12, C["skin2"], rx=5) + rect(538, 288, 14, 12, C["skin2"], rx=5))
    return wrap(b)


def voisin_2():
    b = [rect(0, 0, W, H, "#e9dfc7"), rect(0, 310, W, 90, "#c9ae88"), rect(0, 302, W, 8, "#b49670")]
    b.append(rect(420, 50, 160, 130, "#fffdf8", rx=6) + rect(432, 62, 136, 106, C["sky"]) + rect(496, 62, 8, 106, "#fffdf8") + rect(432, 112, 136, 8, "#fffdf8"))
    b.append(tree(540, 168, 70, leaf=C["sage_d"]))
    b.append(box(30, 244, 100, 70) + box(44, 206, 76, 40, "#c79a62") + box(560, 258, 70, 56, "#d9ac76"))
    b.append(person(190, 400, h=275, coat=C["sage_d"], look=1, cheeks=True, mood="smile", arms=((150, 312), (292, 262))))
    b.append(person(450, 400, h=275, coat="#c98a62", hair="#2b2622", style="short", skin=C["skin2"], mood="smile", look=-1, arms=((350, 262), (500, 312))))
    b.append(mug(292, 270, 28) + mug(350, 270, 28))
    b.append(circ(292, 262, 9, C["skin"]) + circ(350, 262, 9, C["skin2"]))
    b.append(rect(300, 330, 50, 0, "#0000"))
    return wrap(b)


SCENES = {"nouveau-voisin-1": voisin_1, "nouveau-voisin-2": voisin_2}
