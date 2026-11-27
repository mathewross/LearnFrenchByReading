import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

LUCIA = dict(coat="#c24a3f", hair="#3a2e28", style="bun", pants=C["navy"], cheeks=True)
ANSELMO = dict(coat="#7a6a4a", hair="#e0e0e0", style="short", pants="#4a5568", skin=C["skin2"])
PABLO = dict(coat=C["mustard"], hair="#2b2622", style="short", pants="#3a4250")


def mountains(y, tones=("#9db3b0", "#86a09c", "#6f8f8a")):
    o = [poly([(0, y), (90, y - 130), (190, y - 40), (300, y - 170), (410, y - 60), (520, y - 150), (640, y - 50), (640, y)], tones[0]),
         poly([(0, y), (60, y - 60), (160, y - 20), (260, y - 90), (360, y - 30), (470, y - 80), (560, y - 30), (640, y - 70), (640, y)], tones[1])]
    o.append(poly([(300, y - 170), (270, y - 130), (292, y - 136), (304, y - 118), (322, y - 134), (336, y - 124)], "#f6f1e4"))
    o.append(poly([(90, y - 130), (68, y - 96), (86, y - 100), (96, y - 88), (110, y - 100)], "#f6f1e4"))
    return o


def stone_house(x, base, w, h, roof=C["terra"], door=True):
    o = [rect(x, base - h, w, h, "#b8a58a")]
    for r_ in range(int(h / 14)):
        for c_ in range(int(w / 20) + 1):
            o.append(rect(x + (c_ * 20 + (r_ % 2) * 10) % w, base - h + r_ * 14 + 1, 18, 12, "#c9b99f", rx=2, extra='opacity=".7"'))
    o.append(poly([(x - 8, base - h), (x + w + 8, base - h), (x + w - 10, base - h - 26), (x + 10, base - h - 26)], roof))
    o.append(rect(x + w * .16, base - h * .72, w * .24, h * .3, "#f3e6b8", rx=2) + rect(x + w * .16 - 3, base - h * .72 + h * .3, w * .24 + 6, 4, "#8a7a5a"))
    if door:
        o.append(rect(x + w * .6, base - h * .52, w * .24, h * .52, "#6b4a3a", rx=3))
    return "".join(o)


def church(x, base):
    o = [rect(x, base - 90, 110, 90, "#d8cdb0"), poly([(x - 6, base - 90), (x + 116, base - 90), (x + 55, base - 132)], C["terra"]),
         rect(x + 118, base - 170, 46, 170, "#c9b99f"), rect(x + 128, base - 150, 26, 40, C["ink"], rx=13), rect(x + 128, base - 124, 26, 20, C["ink"]),
         poly([(x + 112, base - 170), (x + 170, base - 170), (x + 141, base - 214)], C["terra"]),
         circ(x + 141, base - 112, 4, C["mustard"]), rect(x + 40, base - 56, 30, 56, "#6b4a3a", rx=15), circ(x + 55, base - 74, 10, "#f3e6b8")]
    return "".join(o)


def sheep(x, y, s=1.0, d=1, head=True):
    o = [rect(x - 22 * s, y - 14 * s, 6 * s, 14 * s, "#4a4a4a", rx=2 * s), rect(x + 12 * s, y - 14 * s, 6 * s, 14 * s, "#4a4a4a", rx=2 * s)]
    for dx, dy, r_ in ((-22, -34, 17), (-6, -42, 19), (12, -38, 18), (26, -28, 14), (-30, -22, 13), (4, -22, 16), (-14, -26, 14)):
        o.append(circ(x + dx * s, y + dy * s, r_ * s, "#f6f1e4", f'stroke="#e6dcc3" stroke-width="{n(1.5 * s)}"'))
    if head:
        o.append(ell(x + d * 36 * s, y - 34 * s, 12 * s, 14 * s, "#4a4a4a") + ell(x + d * 30 * s, y - 42 * s, 5 * s, 8 * s, "#4a4a4a", f'transform="rotate({-d * 40} {n(x + d * 30 * s)} {n(y - 42 * s)})"')
                 + circ(x + d * 38 * s, y - 38 * s, 1.8 * s, "#fff"))
    return "".join(o)


