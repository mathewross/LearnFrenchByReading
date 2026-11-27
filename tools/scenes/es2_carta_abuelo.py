import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

NARR = dict(coat=C["teal"], hair="#5a3a2a", style="bob", pants=C["navy"], cheeks=True)
MADRE = dict(coat=C["plum"], hair="#3a2e28", style="bun", pants="#6f8790", cheeks=True)
ELENA = dict(coat="#8a6b8f", hair="#e6e6e6", style="bun", pants=C["dgrey"], cheeks=True, skin=C["skin"])
CHICA = dict(coat=C["mustard"], hair="#2b2622", style="bob", pants=C["navy"], cheeks=True)
BOOKS = ["#c24a3f", "#4f7c82", "#d9ab4a", "#6a8f7b", "#8a6b8f", "#a15f49", "#3d4a63", "#e0c9a0", "#b9735a"]


def shelf(x, y, w, h, rows=4, seed=1):
    rnd = random.Random(seed)
    o = [rect(x, y, w, h, "#6b4a3a", rx=4), rect(x + 6, y + 6, w - 12, h - 12, "#4a3328")]
    rh = (h - 12) / rows
    for r_ in range(rows):
        by = y + 6 + (r_ + 1) * rh
        bx = x + 8
        while bx < x + w - 18:
            bw = rnd.randint(9, 16)
            bh = rnd.randint(int(rh * .6), int(rh - 6))
            o.append(rect(bx, by - bh - 2, bw, bh, rnd.choice(BOOKS), rx=1.5))
            bx += bw + 1
        o.append(rect(x + 6, by - 2, w - 12, 5, "#6b4a3a"))
    return "".join(o)


def pot(x, y, color=C["terra"], flowers=C["red"], s=1.0):
    o = [poly([(x - 14 * s, y - 20 * s), (x + 14 * s, y - 20 * s), (x + 10 * s, y), (x - 10 * s, y)], color), circ(x, y - 32 * s, 13 * s, "#5f8a66"), circ(x - 11 * s, y - 26 * s, 9 * s, "#6a9a72")]
    for dx, dy in ((-6, -38), (6, -36), (0, -46), (12, -30), (-12, -30)):
        o.append(circ(x + dx * s, y + dy * s, 5 * s, flowers) + circ(x + dx * s, y + dy * s, 1.8 * s, "#fff3c4"))
    return "".join(o)


def envelope(x, y, w=50, rot=0, color="#e9d28a"):
    h = w * .66
    return (f'<g transform="translate({n(x)},{n(y)}) rotate({n(rot)})">' + rect(-w / 2, -h / 2, w, h, color, rx=2, extra='stroke="#b9953f" stroke-width="2"')
            + path(f"M{n(-w / 2)},{n(-h / 2)} L0,{n(h * .1)} L{n(w / 2)},{n(-h / 2)}", "none", 'stroke="#b9953f" stroke-width="2"') + circ(0, h * .08, 3.5, C["red"]) + "</g>")


def carta_1():
    b = [rect(0, 0, W, H, "#e8dcc0"), rect(0, 310, W, 90, "#a98466"), rect(0, 302, W, 8, "#8d6a4f")]
    for k in range(0, W, 80):
        b.append(line(k, 310, k - 20, 400, "#8d6a4f", 2))
    b.append(shelf(10, 24, 150, 278, 5, 3))
    b.append(shelf(480, 24, 150, 278, 5, 7))
    b.append(rect(210, 44, 220, 140, "#fffdf8", rx=4, extra=f'stroke="{C["brown"]}" stroke-width="6"') + rect(222, 56, 196, 116, "#f3dfa8") + sun(320, 116, 26, "#f0c75e"))
    # boxes on floor
    b.append(box(40, 330, 110, 70, "#d2a46f") + box(70, 298, 80, 40, "#c9985f"))
    b.append(box(500, 336, 120, 64, "#d2a46f"))
    # mother carrying books
    b.append(person(540, 340, h=240, look=-1, mood="smile", show_legs=False, arms=((508, 310), (578, 310)), **MADRE))
    b.append(rect(504, 292, 80, 40, "#c24a3f", rx=3) + rect(508, 280, 72, 14, "#4f7c82", rx=2) + rect(512, 270, 64, 12, "#d9ab4a", rx=2))
    # narrator with book
    b.append(person(320, 396, h=250, look=0, mood="open", arms=((280, 262), (362, 262)), **NARR))
    b.append(rect(282, 252, 80, 26, "#6a8f7b", rx=3) + rect(318, 252, 4, 26, "#4a6e5a"))
    b.append(circ(282, 266, 6, C["skin"]) + circ(362, 266, 6, C["skin"]))
    b.append(envelope(352, 312, 54, 28))
    b.append(path("M330,292 q6,6 0,12", "none", 'stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"'))
    b.append(circ(190, 150, 18, "#e0c9a0", 'opacity="0"'))
    return wrap(b)


