import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

LUCIA = dict(coat="#c9783a", hair="#3a2e28", style="bob", pants=C["navy"], cheeks=True, scarf=C["teal"])
CLERK = dict(coat=C["white"], hair="#3a2e28", style="short", pants="#4a5568")


def jacket(x, y, color, s=1.0):
    """Jacket on a hanger, hook at (x, y), about 70 px wide."""
    o = [path(f"M{n(x)},{n(y)} l0,{n(8 * s)} m{n(-18 * s)},{n(10 * s)} l{n(18 * s)},{n(-10 * s)} l{n(18 * s)},{n(10 * s)}", "none", 'stroke="#8c9296" stroke-width="2.5" stroke-linecap="round"')]
    o.append(poly([(x - 16 * s, y + 16 * s), (x + 16 * s, y + 16 * s), (x + 30 * s, y + 24 * s), (x + 40 * s, y + 80 * s), (x + 28 * s, y + 84 * s),
                   (x + 24 * s, y + 52 * s), (x + 24 * s, y + 96 * s), (x - 24 * s, y + 96 * s), (x - 24 * s, y + 52 * s), (x - 28 * s, y + 84 * s),
                   (x - 40 * s, y + 80 * s), (x - 30 * s, y + 24 * s)], color))
    o.append(line(x, y + 18 * s, x, y + 96 * s, "#00000033", 2.5) + rect(x - 22 * s, y + 66 * s, 12 * s, 3, "#00000026") + rect(x + 10 * s, y + 66 * s, 12 * s, 3, "#00000026"))
    return "".join(o)


def rack(x, y, w, colors):
    o = [line(x, y, x + w, y, "#8c9296", 6), rect(x - 4, y, 7, 170, "#8c9296"), rect(x + w - 3, y, 7, 170, "#8c9296"),
         rect(x - 20, y + 166, 44, 6, "#6b7478", rx=3), rect(x + w - 22, y + 166, 44, 6, "#6b7478", rx=3)]
    step = w / len(colors)
    for k, c in enumerate(colors):
        o.append(jacket(x + step * (k + .5), y, c))
    return "".join(o)


def shop_wall():
    b = [rect(0, 0, W, H, "#efe5d0"), rect(0, 300, W, 100, "#b99d7a"), rect(0, 290, W, 10, "#a58863")]
    for k in range(0, W, 64):
        b.append(rect(k, 300, 2, 100, "#a58863", extra='opacity=".6"'))
    return b


def tienda_1():
    b = shop_wall()
    # door and cold street window at the left
    b.append(rect(0, 30, 168, 260, "#cfe3e6") + rect(0, 30, 168, 260, "none", extra=f'stroke="{C["brown"]}" stroke-width="8"'))
    b.append(rect(80, 30, 8, 260, C["brown"]))
    for fx, fy in ((22, 70), (60, 120), (112, 80), (130, 160), (36, 200), (100, 230), (146, 40)):
        b.append(circ(fx, fy, 4, "#fffdf8"))
    b.append(rect(0, 270, 168, 20, "#fffdf8"))
    # racks
    b.append(rack(190, 92, 210, [C["red"], "#4a82b8", C["ink"], C["red"]]))
    b.append(rack(430, 92, 190, ["#4a82b8", C["ink"], C["red"]]))
    b.append(rect(190, 40, 430, 30, C["deep"], rx=6) + circ(235, 55, 8, C["mustard"]) + circ(265, 55, 8, C["mustard"]) + circ(295, 55, 8, C["mustard"]))
    # counter
    b.append(rect(420, 285, 220, 80, "#a98466") + rect(410, 274, 240, 14, "#c99a5b", rx=4))
    b.append(rect(460, 246, 56, 30, "#cfd5d6", rx=4) + rect(470, 238, 36, 10, C["dgrey"]))
    # clerk behind and Lucia
    b.append(person(540, 345, h=235, look=-1, mood="smile", arms=((470, 260), (606, 262)), **CLERK))
    b.append(rect(410, 274, 240, 14, "#c99a5b", rx=4) + rect(420, 288, 220, 80, "#a98466"))
    b.append(person(270, 392, h=238, look=1, mood="sad", arms=((296, 262), (246, 264)), **LUCIA))
    b.append(rect(222, 290, 82, 26, "#00000000"))
    return wrap(b)


def tienda_2():
    b = shop_wall()
    # fitting room curtain left, big mirror right
    b.append(rect(0, 20, 250, 280, "#e7c1b7") + rect(0, 20, 250, 24, C["terra_d"]))
    for k in range(0, 250, 30):
        b.append(path(f"M{k},44 q10,120 0,256", "none", 'stroke="#d3a79b" stroke-width="6"'))
    b.append(rect(300, 24, 170, 290, "#a98466", rx=10) + rect(312, 36, 146, 266, "#d9ecef", rx=6))
    b.append(poly([(312, 120), (340, 36), (372, 36), (312, 170)], "#ffffff", 'opacity=".5"'))
    b.append('<clipPath id="mr"><rect x="312" y="36" width="146" height="266" rx="6"/></clipPath><g clip-path="url(#mr)">')
    b.append(person(385, 330, h=210, look=0, mood="smile", **dict(LUCIA, coat=C["ink"], scarf=None)))
    b.append("</g>")
    b.append(rect(312, 36, 146, 266, "#ffffff", extra='opacity=".18"'))
    # Lucia in front
    b.append(person(190, 394, h=250, look=1, mood="smile", arms=((150, 290), (230, 292)), **dict(LUCIA, coat=C["ink"], scarf=None)))
    # clerk with price tag
    b.append(person(545, 394, h=238, look=-1, mood="smile", arms=((505, 270), (484, 236)), **CLERK))
    b.append(path("M484,236 l20,-30", "none", f'stroke="{C["brown"]}" stroke-width="2"'))
    b.append(poly([(466, 188), (526, 188), (540, 210), (526, 232), (466, 232)], C["red"]) + circ(480, 210, 5, C["white"]) + circ(506, 210, 7, C["white"], 'opacity=".9"'))
    b.append(path("M498,204 l16,12 M514,204 l-16,12", "none", 'stroke="#c24a3f" stroke-width="3"'))
    b.append(rect(300, 330, 170, 10, "#a98466", rx=3))
    return wrap(b)


SCENES = {"es-en-la-tienda-de-ropa-1": tienda_1, "es-en-la-tienda-de-ropa-2": tienda_2}
