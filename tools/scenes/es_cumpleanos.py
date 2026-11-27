import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

ELENA = dict(coat="#c24a3f", hair="#5a3a2a", style="bob", pants=C["navy"], cheeks=True)
JAVIER = dict(coat=C["teal"], hair="#2b2622", style="short", pants=C["navy"])
GUESTS = [dict(coat=C["mustard"], hair="#3a2e28", style="short"), dict(coat=C["plum"], hair="#cfd5d6", style="bun", pants="#5c6568"),
          dict(coat="#6f8f6a", hair="#6b4a3a", style="bob", cheeks=True), dict(coat=C["pink"], hair="#3a2e28", style="bun", cheeks=True)]


def bucket_flowers(x, y, colors):
    o = [poly([(x - 22, y - 36), (x + 22, y - 36), (x + 17, y), (x - 17, y)], "#8fae9a")]
    for k, c_ in enumerate(colors):
        fx = x - 18 + k * 12
        o.append(line(fx, y - 34, fx + (k - 2) * 2, y - 66 - (k % 3) * 10, "#5f8a66", 2.5) + circ(fx + (k - 2) * 2, y - 68 - (k % 3) * 10, 7, c_) + circ(fx + (k - 2) * 2, y - 68 - (k % 3) * 10, 2.5, "#fff3c4"))
    return "".join(o)


