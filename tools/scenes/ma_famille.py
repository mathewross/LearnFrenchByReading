import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *

POM = dict(fur="#f6f2ea", belly="#e6dcc3", fat=1.35)


def living():
    b = [rect(0, 0, W, H, "#efe3c9"), rect(0, 292, W, 108, "#c9ae88"), rect(0, 284, W, 8, "#b49670")]
    b.append(rect(60, 50, 100, 80, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(72, 62, 76, 56, C["sky"]))
    b.append(circ(110, 90, 12, C["mustard"]))
    b.append(rect(480, 56, 90, 70, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(492, 68, 66, 46, "#e7c1b7"))
    b.append(ell(320, 360, 280, 34, "#b9735a", 'opacity=".55"'))
    return b


def fam_1():
    b = living()
    b.append(person(120, 372, h=262, coat=C["white"], hair="#3a2e28", style="short", pants=C["navy"], cheeks=False, arms=(None, None)))
    b.append(person(235, 372, h=240, coat=C["plum"], hair="#6b4a3a", style="bob", cheeks=True))
    b.append(person(350, 372, h=185, coat="#6f8f6a", hair="#2b2622", style="short"))
    b.append(person(445, 372, h=150, coat=C["pink"], hair="#6b4a3a", style="bob", cheeks=True, pants="#6f8790"))
    b.append(cat(550, 372, 1.0, **POM))
    # dad's baker apron
    b.append(rect(96, 214, 48, 70, "#f3efe3", rx=6, extra=f'stroke="{C["lgrey"]}" stroke-width="2"'))
    return wrap(b)


def fam_2():
    b = living()
    # people behind the box
    b.append(person(110, 372, h=262, coat=C["white"], hair="#3a2e28", style="short", mood="open", arms=((72, 250), (150, 250))))
    b.append(person(210, 372, h=240, coat=C["plum"], hair="#6b4a3a", style="bob", mood="open", cheeks=True))
    b.append(person(445, 372, h=185, coat="#6f8f6a", hair="#2b2622", style="short", mood="open"))
    b.append(person(535, 372, h=150, coat=C["pink"], hair="#6b4a3a", style="bob", mood="open", cheeks=True, pants="#6f8790", arms=((505, 300), (560, 262))))
    # cat squeezed in the box
    b.append(cat(328, 330, 1.35, **POM))
    b.append(box(256, 292, 144, 80))
    b.append(poly([(256, 292), (232, 262), (262, 262), (284, 292)], "#bd8d57") + poly([(400, 292), (424, 262), (394, 262), (372, 292)], "#bd8d57"))
    return wrap(b)


SCENES = {"ma-famille-1": fam_1, "ma-famille-2": fam_2}