def carta_2():
    b = [rect(0, 0, W, H, "#cfe8ee"), sun(560, 56, 24), cloud(120, 56, .8)]
    # back house with the door
    b.append(rect(200, 70, 240, 250, "#fffdf8") + rect(200, 70, 240, 16, "#e6dcc3") + poly([(190, 70), (450, 70), (420, 40), (220, 40)], C["terra"]))
    b.append(rect(290, 150, 70, 170, "#3d6b78", rx=4) + rect(300, 160, 50, 56, "#2f5560", rx=3) + circ(346, 240, 4, C["mustard"]) + rect(310, 112, 30, 22, C["mustard"], rx=3))
    b.append(rect(215, 110, 54, 62, "#6f9aa0", rx=3) + rect(380, 110, 54, 62, "#6f9aa0", rx=3) + rect(210, 170, 64, 8, "#d9cfb8") + rect(375, 170, 64, 8, "#d9cfb8"))
    b.append(pot(240, 170, C["terra"], C["red"]) + pot(405, 170, C["terra"], C["red"]))
    # left and right walls, whitewashed, with pots
    b.append(poly([(0, 0), (190, 70), (190, 320), (0, 400)], "#f6f1e4") + poly([(640, 0), (450, 70), (450, 320), (640, 400)], "#efe5cf"))
    b.append(poly([(0, 0), (190, 70), (190, 82), (0, 24)], "#e6dcc3"))
    for k, (px, py) in enumerate(((40, 250), (100, 228), (150, 212))):
        b.append(pot(px, py + 20, C["terra"], C["red"], 1.1 - k * .1) + line(px - 20, py + 22, px + 20, py + 22, "#6b4a3a", 3))
    for k, (px, py) in enumerate(((600, 250), (540, 228), (490, 212))):
        b.append(pot(px, py + 20, C["terra"], C["red"], 1.1 - k * .1) + line(px - 20, py + 22, px + 20, py + 22, "#6b4a3a", 3))
    b.append(rect(30, 80, 80, 100, "#6f9aa0", rx=3, extra='opacity="0"'))
    # cobbled street
    b.append(poly([(0, 400), (190, 320), (450, 320), (640, 400)], "#d8c9a6"))
    for k in range(9):
        b.append(line(190 + k * 32, 320, -30 + k * 85, 400, "#c4b48f", 2))
    b.append(line(110, 360, 530, 360, "#c4b48f", 2) + line(60, 380, 580, 380, "#c4b48f", 2))
    # young woman in doorway
    b.append(person(325, 322, h=165, look=0, mood="smile", **CHICA))
    # visitors in foreground
    b.append(person(185, 398, h=250, look=1, mood="open", arms=((150, 300), (240, 262)), **NARR))
    b.append(envelope(244, 262, 40, 12))
    b.append(person(470, 398, h=240, look=-1, mood="smile", arms=((440, 300), (508, 300)), **MADRE))
    return wrap(b)


