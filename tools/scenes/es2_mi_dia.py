import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

PABLO = dict(coat=C["teal"], hair="#3a2e28", style="short", pants=C["navy"])
MADRE = dict(coat=C["terra"], hair="#5a3a2a", style="bun", pants=C["plum"], cheeks=True)
HERMANA = dict(coat=C["pink"], hair="#2b2622", style="bob", pants="#6f8790", cheeks=True)
PROFE = dict(coat=C["plum"], hair="#4a3a32", style="bun", pants=C["navy"], cheeks=True)


def wall_clock(x, y, r=30, hh=7, mh=0):
    o = [circ(x, y, r, C["white"], f'stroke="{C["brown"]}" stroke-width="5"')]
    for k in range(12):
        a = k * math.pi / 6
        o.append(line(x + math.sin(a) * (r - 7), y - math.cos(a) * (r - 7), x + math.sin(a) * (r - 3), y - math.cos(a) * (r - 3), C["ink"], 2))
    ah = (hh % 12) * math.pi / 6
    o.append(line(x, y, x + math.sin(ah) * r * .5, y - math.cos(ah) * r * .5, C["ink"], 4))
    am = mh * math.pi / 30
    o.append(line(x, y, x + math.sin(am) * r * .75, y - math.cos(am) * r * .75, C["ink"], 3))
    return "".join(o) + circ(x, y, 3, C["ink"])


def rooster(x, y, s=1.0, d=1):
    """Cartoon rooster standing, feet at (x, y), faces right when d=1."""
    o = []
    for k, c in enumerate(("#c24a3f", "#2f7f8a", "#d9ab4a", "#6a8f7b")):
        o.append(ell(x - d * 30 * s, y - (44 + k * 4) * s, 10 * s, 28 * s, c, f'transform="rotate({d * (-50 + k * 22)} {n(x - d * 28 * s)} {n(y - 40 * s)})"'))
    o.append(ell(x, y - 38 * s, 30 * s, 24 * s, "#c9783a"))
    o.append(ell(x - d * 4 * s, y - 34 * s, 18 * s, 12 * s, "#e0a05a"))
    o.append(rect(x - 6 * s, y - 16 * s, 4 * s, 16 * s, "#d9a33a") + rect(x + 6 * s, y - 16 * s, 4 * s, 16 * s, "#d9a33a"))
    o.append(rect(x + d * 12 * s - 5 * s, y - 80 * s, 10 * s, 30 * s, "#c9783a"))
    o.append(circ(x + d * 17 * s, y - 74 * s, 14 * s, "#c9783a"))
    for k in range(3):
        o.append(circ(x + d * (10 + k * 7) * s, y - 91 * s + (k % 2) * 3 * s, 6 * s, C["red"]))
    o.append(poly([(x + d * 28 * s, y - 78 * s), (x + d * 44 * s, y - 72 * s), (x + d * 28 * s, y - 68 * s)], C["yellow"]))
    o.append(poly([(x + d * 27 * s, y - 67 * s), (x + d * 32 * s, y - 67 * s), (x + d * 29 * s, y - 56 * s)], C["red"]))
    o.append(circ(x + d * 22 * s, y - 76 * s, 2.6 * s, C["ink"]))
    return "<g>" + "".join(o) + "</g>"