def car(x, base, s=1.0, color="#4a82b8"):
    o = [rect(x, base - 44 * s, 150 * s, 32 * s, color, rx=10 * s), path(f"M{n(x + 32 * s)},{n(base - 44 * s)} l{n(16 * s)},{n(-26 * s)} h{n(56 * s)} l{n(20 * s)},{n(26 * s)} Z", color),
         path(f"M{n(x + 42 * s)},{n(base - 44 * s)} l{n(11 * s)},{n(-20 * s)} h{n(24 * s)} v{n(20 * s)} Z", "#cfe3e6"), path(f"M{n(x + 84 * s)},{n(base - 44 * s)} v{n(-20 * s)} h{n(22 * s)} l{n(14 * s)},{n(20 * s)} Z", "#cfe3e6")]
    for wx in (30, 120):
        o.append(circ(x + wx * s, base - 12 * s, 14 * s, C["ink"]) + circ(x + wx * s, base - 12 * s, 6 * s, C["lgrey"]))
    return "".join(o)


def pueblo_1():
    b = [rect(0, 0, W, H, "#d8ecf0"), sun(560, 56, 24), cloud(90, 52, .8)]
    b += mountains(250)
    b.append(rect(0, 235, W, 20, "#6f8f8a", extra='opacity="0"'))
    b.append(rect(0, 240, W, 70, "#8fae9a"))
    for tx, s in ((30, 70), (74, 90), (590, 80), (620, 66)):
        b.append(tree(tx, 262, s, leaf="#4f7a62", leaf2="#6a9a7a"))
    b.append(stone_house(30, 300, 110, 70) + stone_house(150, 300, 90, 60, door=False) + church(250, 300) + stone_house(440, 300, 100, 66) + stone_house(548, 300, 84, 56, door=False))
    b += [rect(0, 300, W, 100, "#d3c09a"), rect(0, 300, W, 8, "#bfa97f")]
    for k in range(0, 640, 60):
        b.append(ell(k + 20, 360 + (k % 3) * 14, 20, 4, "#c4b48f"))
    b.append(car(20, 394, 1.0))
    b.append(rect(240, 250, 22, 70, "#fff", extra='opacity="0"'))
    b.append(person(400, 396, h=250, look=-1, mood="flat", arms=((366, 300), (440, 262)), **LUCIA))
    # phone with no signal: crossed bars
    b.append(rect(432, 224, 28, 48, C["ink"], rx=5) + rect(436, 230, 20, 36, "#cfe3e6", rx=2))
    for k in range(3):
        b.append(rect(440 + k * 5, 252 - k * 6, 3, 6 + k * 6, C["grey"]))
    b.append(line(438, 234, 454, 262, C["red"], 3))
    b.append(circ(440, 268, 6, C["skin"]))
    b.append(suitcase(520, 396, 56, 78, C["mustard"]))
    return wrap(b)


def pueblo_2():
    b = [rect(0, 0, W, H, "#d8ecf0"), sun(80, 60, 26), cloud(260, 50, .9), cloud(470, 90, .7)]
    b += mountains(230, ("#9db3b0", "#86a09c", "#6f8f8a"))
    b.append(rect(0, 220, W, 180, "#a9c58f") + rect(0, 220, W, 8, "#8fae78"))
    b.append(ell(180, 250, 260, 36, "#9ab87f") + ell(520, 262, 240, 40, "#b3cd9a"))
    for fx in range(20, 640, 46):
        b.append(flower(fx + (fx % 3) * 6, 300 + (fx % 4) * 22, [C["yellow"], C["white"], C["pink"]][fx % 3]))
    b.append(tree(40, 270, 150, leaf="#5f8a66", leaf2="#7fae86"))
    b.append(dog(140, 330, .7, d=1))
    b.append(sheep(210, 292, .8) + sheep(560, 300, .9, d=-1) + sheep(620, 276, .6, d=-1))
    # Anselmo standing with crook
    b.append(line(540, 400, 546, 200, C["brown"], 6) + path("M546,200 q-18,-16 -18,6", "none", f'stroke="{C["brown"]}" stroke-width="6" stroke-linecap="round"'))
    b.append(person(486, 398, h=245, look=-1, mood="smile", arms=((450, 300), (538, 270)), **ANSELMO))
    b.append(ell(486, 168, 36, 9, "#8a6a4a") + path("M462,166 q24,-34 48,0 Z", "#8a6a4a"))
    # Lucia sitting among sheep
    b.append(person(330, 372, h=225, look=1, mood="smile", show_legs=False, arms=((300, 322), (372, 330)), **LUCIA))
    b.append(sheep(330, 392, 1.5, d=-1) + sheep(212, 400, 1.2, d=1))
    b.append(sheep(430, 398, 1.15, d=-1))
    return wrap(b)