def carta_3():
    b = [rect(0, 0, W, H, "#f6f1e4"), rect(0, 300, W, 100, "#d9b78a"), rect(0, 292, W, 8, "#c9a370")]
    for yy in range(300, 400, 28):
        b.append(line(0, yy, W, yy, "#c9a370", 2))
    # blue tile dado
    b.append(rect(0, 214, W, 80, "#4a82b8"))
    for xx in range(0, W, 40):
        b.append(rect(xx + 4, 218, 32, 32, "#fffdf8", rx=3, extra='opacity=".85"') + circ(xx + 20, 234, 8, "#4a82b8") + rect(xx + 4, 254, 32, 32, "#fffdf8", rx=3, extra='opacity=".85"') + circ(xx + 20, 270, 8, "#4a82b8"))
    b.append(rect(0, 210, W, 8, "#35709f"))
    # arch with vine and hanging pots on the wall
    b.append(path("M60,214 v-110 a60,60 0 0 1 120,0 v110 Z", "#cfe3e6") + path("M52,214 v-110 a68,68 0 0 1 136,0 v110", "none", f'stroke="{C["brown"]}" stroke-width="8"'))
    b.append(circ(60, 110, 24, "#5f8a66") + circ(100, 52, 28, "#6a9a72") + circ(150, 70, 22, "#5f8a66") + circ(176, 120, 20, "#6a9a72") + circ(90, 100, 16, "#7fae86"))
    for k in range(5):
        b.append(circ(60 + k * 30, 70 + (k % 3) * 22, 5, C["pink"]))
    for px in (330, 420, 510, 600):
        b.append(rect(px - 3, 40, 6, 26, "none", extra="opacity='0'") + pot(px, 150, C["terra"], [C["red"], C["pink"], C["yellow"], C["red"]][(px // 90) % 4], 1.0) + line(px - 22, 150, px + 22, 150, "#6b4a3a", 3))
    # table with cups
    b.append(rect(240, 300, 320, 12, "#a98466", rx=4) + rect(252, 312, 8, 86, "#8d6a4f") + rect(540, 312, 8, 86, "#8d6a4f") + ell(400, 346, 0, 0, "none"))
    b.append(mug(300, 300, 28, C["white"]) + mug(500, 300, 28, C["terra"]) + rect(380, 284, 56, 18, "#e0c9a0", rx=9) + rect(386, 288, 44, 4, "#8a9a5a", rx=2))
    # Elena (seated) and narrator
    b.append(person(430, 352, h=235, look=-1, mood="sad", show_legs=False, arms=((396, 262), (360, 250)), **ELENA))
    b.append(rect(240, 296, 320, 14, "#a98466", rx=4) + rect(240, 310, 320, 4, "#00000014"))
    b.append(rect(300, 296, 28, 4, "#fff", extra="opacity='0'"))
    b.append(person(160, 396, h=250, look=1, mood="smile", arms=((130, 300), (210, 290)), **NARR))
    # letter in Elena's hands, tears
    b.append(rect(344, 218, 40, 56, "#fffdf8", rx=2, extra='stroke="#b9953f" stroke-width="2" transform="rotate(-8 364 246)"'))
    for k in range(4):
        b.append(line(350, 230 + k * 9, 376, 228 + k * 9, "#8c9296", 2, 'transform="rotate(-8 364 246)"'))
    b.append(circ(360, 254, 6, C["skin"]) + circ(396, 262, 6, C["skin"]))
    for sx, sy in ((408, 186), (452, 186)):
        b.append(path(f"M{sx},{sy} q4,8 0,12 q-4,-4 0,-12 Z", "#7fb3c7"))
    b.append(ell(540, 396, 60, 10, "#00000012"))
    b.append(pot(580, 396, C["terra"], C["red"], 1.6))
    return wrap(b)


SCENES = {"es-la-carta-de-mi-abuelo-1": carta_1, "es-la-carta-de-mi-abuelo-2": carta_2, "es-la-carta-de-mi-abuelo-3": carta_3}
