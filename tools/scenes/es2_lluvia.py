import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

JULIA = dict(coat="#3d6b78", hair="#5a3a2a", style="bob", pants=C["navy"], cheeks=True)
ANTONIO = dict(coat="#8a7a5a", hair="#e0e0e0", style="short", pants="#4a5568", skin=C["skin2"])
CAMARERO = dict(coat=C["white"], hair="#2b2622", style="short", pants="#3a4250")
RED = "#c24a3f"


def brolly(x, y, w, color, pole=110):
    top = y - .55 * w
    d = (f"M{n(x - w / 2)},{n(y)} C{n(x - w / 2)},{n(y - .62 * w)} {n(x + w / 2)},{n(y - .62 * w)} {n(x + w / 2)},{n(y)} "
         f"A{n(w / 6)},{n(w / 6)} 0 0 1 {n(x + w / 6)},{n(y)} A{n(w / 6)},{n(w / 6)} 0 0 1 {n(x - w / 6)},{n(y)} "
         f"A{n(w / 6)},{n(w / 6)} 0 0 1 {n(x - w / 2)},{n(y)} Z")
    return (line(x, y - 8, x, y + pole, C["ink"], 4)
            + path(f"M{n(x)},{n(y + pole)} q0,12 -12,12", "none", f'stroke="{C["ink"]}" stroke-width="4" stroke-linecap="round"')
            + path(d, color) + path(f"M{n(x)},{n(top + 6)} L{n(x - w / 6)},{n(y)} M{n(x)},{n(top + 6)} L{n(x + w / 6)},{n(y)}", "none", 'stroke="#00000033" stroke-width="2"')
            + circ(x, top + 2, 4, C["ink"]))


def wet_street(base=290, shutter="#6f8f8a"):
    b = [rect(0, 0, W, H, "#b7c3c8")]
    cols = [("#d9b77a", shutter), ("#d99f90", shutter), ("#c98a62", "#7a8f98"), ("#e5d6b8", shutter)]
    x = -10
    for i, hgt in enumerate([200, 230, 180, 215, 190, 235, 200]):
        f, sh = cols[i % 4]
        b.append(building(x, base, 98, hgt, f, "#8fa4ab", cols=2, rows=int(hgt / 42), roof="#8a8f94", shutter=sh))
        x += 99
    b += [rect(0, base, W, 110, "#8e9aa0"), rect(0, base, W, 8, "#a3adb2")]
    for yy, ww, xx in ((330, 220, 60), (362, 300, 250), (388, 160, 20), (342, 120, 470)):
        b.append(rect(xx, yy, ww, 4, "#a6b2b7", rx=2))
    return b


def lluvia_1():
    b = wet_street()
    # bus stop far right
    b += [rect(556, 170, 8, 180, C["grey"]), circ(560, 170, 24, C["deep"]), rect(549, 160, 22, 16, C["white"], rx=4), circ(553, 180, 3, C["white"]), circ(567, 180, 3, C["white"]),
          rect(520, 318, 82, 8, "#a98466", rx=3)]
    # Julia with red umbrella and gift bag
    b.append(person(280, 394, h=236, mood="smile", look=1, legs=((252, 394), (306, 386)), arms=((238, 292), (326, 252)), **JULIA))
    b.append(rect(210, 288, 40, 46, C["mustard"], rx=4) + path("M220,288 q10,-18 20,0", "none", f'stroke="{C["brown"]}" stroke-width="3.5"') + rect(214, 306, 32, 5, C["red"]))
    b.append(circ(238, 292, 6, C["skin"]))
    b.append(brolly(326, 104, 230, RED, 148))
    b.append(ell(280, 398, 80, 7, "#a6b2b7") + ell(430, 372, 60, 6, "#a6b2b7"))
    b.append(rain(0, W, 0, 400, 80, seed=11, color="#5f7882", length=24))
    return wrap(b)