def star4(x, y, r, col="#fff3c4"):
    return poly([(x, y - r), (x + r * .25, y - r * .25), (x + r, y), (x + r * .25, y + r * .25), (x, y + r), (x - r * .25, y + r * .25), (x - r, y), (x - r * .25, y - r * .25)], col)


def pueblo_3():
    b = [rect(0, 0, W, H, "#1f2a44"), rect(0, 120, W, 160, "#27365a"), rect(0, 210, W, 90, "#34476e")]
    rnd = random.Random(5)
    for _ in range(70):
        b.append(circ(rnd.uniform(0, W), rnd.uniform(0, 250), rnd.choice((1.2, 1.6, 2.2)), "#fff3c4", f'opacity="{rnd.choice((".6", ".8", "1"))}"'))
    for sx, sy, r_ in ((90, 60, 11), (230, 120, 9), (400, 50, 12), (520, 130, 10), (320, 170, 8)):
        b.append(star4(sx, sy, r_))
    b.append(circ(560, 70, 30, "#f6ecc0") + circ(572, 62, 26, "#1f2a44", 'opacity="0"'))
    b.append(path("M140,30 l60,26", "none", 'stroke="#fff3c4" stroke-width="3" stroke-linecap="round" opacity=".8"'))
    # distant valley with village lights
    b.append(path("M0,270 Q120,230 260,262 T520,254 T640,268 L640,330 L0,330 Z", "#25405a"))
    for hx, hy in ((60, 280), (110, 286), (180, 274), (300, 278), (360, 272), (430, 276), (560, 280)):
        b.append(rect(hx, hy, 18, 12, "#3a4a58") + poly([(hx - 2, hy), (hx + 20, hy), (hx + 9, hy - 8)], "#2f3b4a") + rect(hx + 6, hy + 4, 5, 5, "#f0c75e"))
    b.append(rect(236, 250, 14, 28, "#3a4a58") + poly([(234, 250), (252, 250), (243, 236)], "#2f3b4a") + rect(240, 256, 5, 8, "#f0c75e"))
    # foreground hill
    b.append(path("M0,330 Q200,290 400,320 T640,310 L640,400 L0,400 Z", "#2d4a46") + path("M0,372 Q220,340 440,366 T640,356 L640,400 L0,400 Z", "#243d3a"))
    for gx in range(10, 640, 38):
        b.append(path(f"M{gx},392 q-3,-14 -8,-18 M{gx},392 q2,-12 8,-16", "none", 'stroke="#3a5e56" stroke-width="3" stroke-linecap="round"'))
    # Pablo pointing up, Lucia amazed
    b.append(person(250, 396, h=250, look=0, mood="open", arms=((214, 300), (190, 130)), **dict(LUCIA, coat="#e07a6a")))
    b.append(person(400, 398, h=160, look=0, mood="open", arms=((380, 320), (432, 220)), **PABLO))
    b.append(circ(190, 130, 7, C["skin"]) + circ(432, 220, 6, C["skin"]))
    # phone lying on the grass, face down, forgotten
    b.append(rect(300, 384, 30, 14, "#2a2f33", rx=3))
    return wrap(b)


SCENES = {"es-un-pueblo-en-la-montana-1": pueblo_1, "es-un-pueblo-en-la-montana-2": pueblo_2, "es-un-pueblo-en-la-montana-3": pueblo_3}
