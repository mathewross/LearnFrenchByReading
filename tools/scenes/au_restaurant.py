import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import *

JULIE = dict(coat=C["plum"], hair="#3a2e28", style="bob")
HUGO = dict(coat=C["navy"], hair="#5a3a2a", style="short", skin=C["skin2"])


def glass(x, y, h=34, wine=None):
    o = [path(f"M{n(x - 9)},{n(y - h)} h18 q0,{n(h * .6)} -9,{n(h * .62)} q-9,0 -9,{n(-h * .62)} Z", "#e9f4f6", 'opacity=".9" stroke="#9cc3cc" stroke-width="2"')]
    if wine:
        o.append(path(f"M{n(x - 8)},{n(y - h * .5)} h16 q0,{n(h * .38)} -8,{n(h * .4)} q-8,0 -8,{n(-h * .4)} Z", wine))
    o.append(rect(x - 1.5, y - h * .38, 3, h * .38, "#9cc3cc") + ell(x, y + 1, 10, 2.5, "#9cc3cc"))
    return "".join(o)


def lamp(x, y, c="#e8c547"):
    return line(x, 0, x, y, C["brown"], 3) + path(f"M{x - 24},{y + 26} Q{x},{y - 8} {x + 24},{y + 26} Z", c) + ell(x, y + 30, 40, 12, "#f6dc86", 'opacity=".35"')


def restaurant_bg(dark=False):
    wall, floor = ("#e7c9a0", "#a8774f") if not dark else ("#6b4a45", "#3d2b2b")
    b = [rect(0, 0, W, H, wall), rect(0, 300, W, 100, floor), rect(0, 292, W, 8, "#00000022")]
    b.append(rect(0, 150, W, 142, "#00000010"))
    return b


def rest_1():
    b = restaurant_bg()
    # window with street at night-ish dusk
    b.append(rect(24, 50, 160, 190, "#fffdf8", rx=6) + rect(36, 62, 136, 166, "#7f9ec0") + rect(100, 62, 8, 166, "#fffdf8"))
    b.append(rect(36, 170, 136, 58, "#51627f") + circ(62, 98, 14, "#f3e3b0"))
    b.append(lamp(280, 34) + lamp(500, 34))
    # background tables and diners
    b.append(person(556, 318, h=150, coat=C["terra"], hair="#2f2622", show_legs=False, mood="smile"))
    b.append(rect(500, 258, 110, 8, C["white"]) + rect(550, 266, 10, 52, C["brown"]))
    # main table
    b.append(person(100, 372, h=235, show_legs=False, look=1, cheeks=True, mood="smile", arms=((70, 330), (150, 322)), **JULIE))
    b.append(person(262, 372, h=240, show_legs=False, look=-1, mood="smile", arms=((220, 330), (300, 322)), **HUGO))
    b.append(ell(180, 322, 112, 24, "#d0c7b3") + ell(180, 314, 112, 24, "#fffdf8") + rect(171, 336, 18, 70, C["brown"]) + ell(180, 402, 52, 9, C["brown"]))
    b.append(glass(140, 312, 30, "#b05a6a") + glass(232, 312, 30, "#bfe0ea"))
    # waiter with menu
    b.append(person(410, 412, h=285, coat="#fffdf8", hair="#3a2e28", style="short", pants="#2f3b4a", mood="smile",
                    arms=((372, 300), (326, 206))))
    b.append(rect(300, 140, 54, 80, C["red"], rx=4) + rect(308, 150, 38, 4, "#e8c547") + rect(308, 162, 38, 4, "#e8c547") + rect(308, 174, 38, 4, "#e8c547"))
    b.append(circ(326, 214, 10, C["skin2"]))
    return wrap(b)