def cumple_1():
    b = [rect(0, 0, W, H, "#e9ddc0"), rect(0, 310, W, 90, "#b9b2a1"), rect(0, 304, W, 8, "#a39c8b")]
    b.append(rect(0, 0, W, 60, "#d99f90") + "".join(poly([(k * 64, 60), (k * 64 + 64, 60), (k * 64 + 32, 78)], "#c24a3f" if k % 2 else "#f6f1e4") for k in range(10)))
    b.append(rect(40, 100, 180, 120, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(52, 112, 156, 96, C["sky"]) + rect(126, 112, 8, 96, "#fffdf8"))
    for k, cols in enumerate((["#c24a3f", "#e8c547", "#e7a9a0", "#c24a3f", "#fffdf8"], ["#e8c547", "#8a6b8f", "#c24a3f", "#e7a9a0", "#fffdf8"], ["#e7a9a0", "#fffdf8", "#e8c547", "#c24a3f", "#8a6b8f"])):
        b.append(bucket_flowers(420 + k * 70, 360 + (k % 2) * 6, cols))
    b.append(rect(240, 250, 150, 16, "#a98466", rx=3) + rect(250, 266, 8, 56, "#a98466") + rect(372, 266, 8, 56, "#a98466"))
    b.append(rect(300, 236, 36, 14, C["dgrey"], rx=3))
    b.append(person(300, 392, h=250, mood="sad", look=-1, **ELENA, show_legs=True, arms=((262, 316), (338, 300))))
    b.append(rect(272, 186, 56, 62, "#f3efe3", rx=6, extra='opacity="0"'))
    b.append(path("M285,128 q15,-10 30,0", "none", 'stroke="#fff" stroke-width="0"'))
    b.append(cloud(70, 270, .5, "#cfd5d6") if False else "")
    return wrap(b)


def cumple_2():
    b = [rect(0, 0, W, H, "#f3e4b8"), rect(0, 300, W, 100, "#c9ae88")]
    b.append(rect(0, 290, W, 10, "#b49670"))
    b.append(path("M0,40 Q160,100 320,40 T640,40", "none", 'stroke="#c24a3f" stroke-width="3"'))
    for k, c_ in enumerate(("#c24a3f", "#e8c547", "#4a82b8", "#8a6b8f", "#6f8f6a", "#e7a9a0", "#e8c547")):
        b.append(poly([(k * 100 + 22, 70 + (k % 2) * 8), (k * 100 + 46, 70 + (k % 2) * 8), (k * 100 + 34, 96 + (k % 2) * 8)], c_))
    for bx, by, c_ in ((60, 130, "#c24a3f"), (110, 170, "#4a82b8"), (560, 130, "#e8c547"), (520, 180, "#8a6b8f"), (600, 200, "#e7a9a0"), (30, 200, "#6f8f6a")):
        b.append(balloon(bx, by, c_))
    b.append(rect(180, 280, 280, 18, "#fffdf8", extra='opacity="0"'))
    b.append(rect(150, 300, 340, 14, "#fffdf8", rx=3) + rect(160, 314, 320, 40, "#b9735a"))
    b.append("".join(churro(200 + k * 6, 292, 0, 0) if False else "" for k in range(1)) + circ(230, 292, 10, "#c24a3f") + circ(250, 292, 10, "#e8c547") + rect(380, 276, 46, 24, "#e6c590", rx=4) + circ(330, 290, 14, "#e58a2c"))
    for k, (gx, gh, st) in enumerate(((60, 210, GUESTS[0]), (150, 230, GUESTS[1]), (500, 225, GUESTS[2]), (590, 200, GUESTS[3]))):
        b.append(person(gx, 392, h=gh, mood="open", look=1 if gx < 320 else -1, arms=((gx - 36, 150), (gx + 36, 150)), **st))
    b.append(person(250, 392, h=170, coat="#8f9aa3", hair="#cfd5d6", style="bun", mood="open", pants="#5c6568", arms=((226, 250), (276, 230))) if False else "")
    b.append(person(320, 392, h=250, mood="open", look=0, **ELENA, arms=((268, 190), (372, 190))))
    b.append(person(410, 392, h=240, mood="open", look=-1, arms=((376, 170), (446, 168)), **JAVIER))
    for k in range(26):
        rnd = [(37 * k + 11) % 600 + 20, (53 * k + 17) % 120 + 90]
        b.append(rect(rnd[0], rnd[1], 8, 4, ["#c24a3f", "#e8c547", "#4a82b8", "#e7a9a0", "#6f8f6a"][k % 5], extra=f'transform="rotate({k * 37 % 180} {rnd[0]} {rnd[1]})"'))
    return wrap(b)


def candles(x, y, n_, w):
    o = []
    for k in range(n_):
        cx = x - w / 2 + 6 + k * (w - 12) / (n_ - 1)
        o.append(rect(cx - 2, y - 18, 4, 18, "#e7a9a0") + ell(cx, y - 24, 3.2, 5.5, "#f6c24a") + ell(cx, y - 23, 1.5, 3, "#fff3c4"))
    return "".join(o)


def cumple_3():
    b = [rect(0, 0, W, H, "#f3e4b8"), rect(0, 292, W, 108, "#c9ae88")]
    b.append(path("M0,36 Q160,90 320,36 T640,36", "none", 'stroke="#c24a3f" stroke-width="3"'))
    b.append(balloon(70, 120, "#c24a3f") + balloon(580, 120, "#4a82b8") + balloon(110, 170, "#e8c547") + balloon(540, 170, "#e7a9a0"))
    b.append(person(90, 392, h=220, mood="smile", look=1, arms=((60, 300), (130, 280)), **GUESTS[1]))
    b.append(person(550, 392, h=200, mood="smile", look=-1, arms=((520, 300), (580, 290)), **GUESTS[0]))
    b.append(person(170, 392, h=120, mood="open", look=1, **GUESTS[3]) + person(470, 392, h=130, mood="open", look=-1, **GUESTS[2]))
    b.append(person(260, 392, h=236, mood="smile", look=1, arms=((226, 310), (280, 290)), **ELENA))
    b.append(person(380, 392, h=236, mood="smile", look=-1, arms=((350, 300), (420, 310)), **JAVIER))
    b.append(ell(320, 332, 170, 24, "#d8cdb0") + rect(150, 280, 340, 52, C["white"], rx=6) + rect(150, 280, 340, 8, "#e6dcc3"))
    b.append(rect(262, 238, 116, 48, "#fffdf8", rx=8) + rect(262, 262, 116, 12, "#e7a9a0") + candles(320, 238, 11, 100))
    b.append(circ(262, 262, 0, "none") + rect(186, 262, 40, 18, "#d9a357", rx=3) + rect(186, 262, 40, 6, "#c24a3f") + circ(430, 270, 10, C["red"]) + circ(450, 274, 10, "#e8c547"))
    b.append(rect(510, 300, 50, 36, "#4a82b8", rx=3) + rect(532, 300, 6, 36, "#fffdf8") + rect(510, 314, 50, 6, "#fffdf8"))
    return wrap(b)


SCENES = {"es-el-cumpleanos-1": cumple_1, "es-el-cumpleanos-2": cumple_2, "es-el-cumpleanos-3": cumple_3}
