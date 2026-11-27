import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

TOBY = dict(fur="#8b5a3c", dark="#6b4a3a")


def fam_1():
    b = [rect(0, 0, W, H, C["sky"]), cloud(60, 60, .8), cloud(500, 80, .7), sun(570, 56, 20)]
    b += grass(300)
    b.append(rect(190, 96, 260, 206, "#e9ddc0") + poly([(170, 100), (320, 28), (470, 100)], C["terra"]))
    b.append(rect(276, 180, 76, 122, C["brown"], rx=4) + circ(338, 244, 4, "#e6c590"))
    for wx in (212, 380):
        b.append(rect(wx, 140, 52, 56, C["white"], rx=3) + rect(wx + 6, 146, 40, 44, C["sky"]) + rect(wx + 23, 146, 6, 44, C["white"]))
    b.append(tree(570, 330, 220))
    for fx in range(20, 160, 26):
        b.append(flower(fx, 324, [C["red"], C["yellow"], C["pink"]][(fx // 26) % 3]))
    b.append(person(110, 392, h=250, coat="#6f8f6a", hair="#2b2622", style="short", mood="smile"))
    b.append(person(205, 392, h=236, coat=C["plum"], hair="#6b4a3a", style="bun", mood="smile", cheeks=True))
    b.append(person(290, 392, h=150, coat=C["pink"], hair="#6b4a3a", style="bob", mood="smile", cheeks=True, pants="#6f8790"))
    b.append(person(365, 392, h=125, coat=C["mustard"], hair="#3a2e28", style="short", mood="open"))
    b.append(person(450, 392, h=226, coat="#8f9aa3", hair="#cfd5d6", style="short", mood="smile", pants="#5c6568"))
    b.append(dog(560, 392, 1.0, d=-1, **TOBY))
    return wrap(b)


def fam_2():
    b = [rect(0, 0, W, H, "#efe3c9"), rect(0, 300, W, 100, "#c9ae88"), rect(0, 292, W, 8, "#b49670")]
    b.append(rect(60, 50, 100, 80, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(72, 62, 76, 56, C["sky"]))
    b.append(rect(480, 56, 90, 70, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(492, 68, 66, 46, "#e7c1b7"))
    b.append(ell(320, 380, 270, 30, "#b9735a", 'opacity=".5"'))
    b.append(person(150, 392, h=246, coat="#6f8f6a", hair="#2b2622", style="short", mood="smile", arms=((190, 270), (160, 330))))
    b.append(person(250, 392, h=232, coat=C["plum"], hair="#6b4a3a", style="bun", mood="smile", cheeks=True, arms=((210, 300), (290, 270))))
    b.append(rect(300, 262, 150, 14, "#a98466", rx=3) + rect(312, 276, 10, 74, "#a98466") + rect(428, 276, 10, 74, "#a98466"))
    b.append(person(375, 392, h=170, coat=C["pink"], hair="#6b4a3a", style="bob", mood="open", cheeks=True, show_legs=True, arms=((345, 266), (405, 266))))
    b.append(rabbit(375, 262, 1.0))
    b.append(box(340, 228, 70, 40, "#d2a46f"))
    b.append(person(490, 392, h=130, coat=C["mustard"], hair="#3a2e28", style="short", mood="open", arms=((470, 280), (520, 290))))
    b.append(dog(570, 392, .8, d=-1, **TOBY))
    b.append(cat(90, 392, .8, fur="#3a3f41", belly="#4a5053", eyes="#e8c547", look=1))
    return wrap(b)


SCENES = {"es-mi-familia-1": fam_1, "es-mi-familia-2": fam_2}
