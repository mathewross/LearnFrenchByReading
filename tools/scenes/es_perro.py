import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

LUIS = dict(coat=C["teal"], hair="#3a2e28", style="short", pants=C["navy"])
NINA = dict(coat=C["pink"], hair="#6b4a3a", style="bob", pants="#6f8790")
TOBY = dict(fur="#8b5a3c", dark="#6b4a3a")


def park_bg(far=True):
    b = [rect(0, 0, W, H, C["sky"]), cloud(70, 60, .8), cloud(430, 90, .7)]
    b += grass(290)
    b.append(path("M0,400 Q260,320 640,350 L640,400 Z", "#e6dcc3"))
    return b


def ball(x, y, r=10):
    return circ(x, y, r, C["red"]) + path(f"M{n(x - r * .8)},{n(y - r * .3)} q{n(r * .8)},{n(r * .6)} {n(r * 1.6)},0", "none", 'stroke="#fff" stroke-width="1.8"')


def luis_1():
    b = park_bg()
    b.append(tree(70, 300, 230) + tree(580, 300, 210) + tree(520, 296, 130, leaf="#7fa88a"))
    for fx in (170, 200, 230, 410, 440, 470):
        b.append(flower(fx, 312, [C["red"], C["yellow"], C["pink"]][(fx // 30) % 3]))
    b.append(person(250, 392, h=250, arms=((222, 296), (320, 120)), look=1, mood="smile", **LUIS))
    b.append(ball(358, 80, 12) + path("M330,112 q10,-16 22,-26", "none", 'stroke="#9aa3a6" stroke-width="2" stroke-dasharray="4 5"'))
    b.append(dog(430, 392, 1.1, d=-1, mouth=True, **TOBY))
    return wrap(b)


def tree_big(x, base):
    o = [rect(x - 22, base - 190, 44, 190, C["brown"]), path(f"M{n(x)},{n(base - 130)} l60,-60", "none", 'stroke="#6b4a3a" stroke-width="14" stroke-linecap="round"'),
         circ(x, base - 250, 100, C["sage_d"]), circ(x - 70, base - 200, 70, C["sage_d"]), circ(x + 74, base - 206, 72, C["sage_d"]), circ(x - 20, base - 290, 54, C["sage"])]
    return "".join(o)


def luis_2():
    b = park_bg()
    b.append(tree(80, 300, 200) + tree(580, 300, 190))
    b.append(tree_big(330, 330))
    b.append(circ(340, 144, 0, "none"))
    b.append(cat(392, 176, .62, fur="#f6f2ea", belly="#e6dcc3", eyes="#7fb77e", look=-1) + circ(378, 108, 9, "#2f3b3d") + ell(402, 150, 10, 8, "#2f3b3d"))
    b.append(dog(330, 392, 1.0, d=1, mouth=True, **TOBY))
    b.append(person(160, 392, h=240, arms=((128, 290), (200, 130)), look=1, mood="open", **LUIS))
    b.append(person(500, 392, h=170, arms=((476, 300), (526, 240)), look=-1, mood="smile", cheeks=True, **NINA))
    b.append(ball(430, 384, 10))
    return wrap(b)


SCENES = {"es-el-perro-de-luis-1": luis_1, "es-el-perro-de-luis-2": luis_2}