def lluvia_2():
    b = [rect(0, 0, W, H, "#efe0c0"), rect(0, 300, W, 100, "#b99d7a"), rect(0, 292, W, 8, "#a58863")]
    # counter at left with waiter
    b.append(person(110, 340, h=215, show_legs=False, look=1, mood="smile", arms=((160, 280), (70, 270)), **CAMARERO))
    b.append(rect(0, 280, 220, 14, "#c99a5b", rx=3) + rect(0, 294, 220, 106, "#8d6a4f") + rect(180, 238, 38, 42, "#cfd5d6", rx=5) + circ(199, 252, 6, C["dgrey"]))
    b.append(rect(14, 60, 200, 8, C["brown"], rx=3) + "".join(cup(34 + k * 40, 60, 24) for k in range(5)))
    b.append(circ(300, 70, 32, C["white"], f'stroke="{C["brown"]}" stroke-width="6"') + line(300, 70, 300, 48, C["ink"], 3) + line(300, 70, 316, 76, C["ink"], 3))
    # glass door with rain outside
    b.append(rect(400, 24, 220, 300, C["brown"], rx=6) + rect(412, 36, 196, 276, "#b7c3c8"))
    b.append('<clipPath id="dr"><rect x="412" y="36" width="196" height="276"/></clipPath><g clip-path="url(#dr)">')
    b.append(rect(420, 160, 70, 150, "#a9bcc0") + rect(520, 130, 80, 180, "#9fb1b8") + rain(412, 608, 36, 312, 22, seed=4, color="#5f7882", length=26) + "</g>")
    b.append(rect(506, 36, 8, 276, C["brown"]) + circ(490, 190, 6, C["mustard"]) + circ(530, 190, 6, C["mustard"]))
    # empty umbrella stand
    b.append(path("M350,330 l-6,64 h54 l-6,-64 Z", "#6b7478") + ell(374, 330, 24, 6, "#4a5558") + ell(374, 332, 18, 3, "#2a2f33"))
    # small table with the abandoned coffee and book
    b.append(ell(130, 392, 0, 0, "none"))
    b.append(person(260, 396, h=240, look=1, mood="open", arms=((214, 236), (318, 236)), **JULIA))
    b.append(rect(80, 322, 4, 4, "#000", extra='opacity="0"'))
    b.append(circ(340, 160, 4, "#c24a3f", 'opacity="0"'))
    b.append(rect(332, 322, 6, 6, "#000", extra='opacity="0"'))
    b.append(rect(12, 330, 90, 6, "#c99a5b", rx=3, extra='opacity="0"'))
    return wrap(b)


def lluvia_3():
    b = wet_street(300)
    b += [rect(30, 190, 8, 170, C["grey"]), circ(34, 190, 24, C["deep"]), rect(23, 180, 22, 16, C["white"], rx=4), circ(27, 200, 3, C["white"]), circ(41, 200, 3, C["white"])]
    # window boxes in the background
    b.append(rect(100, 150, 70, 14, C["terra"], rx=3) + "".join(circ(110 + k * 14, 146, 7, [C["red"], C["pink"], C["yellow"]][k % 3]) for k in range(5)))
    b.append(person(250, 396, h=232, mood="smile", look=1, legs=((226, 396), (276, 388)), arms=((214, 296), (286, 296)), **JULIA))
    b.append(person(380, 396, h=236, mood="open", look=-1, legs=((358, 388), (408, 396)), arms=((346, 296), (392, 244)), **ANTONIO))
    b.append(brolly(392, 112, 300, "#35595e", 136))
    b.append(circ(392, 244, 6, C["skin2"]))
    b.append(ell(432, 188, 16, 26, "#00000022", extra='opacity="0"'))
    b.append(rect(406, 204, 30, 44, "#2a4a50", rx=10, extra='opacity=".5"'))
    b.append(ell(300, 398, 90, 7, "#a6b2b7") + ell(500, 376, 70, 6, "#a6b2b7"))
    for fx, fy in ((520, 330), (546, 336), (572, 330)):
        b.append(rect(fx - 12, fy, 24, 22, C["terra"], rx=3) + flower(fx, fy - 20, [C["pink"], C["yellow"], C["red"]][(fx // 26) % 3]) + flower(fx + 6, fy - 12, C["pink"]))
    b.append(rain(0, W, 0, 400, 70, seed=21, color="#5f7882", length=24))
    return wrap(b)


SCENES = {"es-un-dia-de-lluvia-1": lluvia_1, "es-un-dia-de-lluvia-2": lluvia_2, "es-un-dia-de-lluvia-3": lluvia_3}