def mi_dia_1():
    b = [rect(0, 0, W, H, "#f1e4c8"), rect(0, 290, W, 110, "#c9ae88"), rect(0, 282, W, 8, "#b49670")]
    b.append(rect(60, 50, 170, 130, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(72, 62, 146, 106, "#f9e5a8") + sun(145, 115, 22, "#f0c75e")
             + rect(141, 62, 8, 106, "#fffdf8"))
    b.append(wall_clock(330, 80, 34, 7, 0))
    b += [rect(420, 40, 190, 10, C["brown"], rx=3)] + [mug(450 + k * 46, 40, 26, c, steam=False) for k, c in enumerate((C["terra"], C["sage"], C["mustard"], C["pink"]))]
    # table
    b.append(rect(120, 278, 400, 14, "#a98466", rx=5) + rect(138, 290, 10, 100, "#a98466") + rect(492, 290, 10, 100, "#a98466"))
    b.append(person(170, 340, h=215, show_legs=False, look=1, mood="smile", arms=((205, 262), (140, 250)), **MADRE))
    b.append(person(320, 346, h=220, show_legs=False, look=1, mood="smile", arms=((290, 272), (375, 268)), **PABLO))
    b.append(person(470, 342, h=190, show_legs=False, look=-1, mood="smile", arms=((430, 268), (510, 250)), **HERMANA))
    b.append(rect(112, 296, 416, 10, "#c99a5b", rx=4) + rect(112, 280, 416, 18, "#c99a5b", rx=5))
    # breakfast on table
    b.append(mug(384, 278, 30) + ell(250, 276, 38, 7, "#efe9d8") + rect(228, 262, 44, 14, "#d9a357", rx=5) + circ(238, 262, 5, "#cf4a3b") + circ(254, 262, 5, "#cf4a3b") + circ(268, 262, 5, "#cf4a3b"))
    b.append(tomato(440, 268, 12) + tomato(470, 270, 12) + basket(530, 280, 52, 28, False))
    return wrap(b)


def mi_dia_2():
    b = [rect(0, 0, W, H, "#e8e0cc"), rect(0, 300, W, 100, "#c9ae88"), rect(0, 292, W, 8, "#b49670")]
    # blackboard with chalk animals
    b.append(rect(120, 30, 400, 170, "#6b4a3a", rx=6) + rect(130, 40, 380, 150, "#3f5a52", rx=4))
    ch = 'stroke="#f6f1e4" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"'
    b.append(path("M170,150 q10,-34 40,-26 q22,-18 38,2 q16,8 6,30 z M182,150 l0,22 M236,152 l0,22 M200,126 l-6,-14 l14,6", "none", ch))
    b.append(path("M300,160 q-6,-40 24,-48 q-8,-10 8,-12 l10,8 q18,20 -6,52 z M312,160 l-4,18 M338,160 l4,18", "none", ch))
    b.append(path("M420,158 q10,-28 36,-20 q4,-18 18,-14 q-2,10 8,18 q-6,18 -24,22 z M430,160 l-2,16 M462,160 l2,16", "none", ch))
    # profesora
    b.append(person(90, 340, h=250, look=1, mood="smile", arms=((130, 192), (50, 270)), **PROFE))
    # desks and students (back row)
    for sx, sc, hr_, lk in ((196, C["sage_d"], "#6b4a3a", 1), (292, C["terra"], "#2b2622", 1), (540, C["mustard"], "#3a2e28", -1)):
        b.append(person(sx, 392, h=190, show_legs=False, look=lk, mood="open", cheeks=True, coat=sc, hair=hr_, style="short", arms=((sx - 30, 330), (sx + 30, 330))))
        b.append(rect(sx - 58, 316, 116, 12, "#c99a5b", rx=4) + rect(sx - 50, 328, 8, 72, "#a98466") + rect(sx + 42, 328, 8, 72, "#a98466"))
    # Pablo front-centre with the rooster phone
    b.append(person(420, 398, h=230, show_legs=False, look=-1, mood="open", cheeks=True, arms=((388, 300), (466, 208)), **PABLO))
    b.append(rect(350, 322, 150, 14, "#c99a5b", rx=5) + rect(360, 336, 9, 64, "#a98466") + rect(482, 336, 9, 64, "#a98466"))
    b.append(rect(300, 336, 36, 6, C["red"], rx=2))
    b.append(rect(446, 176, 52, 90, C["ink"], rx=8) + rect(451, 184, 42, 74, "#f9e5a8", rx=4) + rooster(472, 252, .42))
    b.append(circ(466, 208, 8, C["skin"]))
    for r_ in (22, 36):
        b.append(path(f"M{498 + r_},{176 + 20} q{r_ * .5},{r_ * .6} 0,{r_ * 1.2}", "none", f'stroke="{C["red"]}" stroke-width="4" stroke-linecap="round"'))
    return wrap(b)


SCENES = {"es-mi-dia-1": mi_dia_1, "es-mi-dia-2": mi_dia_2}
