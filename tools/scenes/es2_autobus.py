import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

ELENA = dict(coat=C["plum"], hair="#3a2e28", style="bob", pants=C["navy"], cheeks=True)
DRIVER = dict(coat=C["deep"], hair="#2b2622", style="short", pants=C["navy"])


def bus(x, base, w, h, color):
    top = base - h
    o = [rect(x, top, w, h - 16, color, rx=16), rect(x + 4, top + h * .66, w - 8, 9, "#fffdf8", extra='opacity=".8"')]
    k = 0
    xx = x + 16
    while xx + 54 < x + w - 90:
        o.append(rect(xx, top + 14, 54, h * .38, "#cfe3e6", rx=5))
        xx += 62
        k += 1
    o.append(rect(x + w - 84, top + 14, 68, h * .6, "#cfe3e6", rx=6))  # windscreen / door glass
    o.append(rect(x + w - 150, top + 12, 54, h * .66, "#a9c3c8", rx=4) + line(x + w - 123, top + 12, x + w - 123, top + 12 + h * .66, color, 3))
    o.append(rect(x + w - 10, top + h * .6, 10, 18, C["yellow"], rx=4))
    for wx in (x + 62, x + w - 70):
        o.append(circ(wx, base - 14, 20, C["ink"]) + circ(wx, base - 14, 9, C["lgrey"]))
    o.append(rect(x + 14, top + h * .78, w - 28, 3, "#00000022"))
    return "".join(o)


def street_bg(base=262):
    b = [rect(0, 0, W, H, "#cfe3e6"), sun(560, 58, 24), cloud(90, 62, .9), cloud(330, 42, .7)]
    x = -10
    for i, (hgt, f) in enumerate([(150, "#d9b77a"), (190, "#d99f90"), (130, "#e5d6b8"), (175, "#c98a62"), (150, "#d9b77a"), (185, "#e5d6b8")]):
        b.append(building(x, base, 108, hgt, f, "#8fa4ab", cols=2, rows=max(2, int(hgt / 44)), roof="#8a8f94", shutter="#6f8f8a"))
        x += 106
    b += [rect(0, base, W, 24, "#d9cfb8"), rect(0, base + 24, W, 70, C["dgrey"]), rect(0, base + 94, W, 6, "#b9b2a1"), rect(0, base + 100, W, 40, "#d9cfb8")]
    b.append(rect(0, base + 140, W, 20, "#d9cfb8"))
    for xx in range(10, W, 90):
        b.append(rect(xx, base + 56, 46, 5, "#efe9d6", rx=2))
    return b


def autobus_1():
    b = street_bg()
    b.append(bus(300, 344, 340, 128, C["terra"]))
    # bus stop at left
    b += [rect(78, 190, 8, 190, C["grey"]), circ(82, 190, 26, C["deep"]), rect(70, 178, 24, 18, C["white"], rx=4),
          circ(74, 202, 3.5, C["white"]), circ(90, 202, 3.5, C["white"]),
          rect(30, 330, 100, 10, "#a98466", rx=3), rect(36, 340, 6, 36, "#a98466"), rect(118, 340, 6, 36, "#a98466")]
    b.append(rect(0, 392, W, 8, "#cfc4a8"))
    for lx in (150, 128, 168):
        b.append(line(lx - 20, 270 + (lx % 7) * 8, lx - 70, 270 + (lx % 7) * 8, "#ffffffaa", 4))
    b.append(person(238, 394, h=238, mood="open", look=1, legs=((196, 394), (284, 366)), arms=((190, 262), (306, 232)), **ELENA))
    b.append(rect(172, 258, 34, 26, C["brown"], rx=4) + path("M180,258 q9,-12 18,0", "none", f'stroke="{C["brown"]}" stroke-width="4"'))
    b.append(circ(306, 232, 7, C["skin"]))
    b.append(path("M196,396 q-10,-4 -18,-14 M214,398 q-14,-2 -26,-10", "none", 'stroke="#ffffffaa" stroke-width="4" stroke-linecap="round"'))
    return wrap(b)


def autobus_2():
    b = [rect(0, 0, W, H, "#efe3c9"), rect(0, 300, W, 100, "#8c9296"), rect(0, 292, W, 8, "#6b7478")]
    b.append('<clipPath id="bw"><rect x="0" y="44" width="640" height="150"/></clipPath><g clip-path="url(#bw)">')
    b.append(rect(0, 44, W, 150, "#cfe3e6") + sun(560, 90, 18))
    x = 0
    for hgt, f in [(100, "#d9b77a"), (130, "#d99f90"), (90, "#e5d6b8"), (120, "#c98a62"), (100, "#d9b77a"), (125, "#e5d6b8"), (95, "#d99f90")]:
        b.append(building(x, 194, 96, hgt, f, "#8fa4ab", cols=2, rows=3, roof="#8a8f94"))
        x += 94
    b.append("</g>")
    b += [rect(0, 28, W, 18, C["terra"]), rect(0, 192, W, 8, "#d8cdb0")]
    for px in (160, 320, 480):
        b.append(rect(px, 44, 12, 150, "#d8cdb0"))
    b.append(line(0, 64, W, 64, "#c9ced0", 5, 'opacity="0"'))
    for hx in (90, 240, 420, 590):
        b.append(line(hx, 46, hx, 82, "#b9bfc1", 3) + circ(hx, 94, 11, "none", 'stroke="#6b7478" stroke-width="4"'))
    # seats + passenger
    b.append(person(78, 348, h=215, coat=C["mustard"], hair="#cfcfcf", style="bun", show_legs=False, look=1))
    b.append(rect(14, 246, 128, 104, C["teal"], rx=14) + rect(14, 326, 128, 24, C["deep"], rx=8))
    # driver cabin
    b.append(rect(440, 280, 200, 62, C["dgrey"], rx=6) + rect(440, 276, 200, 8, "#8c9296"))
    b.append(person(556, 352, h=205, show_legs=False, look=-1, arms=((498, 262), (484, 268)), **DRIVER))
    b.append(ell(486, 262, 38, 12, "none", f'stroke="{C["ink"]}" stroke-width="6"') + circ(486, 262, 6, C["ink"]) + rect(484, 268, 5, 22, C["ink"]))
    # pole + Elena
    b.append(rect(334, 30, 10, 312, "#b9bfc1") + rect(334, 30, 4, 312, "#dfe3e4"))
    b.append(person(262, 394, h=238, mood="open", look=1, arms=((222, 262), (338, 172)), **ELENA))
    b.append(rect(210, 232, 26, 42, C["ink"], rx=5) + rect(213, 236, 20, 30, "#7fb3c7", rx=3) + circ(222, 266, 7, C["skin"]))
    b.append(circ(338, 172, 7, C["skin"]))
    b.append(rect(8, 340, 40, 56, C["brown"], rx=8) + rect(16, 332, 24, 14, "none", rx=5, extra=f'stroke="{C["ink"]}" stroke-width="3"'))
    return wrap(b)


SCENES = {"es-el-autobus-1": autobus_1, "es-el-autobus-2": autobus_2}
