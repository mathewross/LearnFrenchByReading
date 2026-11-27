import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _es import *

ANA = dict(coat="#e58f86", hair="#6b4a3a", style="bob", pants="#e58f86", cheeks=True)
PABLO = dict(coat=C["teal"], hair="#3a2e28", style="short", pants="#d9ab4a")
MAMA = dict(coat=C["plum"], hair="#3a2e28", style="bun", pants=C["plum"], cheeks=True)
PAPA = dict(coat="#6f8f6a", hair="#2b2622", style="short", pants=C["navy"])


def beach_bg(sea_y=150, wind=False):
    b = [rect(0, 0, W, H, "#cfe8ee"), sun(560, 56, 22)]
    b.append(cloud(80, 56, .8))
    b.append(rect(0, sea_y, W, 90, "#6fb0c0") + rect(0, sea_y, W, 10, "#8fc6d2"))
    for k in range(7):
        b.append(path(f"M{k * 100 + 20},{sea_y + 40 + (k % 3) * 18} q15,-10 30,0 q15,10 30,0", "none", 'stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"'))
    b.append(path(f"M0,{sea_y + 80} Q160,{sea_y + 60} 320,{sea_y + 84} T640,{sea_y + 78} L640,400 L0,400 Z", "#ecd6a0"))
    b.append(path(f"M0,{sea_y + 76} Q160,{sea_y + 56} 320,{sea_y + 80} T640,{sea_y + 74}", "none", 'stroke="#fff" stroke-width="6" opacity=".8"'))
    return b


def castle(x, y, s=1.0):
    c = "#d9b878"
    o = [rect(x - 50 * s, y - 40 * s, 100 * s, 40 * s, c), rect(x - 30 * s, y - 70 * s, 60 * s, 30 * s, c)]
    for tx in (-50, 50):
        o.append(rect(x + tx * s - 14 * s, y - 70 * s, 28 * s, 70 * s, c))
        o.append(poly([(x + tx * s - 14 * s, y - 70 * s), (x + tx * s + 14 * s, y - 70 * s), (x + tx * s, y - 94 * s)], "#c94a3f"))
    o.append(path(f"M{n(x - 12 * s)},{n(y)} v{n(-22 * s)} q{n(12 * s)},{n(-14 * s)} {n(24 * s)},0 v{n(22 * s)} Z", "#b89658"))
    return "".join(o)


def bucket(x, y, c=C["red"]):
    return poly([(x - 12, y - 22), (x + 12, y - 22), (x + 9, y), (x - 9, y)], c) + path(f"M{n(x - 10)},{n(y - 22)} q10,-14 20,0", "none", f'stroke="{C["ink"]}" stroke-width="2"')


def towel(x, y, w=140, h=52, c=C["red"]):
    o = [poly([(x - w / 2 + 12, y - h), (x + w / 2 + 12, y - h), (x + w / 2 - 12, y), (x - w / 2 - 12, y)], c)]
    for k in range(1, 4):
        o.append(poly([(x - w / 2 + 12 + k * w / 4 - 8, y - h), (x - w / 2 + 12 + k * w / 4, y - h), (x - w / 2 + k * w / 4 - 12 + 0, y), (x - w / 2 + k * w / 4 - 12 - 8, y)], "#fffdf8", 'opacity=".7"') if False else "")
    return "".join(o)


def playa_1():
    b = beach_bg()
    b.append(towel(180, 392, 200, 70, "#e7a9a0"))
    b.append(umbrella_open(180, 190, 210, 190))
    b.append(person(150, 360, h=190, show_legs=False, arms=((118, 310), (190, 300)), look=1, mood="smile", **MAMA))
    b.append(rect(172, 290, 36, 26, C["teal"], rx=3, extra='transform="rotate(-8 190 300)"') + rect(190, 292, 3, 22, "#fffdf8"))
    b.append(castle(430, 350, 1.4))
    b.append(person(540, 392, h=150, arms=((520, 336), (500, 360)), look=-1, mood="open", **PABLO))
    b.append(person(340, 392, h=140, arms=((318, 340), (380, 350)), look=1, mood="smile", **ANA))
    b.append(sombrero(340, 266, 17))
    b.append(bucket(474, 392) + bucket(262, 396, C["mustard"]))
    return wrap(b)


def playa_2():
    b = beach_bg(wind=True)
    b.append(person(250, 392, h=190, legs=((222, 392), (292, 366)), arms=((200, 290), (300, 250)), look=1, mood="open", **PABLO))
    b.append(person(130, 392, h=160, legs=((104, 392), (156, 372)), arms=((86, 330), (176, 290)), look=1, mood="open", **ANA))
    b.append(sombrero(430, 140, 24))
    b.append(path("M400,150 q30,-40 70,-18", "none", 'stroke="#fff" stroke-width="3" stroke-dasharray="5 6" opacity=".9"'))
    for yy, xx, ln in ((90, 60, 120), (130, 300, 160), (66, 380, 130), (200, 500, 100)):
        b.append(path(f"M{xx},{yy} h{ln} q18,0 18,-12 q0,-10 -12,-8", "none", 'stroke="#fffdf8" stroke-width="4" stroke-linecap="round" opacity=".9"'))
    b.append(person(540, 340, h=120, show_legs=True, mood="open", arms=((520, 290), (562, 280)), **PAPA))
    b.append(umbrella_closed(580, 280, 600, 392))
    return wrap(b)


def playa_3():
    b = beach_bg()
    b.append(rect(0, 280, W, 120, "#ecd6a0", extra='opacity=".6"'))
    b.append(person(160, 392, h=230, arms=((120, 300), (190, 290)), look=1, mood="smile", **MAMA))
    b.append(person(310, 392, h=150, arms=((290, 340), (344, 290)), look=1, mood="smile", **PABLO))
    b.append(person(450, 392, h=140, arms=((430, 340), (486, 270)), look=-1, mood="smile", **ANA))
    b.append(sombrero(450, 276, 17))
    b.append(cone(350, 278, "#fffdf8") + cone(492, 262, "#f2a0b4"))
    b.append(person(570, 392, h=240, arms=((545, 300), (600, 310)), look=-1, mood="smile", **PAPA))
    return wrap(b)


SCENES = {"es-un-dia-en-la-playa-1": playa_1, "es-un-dia-en-la-playa-2": playa_2, "es-un-dia-en-la-playa-3": playa_3}