def rest_2():
    b = restaurant_bg()
    b.append(lamp(150, 34) + lamp(430, 34))
    b.append(rect(480, 60, 140, 150, "#fffdf8", rx=6) + rect(490, 70, 120, 130, "#7f9ec0"))
    b.append(person(130, 412, h=270, show_legs=False, look=1, cheeks=True, mood="smile", arms=((88, 335), (180, 335)), **JULIE))
    b.append(person(330, 412, h=275, show_legs=False, look=-1, mood="smile", arms=((290, 336), (370, 336)), **HUGO))
    b.append(ell(230, 352, 190, 34, "#d0c7b3") + ell(230, 342, 190, 34, "#fffdf8"))
    b.append(rect(220, 372, 20, 40, C["brown"]))
    b.append(glass(190, 340, 38, "#b05a6a") + glass(290, 340, 38, "#bfe0ea") + glass(110, 342, 38) )
    b.append(ell(230, 345, 46, 10, "#efe9d8"))
    # waiter pouring
    b.append(person(540, 412, h=290, coat="#fffdf8", hair="#3a2e28", style="short", pants="#2f3b4a", mood="smile", look=-1,
                    arms=((560, 330), (440, 300))))
    b.append(f'<g transform="rotate(-70 440 300)">' + rect(428, 262, 20, 78, "#3f6b4a", rx=7) + rect(433, 238, 10, 28, "#3f6b4a", rx=3) + rect(430, 290, 16, 24, "#e8dcc0") + "</g>")
    b.append(circ(444, 304, 10, C["skin2"]))
    b.append(path("M394,276 q-6,22 -6,56", "none", 'stroke="#b05a6a" stroke-width="4" stroke-linecap="round"'))
    return wrap(b)


def rest_3():
    b = [rect(0, 0, W, H, "#4b3a46"), rect(0, 300, W, 100, "#2f2530")]
    for x_, y_ in ((90, 90), (530, 70), (320, 50)):
        b.append(circ(x_, y_, 70, "#f0c75e", 'opacity=".07"') + circ(x_, y_, 4, "#f0c75e"))
    b.append(rect(20, 40, 120, 160, "#2c3a58", rx=6))
    for yy in (60, 110, 160):
        b.append(circ(60 + yy % 3 * 10, yy, 3, "#f3e3b0"))
    b.append(person(130, 400, h=300, show_legs=False, look=1, cheeks=True, mood="open", arms=((90, 340), (200, 346)), **JULIE))
    b.append(person(510, 400, h=300, show_legs=False, look=-1, mood="open", arms=((470, 346), (560, 340)), **HUGO))
    # table
    b.append(rect(0, 330, W, 18, "#fffdf8") + rect(0, 348, W, 52, "#e8dcc0"))
    # candle in the middle
    b.append(rect(310, 296, 20, 40, C["cream"], rx=3) + path("M320,262 q12,18 0,32 q-12,-14 0,-32 Z", "#f0a43e") + path("M320,274 q5,8 0,16 q-5,-8 0,-16 Z", "#f6dc86"))
    b.append(circ(320, 282, 40, "#f0c75e", 'opacity=".15"'))
    # dishes
    b.append(ell(210, 338, 62, 15, "#f6f1e4") + ell(210, 334, 44, 9, "#e8dcc0") + ell(190, 328, 26, 8, "#e8e4d8") + path("M172,324 q22,-16 42,0 q-6,10 -20,10 q-14,0 -22,-10 Z", "#f0b998") + circ(224, 328, 5, "#6f8f6a"))
    b.append(ell(430, 338, 62, 15, "#f6f1e4") + ell(430, 334, 40, 10, "#e8dcc0") + path("M395,330 q35,-34 70,0 Z", C["red"], 'opacity=".9"'))
    b.append(circ(404, 322, 6, "#f6f1e4") + circ(416, 316, 6, "#f6f1e4"))
    b.append(glass(118, 342, 36, "#b05a6a") + glass(540, 342, 36, "#bfe0ea"))
    return wrap(b)


SCENES = {"au-restaurant-1": rest_1, "au-restaurant-2": rest_2, "au-restaurant-3": rest_3}
