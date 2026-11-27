import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

ROSA = dict(coat=C["plum"], hair="#cfd5d6", style="bun", pants="#5c6568")
MATEO = dict(coat=C["teal"], hair="#3a2e28", style="short", pants=C["navy"])


def awning(x, y, w, h=44, n_=8):
    o = []
    sw = w / n_
    for i in range(n_):
        f = C["red"] if i % 2 == 0 else C["cream"]
        o.append(rect(x + i * sw, y, sw, h, f) + path(f"M{n(x + i * sw)},{n(y + h)} h{n(sw)} q{n(-sw / 2)},{n(14)} {n(-sw)},0 Z", f))
    return "".join(o)


def stall(x, w, fill_items, top=70):
    o = [rect(x + 6, top, 8, 260, C["brown"]), rect(x + w - 14, top, 8, 260, C["brown"]), awning(x, top, w)]
    o.append(rect(x, 262, w, 12, "#a98466") + rect(x + 4, 274, w - 8, 70, "#c9ae88"))
    o.append(rect(x + 8, 244, w - 16, 18, "#d9b77a", rx=3))
    o.extend(fill_items)
    return "".join(o)


def market_1():
    b = [rect(0, 0, W, H, "#f1e4c4"), rect(0, 340, W, 60, "#b9b2a1"), rect(0, 336, W, 8, "#a39c8b")]
    b.append(rect(0, 60, W, 200, "#e9d3a0", extra='opacity=".6"'))
    items = [tomato(300 + (k % 6) * 22, 240 - (k // 6) * 14, 11) for k in range(12)]
    items += [orange(450 + (k % 4) * 22, 240 - (k // 4) * 14, 11) for k in range(8)]
    items += [circ(360 + k * 0, 0, 0, "none") for k in range(0)]
    b.append(stall(250, 330, items))
    b.append(person(420, 330, h=250, coat="#f3efe3", hair="#2b2622", style="bun", mood="smile", cheeks=True, show_legs=False, arms=((380, 250), (470, 250))))
    b.append(rect(250, 262, 330, 12, "#a98466") + rect(254, 274, 322, 70, "#c9ae88"))
    b.append("".join(tomato(300 + (k % 6) * 22, 254 - (k // 6) * 12, 11) for k in range(6)) + "".join(orange(460 + k * 22, 254, 11) for k in range(4)))
    b.append(person(110, 392, h=250, arms=((70, 300), (150, 330)), look=1, mood="smile", cheeks=True, **ROSA))
    b.append(basket(158, 340, 62, 40))
    b.append(person(200, 392, h=160, arms=((176, 330), (234, 300)), look=-1, mood="smile", cheeks=True, **MATEO))
    b.append(rect(224, 276, 26, 32, "#fffdf8", rx=2, extra='stroke="#cfd5d6" stroke-width="2"'))
    return wrap(b)


def market_2():
    b = [rect(0, 0, W, H, "#f1e4c4"), rect(0, 300, W, 100, "#b9b2a1"), rect(0, 296, W, 8, "#a39c8b")]
    b.append(rect(0, 70, W, 150, "#e9d3a0", extra='opacity=".7"'))
    for k in range(6):
        b.append(awning(k * 110 - 20, 76, 104, 34, 4))
    for k, xx in enumerate((60, 150, 540, 600)):
        b.append(person(xx, 330, h=160 + (k % 2) * 40, coat=[C["sage_d"], C["mustard"], C["terra"], C["navy"]][k], hair="#3a2e28", style=["short", "bob", "bun", "short"][k], mood="open", look=1, show_legs=True))
    # man whose legs an orange passes between
    b.append(person(420, 350, h=240, coat="#6f8f6a", hair="#2b2622", style="short", mood="open", look=-1, pants="#5c6568"))
    b.append(person(250, 390, h=250, coat=C["teal"], hair="#3a2e28", style="short", mood="open", look=-1, legs=((220, 388), (294, 360)), arms=((196, 270), (310, 236))))
    # lady with hat catching an orange
    b.append(person(540, 380, h=230, coat=C["plum"], hair="#cfd5d6", style="bun", mood="open", look=-1))
    b.append(sombrero(540, 156, 24, "#e7c590") + orange(540, 130, 10))
    # torn bag and oranges
    b.append(rect(88, 340, 60, 40, "#d9b77a", rx=3) + path("M88,340 l12,-10 l12,10 l12,-10 l12,10 l12,-10 l12,10", "none", 'stroke="#d9b77a" stroke-width="3"'))
    for ox, oy in ((330, 372), (372, 356), (400, 340), (296, 388), (176, 370), (118, 372), (210, 386), (470, 372), (600, 378)):
        b.append(orange(ox, oy, 11))
    b.append("".join(line(sx, sy, sx + 22, sy, "#9aa3a6", 2, 'opacity=".6"') for sx, sy in ((345, 390), (310, 396), (190, 392))))
    return wrap(b)


SCENES = {"es-en-el-mercado-1": market_1, "es-en-el-mercado-2": market_2}
