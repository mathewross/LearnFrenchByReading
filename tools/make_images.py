#!/usr/bin/env python3
"""Draws the flat SVG story scenes into content/images/ (original artwork, CC0).
Re-run after editing:  python3 tools/make_images.py
Canvas is 640x400; the reader crops with object-fit: cover, so keep key content central."""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "content" / "images"
W, H = 640, 400

C = dict(
    ink="#2f3b3d", teal="#4f7c82", deep="#35595e", sage="#8fae9a", sage_d="#6a8f7b", cream="#f6f1e4",
    sand="#e6dcc3", terra="#b9735a", terra_d="#a15f49", mustard="#d9ab4a", brown="#6b4a3a", skin="#ecc3a0",
    skin2="#c98f6b", navy="#3d4a63", red="#c24a3f", yellow="#e8c547", grey="#9aa3a6", lgrey="#cfd5d6",
    white="#fffdf8", sky="#cfe3e6", pink="#e7a9a0", plum="#8a6b8f", dgrey="#5c6568",
)
FONT = "Georgia, 'Times New Roman', serif"
SANS = "system-ui, Arial, sans-serif"


def n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def rect(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" rx="{n(rx)}" fill="{fill}" {extra}/>'


def circ(x, y, r, fill, extra=""):
    return f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}" fill="{fill}" {extra}/>'


def ell(x, y, rx, ry, fill, extra=""):
    return f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{n(rx)}" ry="{n(ry)}" fill="{fill}" {extra}/>'


def poly(pts, fill, extra=""):
    return f'<polygon points="{" ".join(f"{n(a)},{n(b)}" for a, b in pts)}" fill="{fill}" {extra}/>'


def polyline(pts, stroke, w, extra=""):
    return (f'<polyline points="{" ".join(f"{n(a)},{n(b)}" for a, b in pts)}" fill="none" stroke="{stroke}" '
            f'stroke-width="{n(w)}" stroke-linecap="round" stroke-linejoin="round" {extra}/>')


def path(d, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" {extra}/>'


def line(x1, y1, x2, y2, stroke, w, extra=""):
    return (f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" stroke="{stroke}" '
            f'stroke-width="{n(w)}" stroke-linecap="round" {extra}/>')


def text(x, y, s, size=18, fill=None, anchor="middle", weight="normal", font=FONT):
    return (f'<text x="{n(x)}" y="{n(y)}" font-family="{font}" font-size="{n(size)}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill or C["ink"]}">{s}</text>')


def wrap(parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
            + "".join(parts) + "</svg>")


# ------------------------------------------------------------------ characters

def person(x, y, h=220, coat=None, hair=None, skin=None, pants=None, style="bob", mood="smile", look=0,
           cheeks=False, arms=None, legs=None, show_legs=True, scarf=None):
    """Flat figure standing with feet at (x, y). arms=(left_hand, right_hand) as absolute points (or None);
    legs=((x,y),(x,y)) for walking/running feet; show_legs=False for a seated figure hidden behind a table."""
    coat, hair, skin, pants = coat or C["sage_d"], hair or C["brown"], skin or C["skin"], pants or C["navy"]
    r = .085 * h
    cy = y - .915 * h
    sh = y - .80 * h
    tb = y - .46 * h
    tw = .27 * h
    o = []
    if show_legs:
        if legs is None:
            lw = .1 * h
            for lx in (x - lw - 2, x + 2):
                o.append(rect(lx, tb - 6, lw, y - tb + 6 - .02 * h, pants, rx=lw / 3))
                o.append(ell(lx + lw / 2, y - .012 * h, lw * .75, .022 * h, C["ink"]))
        else:
            for (fx, fy), hx in zip(legs, (x - .05 * h, x + .05 * h)):
                o.append(line(hx, tb, fx, fy - .012 * h, pants, .1 * h))
                o.append(ell(fx, fy, .065 * h, .025 * h, C["ink"]))
    o.append(rect(x - tw / 2, sh, tw, tb - sh + .05 * h, coat, rx=.08 * h))
    if scarf:
        o.append(rect(x - tw * .42, sh - .015 * h, tw * .84, .06 * h, scarf, rx=.03 * h))
        o.append(rect(x + tw * .1, sh + .02 * h, .05 * h, .13 * h, scarf, rx=.02 * h))
    hl = (x - tw / 2 - .015 * h, tb - .03 * h)
    hr = (x + tw / 2 + .015 * h, tb - .03 * h)
    left, right = (arms or (None, None))
    for (hand, side) in ((left or hl, -1), (right or hr, 1)):
        s0 = (x + side * (tw / 2 - .03 * h), sh + .05 * h)
        o.append(line(s0[0], s0[1], hand[0], hand[1], coat, .08 * h))
        o.append(circ(hand[0], hand[1], .04 * h, skin))
    if style in ("bob", "bun"):
        o.append(ell(x, cy - .22 * r, 1.3 * r, 1.14 * r, hair))  # ends above the chin so it never reads as a beard
    o.append(circ(x, cy, r, skin))
    if style != "bald":
        o.append(path(f"M{n(x - 1.03 * r)},{n(cy - .05 * r)} Q{n(x - .9 * r)},{n(cy - 1.4 * r)} {n(x)},{n(cy - 1.32 * r)} "
                      f"Q{n(x + .9 * r)},{n(cy - 1.4 * r)} {n(x + 1.03 * r)},{n(cy - .05 * r)} "
                      f"Q{n(x)},{n(cy - .78 * r)} {n(x - 1.03 * r)},{n(cy - .05 * r)} Z", hair))
    if style == "bun":
        o.append(circ(x, cy - 1.42 * r, .48 * r, hair))
    ex = look * .22 * r
    er = max(1.7, .09 * r)
    o.append(circ(x - .38 * r + ex, cy + .1 * r, er, C["ink"]))
    o.append(circ(x + .38 * r + ex, cy + .1 * r, er, C["ink"]))
    sw = f'stroke="{C["ink"]}" stroke-width="{n(max(1.4, .07 * r))}" stroke-linecap="round"'
    mx = x + ex * .6
    if mood == "smile":
        o.append(path(f"M{n(mx - .38 * r)},{n(cy + .42 * r)} Q{n(mx)},{n(cy + .88 * r)} {n(mx + .38 * r)},{n(cy + .42 * r)}", "none", sw))
    elif mood == "sad":
        o.append(path(f"M{n(mx - .3 * r)},{n(cy + .66 * r)} Q{n(mx)},{n(cy + .4 * r)} {n(mx + .3 * r)},{n(cy + .66 * r)}", "none", sw))
    elif mood == "open":
        o.append(path(f"M{n(mx - .4 * r)},{n(cy + .38 * r)} Q{n(mx)},{n(cy + 1.1 * r)} {n(mx + .4 * r)},{n(cy + .38 * r)} Z", "#7a3b3b"))
    else:
        o.append(line(mx - .26 * r, cy + .55 * r, mx + .26 * r, cy + .55 * r, C["ink"], max(1.4, .07 * r)))
    if cheeks:
        for sx in (-1, 1):
            o.append(circ(x + sx * .62 * r, cy + .42 * r, .24 * r, "#e58f86", 'opacity=".75"'))
    return "<g>" + "".join(o) + "</g>"


# ------------------------------------------------------------------ props

def suitcase(x, y, w=60, h=85, color=None):
    color = color or C["red"]
    top = y - h
    o = [rect(x - w / 2 + w * .22, top - 15, w * .56, 18, "none", rx=6, extra=f'stroke="{C["ink"]}" stroke-width="3.5"'),
         rect(x - w / 2, top, w, h, color, rx=9),
         rect(x - w / 2 + w * .2, top, w * .09, h, "#9d3a31"), rect(x + w / 2 - w * .29, top, w * .09, h, "#9d3a31"),
         rect(x - w / 2, top + h * .47, w, 5, "#9d3a31"),
         circ(x - w / 2 + 9, y + 2, 5, C["ink"]), circ(x + w / 2 - 9, y + 2, 5, C["ink"])]
    return "".join(o)


def bubble(x, y, w, h, s, tail, size=17):
    tx, ty = tail
    bx = min(max(tx, x + 20), x + w - 20)
    st = f'stroke="{C["lgrey"]}" stroke-width="2"'
    return (rect(x, y, w, h, C["white"], rx=14, extra=st)
            + poly([(bx - 9, y + h - 1), (bx + 9, y + h - 1), (tx, ty)], C["white"], f'{st} stroke-linejoin="round"')
            + rect(bx - 8, y + h - 3, 16, 5, C["white"])
            + text(x + w / 2, y + h / 2 + size * .34, s, size))


def cloud(x, y, s=1.0, fill="#f6f1e4"):
    return ("<g>" + circ(x, y, 22 * s, fill) + circ(x + 26 * s, y - 8 * s, 28 * s, fill) + circ(x + 56 * s, y, 22 * s, fill)
            + rect(x - 22 * s, y, 100 * s, 22 * s, fill, rx=11 * s) + "</g>")


def sun(x, y, r, color="#f0c75e"):
    rays = "".join(line(x + math.cos(a) * (r + 7), y + math.sin(a) * (r + 7), x + math.cos(a) * (r + 17), y + math.sin(a) * (r + 17), color, 4)
                   for a in [i * math.pi / 4 for i in range(8)])
    return circ(x, y, r, color) + rays


def rain(x0, x1, y0, y1, count, seed=3, color="#6f8790", length=20):
    rnd = random.Random(seed)
    drops = "".join(f'<path d="M{n(a)} {n(b)}l{n(-length * .3)} {n(length)}"/>'
                    for a, b in ((rnd.uniform(x0, x1), rnd.uniform(y0, y1)) for _ in range(count)))
    return f'<g stroke="{color}" stroke-width="2" stroke-linecap="round" opacity=".7">{drops}</g>'


def building(x, base, w, h, fill, win="#f6f1e4", cols=3, rows=4, roof=None, shutter=None):
    o = [rect(x, base - h, w, h, fill)]
    if roof:
        o.append(poly([(x - 4, base - h), (x + w + 4, base - h), (x + w - 8, base - h - 22), (x + 8, base - h - 22)], roof))
    ww, wh = w / (cols * 1.9), h / (rows * 2.0)
    for r_ in range(rows):
        for c_ in range(cols):
            wx = x + (c_ + .5) * w / cols - ww / 2
            wy = base - h + (r_ + .55) * h / rows
            if shutter:
                o.append(rect(wx - ww * .45, wy, ww * .4, wh, shutter))
                o.append(rect(wx + ww * 1.05, wy, ww * .4, wh, shutter))
            o.append(rect(wx, wy, ww, wh, win, rx=2))
    return "".join(o)


def tree(x, base, s=120, trunk=None, leaf=None, leaf2=None):
    trunk, leaf, leaf2 = trunk or C["brown"], leaf or C["sage_d"], leaf2 or C["sage"]
    return (rect(x - .05 * s, base - .45 * s, .1 * s, .45 * s, trunk)
            + circ(x, base - .7 * s, .34 * s, leaf) + circ(x - .24 * s, base - .52 * s, .26 * s, leaf)
            + circ(x + .24 * s, base - .52 * s, .26 * s, leaf) + circ(x - .08 * s, base - .78 * s, .16 * s, leaf2))


def flower(x, y, color):
    return line(x, y, x, y + 14, "#5f8a66", 2) + circ(x, y, 5, color) + circ(x, y, 2, "#fff3c4")


def eiffel(x, base, h, fill):
    p = [(0, -h), (.05, -.62), (.1, -.4), (.2, 0), (.14, 0), (.07, -.16), (-.07, -.16), (-.14, 0), (-.2, 0), (-.1, -.4), (-.05, -.62)]
    return (poly([(x + a * h, base + b * h) for a, b in p], fill)
            + rect(x - .075 * h, base - .42 * h, .15 * h, .02 * h, fill) + rect(x - .055 * h, base - .64 * h, .11 * h, .02 * h, fill))


def cup(x, y, w=26, color=None):
    color = color or C["white"]
    return (ell(x, y + 2, w * .85, 4, "#d8d1c0") + rect(x - w / 2, y - w * .7, w, w * .7, color, rx=5)
            + path(f"M{n(x + w / 2 - 1)},{n(y - w * .55)} q{n(w * .4)},{n(w * .1)} 0,{n(w * .35)}", "none", f'stroke="{color}" stroke-width="3"')
            + ell(x, y - w * .7, w / 2, 3.5, "#6b4a3a"))


def croissant(x, y, s=30, color=None):
    color = color or C["mustard"]
    return (f'<g transform="translate({n(x)},{n(y)})">'
            + ell(0, 0, .5 * s, .3 * s, color) + ell(-.46 * s, .12 * s, .3 * s, .2 * s, color, 'transform="rotate(35 -13 3)"')
            + ell(.46 * s, .12 * s, .3 * s, .2 * s, color, 'transform="rotate(-35 13 3)"')
            + line(-.15 * s, -.25 * s, -.1 * s, .25 * s, "#b98a2e", 2) + line(.15 * s, -.25 * s, .1 * s, .25 * s, "#b98a2e", 2) + "</g>")


def umbrella_open(x, y, w=190, pole=110):
    top = y - .55 * w
    d = (f"M{n(x - w / 2)},{n(y)} C{n(x - w / 2)},{n(y - .62 * w)} {n(x + w / 2)},{n(y - .62 * w)} {n(x + w / 2)},{n(y)} "
         f"A{n(w / 6)},{n(w / 6)} 0 0 1 {n(x + w / 6)},{n(y)} A{n(w / 6)},{n(w / 6)} 0 0 1 {n(x - w / 6)},{n(y)} "
         f"A{n(w / 6)},{n(w / 6)} 0 0 1 {n(x - w / 2)},{n(y)} Z")
    o = [line(x, y - 8, x, y + pole, C["ink"], 4),
         path(f"M{n(x)},{n(y + pole)} q0,12 -12,12", "none", f'stroke="{C["ink"]}" stroke-width="4" stroke-linecap="round"'),
         path(d, C["yellow"]),
         path(f"M{n(x)},{n(top + 6)} L{n(x - w / 6)},{n(y)} M{n(x)},{n(top + 6)} L{n(x + w / 6)},{n(y)}", "none", 'stroke="#c9a52c" stroke-width="2"'),
         circ(x, top + 2, 4, C["ink"])]
    return "".join(o)


def umbrella_closed(x1, y1, x2, y2, color=None):
    color = color or C["yellow"]
    return (line(x1, y1, x2, y2, color, 14) + line(x2 - (x2 - x1) * .08, y2 - (y2 - y1) * .08, x2, y2, C["ink"], 8)
            + path(f"M{n(x1)},{n(y1)} q-14,2 -12,16", "none", f'stroke="{C["ink"]}" stroke-width="4" stroke-linecap="round"'))


def tiles(color="#efe9d6", seam="#e1d9c0", floor_y=330, floor="#b9b2a1"):
    o = [rect(0, 0, W, H, color)]
    for xx in range(0, W, 48):
        o.append(line(xx, 0, xx, floor_y, seam, 2))
    for yy in range(0, floor_y, 48):
        o.append(line(0, yy, W, yy, seam, 2))
    o.append(rect(0, floor_y, W, H - floor_y, floor))
    o.append(rect(0, floor_y, W, 6, "#a39c8b"))
    return o


def table(x, y, rx=120):
    return (ell(x, y + 7, rx, 22, "#d0c7b3") + ell(x, y, rx, 22, C["white"]) + rect(x - 7, y + 20, 14, 95, C["brown"])
            + ell(x, y + 118, 48, 9, C["brown"]))


# ------------------------------------------------------------------ léa à paris, episode 1

def lea_1_train():
    b = [rect(0, 0, W, H, "#eadfc6")]
    gx, gy, gw, gh = 250, 46, 360, 200
    b.append(f'<clipPath id="g"><rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="8"/></clipPath>')
    b.append(rect(gx - 14, gy - 14, gw + 28, gh + 38, "#7a5c47", rx=16))
    b.append('<g clip-path="url(#g)">')
    b.append(rect(gx, gy, gw, gh, "#cfe3e6"))
    b.append(sun(300, 90, 18, "#f3e3b0") + cloud(520, 80, .8))
    for bx, bw, bh in [(255, 40, 55), (298, 34, 80), (336, 46, 46), (385, 38, 64), (560, 45, 70), (590, 30, 50)]:
        b.append(rect(bx, 208 - bh, bw, bh, "#a9bcc0"))
    b.append(eiffel(480, 208, 130, "#7f98a8"))
    b.append(rect(gx, 208, gw, 40, "#7f9a8c"))
    for tx in (270, 340, 430, 520, 580):
        b.append(circ(tx, 212, 18, "#6a8f7b"))
    b.append("</g>")
    b.append(rect(426, gy, 8, gh, "#7a5c47"))
    for yy in (100, 145, 190):
        b.append(line(262, yy, 322, yy, C["white"], 3, 'opacity=".6"'))
    b.append(rect(0, 340, W, 60, C["deep"]))
    b.append(person(150, 408, h=300, coat=C["sage_d"], look=1, show_legs=False, arms=((112, 240), (228, 232))))
    b.append(rect(0, 258, W, 84, C["terra"]))
    b.append(rect(0, 258, W, 10, C["terra_d"]))
    b.append(suitcase(560, 392, 66, 94))
    return wrap(b)


def lea_1_platform():
    b = [rect(0, 0, W, H, "#e9e2d0"), rect(0, 0, W, 34, C["deep"]),
         rect(48, 34, 14, 270, "#c9c2b0"), rect(578, 34, 14, 270, "#c9c2b0"),
         rect(0, 92, W, 170, "#d8dede"), rect(0, 214, W, 16, C["teal"]), rect(0, 236, W, 6, C["grey"]),
         rect(0, 262, W, 38, C["dgrey"])]
    for wx in (28, 150, 390, 510):
        b.append(rect(wx, 112, 104, 74, C["deep"], rx=8))
        b.append(rect(wx + 8, 118, 40, 12, "#5d8a90", rx=4))
    b.append(rect(268, 104, 84, 150, "#c4cdcf", rx=6))
    b.append(rect(282, 118, 56, 76, C["deep"], rx=6))
    b += [rect(0, 300, W, 100, "#d9cfb8"), rect(0, 300, W, 8, "#bfb396"), rect(0, 336, W, 6, C["mustard"])]
    b.append(person(470, 388, h=240, coat=C["navy"], hair="#4a3a32", skin=C["skin2"], pants="#2f3b4a", style="short",
                    arms=(None, (540, 150))))
    b.append(suitcase(292, 392, 62, 90))
    b.append(person(205, 388, h=230, coat=C["sage_d"], cheeks=True, look=1, arms=(None, (276, 302))))
    b.append(bubble(20, 52, 215, 40, "Bonjour, monsieur !", (205, 160)))
    b.append(bubble(330, 52, 225, 40, "Bonjour, madame !", (476, 152)))
    return wrap(b)


def lea_1_cafe():
    b = [rect(0, 0, W, H, "#f1e4c8"), rect(0, 250, W, 150, "#d8b995")]
    for lx in (300, 560):
        b += [line(lx, 0, lx, 62, C["brown"], 3), path(f"M{lx - 26},84 Q{lx},38 {lx + 26},84 Z", C["mustard"])]
    b += [rect(350, 118, 250, 8, C["brown"])]
    for cx_ in (380, 420, 540, 575):
        b.append(cup(cx_, 118, 22))
    b.append(person(450, 410, h=250, coat=C["white"], hair="#3a2e28", skin=C["skin"], style="short",
                    arms=((395, 252), (505, 252))))
    b.append(poly([(441, 212), (459, 212), (450, 222)], C["navy"]) + poly([(441, 212), (441, 224), (450, 222)], C["navy"]))
    b += [rect(326, 262, 322, 14, "#a98466"), rect(334, 274, 306, 126, C["brown"]),
          rect(556, 204, 66, 58, C["grey"], rx=6), circ(580, 232, 10, C["lgrey"]), rect(594, 214, 20, 8, C["dgrey"])]
    b.append(cup(500, 262, 26))
    b.append(person(158, 340, h=230, coat=C["sage_d"], show_legs=False, cheeks=True, look=1, arms=((112, 246), (205, 250))))
    b.append(table(160, 258, 125))
    b.append(ell(125, 254, 32, 8, "#efe9d8") + croissant(125, 245, 34))
    b.append(cup(205, 256, 28))
    b.append(bubble(14, 24, 250, 40, "Un café, s'il vous plaît !", (150, 106)))
    b.append(bubble(372, 52, 220, 40, "Oui, tout de suite !", (452, 160)))
    return wrap(b)


def lea_1_sun():
    b = [rect(0, 0, W, 252, "#cfe8ee"), sun(90, 80, 34), cloud(220, 60, .9), cloud(470, 110, .7)]
    xs = [(0, 70, 120, "#efe2c4"), (74, 60, 150, "#e7d6b0"), (138, 80, 110, "#f1e6cc"), (222, 64, 140, "#e5d3ae"),
          (290, 76, 118, "#efe2c4"), (370, 70, 150, "#e7d6b0"), (444, 62, 112, "#f1e6cc"), (510, 70, 138, "#e5d3ae"), (584, 60, 122, "#efe2c4")]
    for x, w, h, f in xs:
        b.append(building(x, 252, w, h, f, "#9fb6bb", cols=2, rows=int(h / 36), roof="#7f8c93"))
    b.append(eiffel(572, 252, 175, "#7f98a8"))
    b.append(rect(0, 252, W, 150, "#e0d5bb"))
    for xx in range(-20, W, 60):
        b.append(line(xx, 252, xx - 40, 400, "#d3c7a8", 2))
    b += [rect(36, 322, 60, 44, C["terra"], rx=6), flower(52, 296, "#e58f86"), flower(66, 288, C["mustard"]), flower(80, 298, C["pink"]),
          line(52, 310, 52, 322, "#5f8a66", 3), line(66, 300, 66, 322, "#5f8a66", 3), line(80, 310, 80, 322, "#5f8a66", 3)]
    b.append(person(222, 384, h=235, coat=C["sage_d"], show_legs=False, cheeks=True, mood="open", arms=((176, 306), (268, 270))))
    b.append(table(222, 304, 112))
    b.append(ell(180, 300, 30, 8, "#efe9d8") + croissant(180, 291, 34))
    b.append(cup(268, 276, 24))
    b.append(bubble(270, 62, 280, 40, "Paris est une belle ville !", (236, 160)))
    return wrap(b)


# ------------------------------------------------------------------ léa à paris, episode 2

def lea_2_map():
    b = tiles()
    b += [rect(40, 40, 300, 210, C["white"], rx=10, extra=f'stroke="{C["lgrey"]}" stroke-width="3"'), rect(40, 40, 300, 32, C["deep"], rx=10),
          rect(40, 56, 300, 16, C["deep"]), text(190, 63, "MÉTRO", 17, C["white"], weight="bold", font=SANS)]
    b.append(polyline([(66, 108), (150, 134), (250, 102), (316, 142)], C["red"], 7))
    b.append(polyline([(62, 214), (150, 166), (240, 216), (318, 188)], "#4a77a8", 7))
    b.append(polyline([(60, 152), (180, 236), (306, 232)], C["sage_d"], 7))
    b.append(polyline([(66, 96), (130, 196), (206, 152), (312, 230)], "#f3e3b0", 18))
    b.append(polyline([(66, 96), (130, 196), (206, 152), (312, 230)], C["yellow"], 9))
    for px, py in [(66, 96), (130, 196), (206, 152), (312, 230), (150, 134), (250, 102), (150, 166), (240, 216), (180, 236)]:
        b.append(circ(px, py, 6, C["white"], f'stroke="{C["ink"]}" stroke-width="2.5"'))
    b += [rect(545, 120, 78, 200, C["navy"], rx=8), rect(555, 134, 58, 42, C["sky"], rx=4), text(584, 164, "2 €", 22, C["ink"], font=SANS, weight="bold"),
          rect(565, 214, 38, 9, "#1f2733", rx=3)]
    for i in range(3):
        for j in range(3):
            b.append(circ(566 + i * 18, 246 + j * 18, 5, C["lgrey"]))
    b.append(person(436, 386, h=232, coat=C["sage_d"], cheeks=True, look=-1, arms=((350, 176), (482, 262))))
    b += [rect(470, 240, 40, 24, C["white"], rx=3, extra=f'stroke="{C["grey"]}" stroke-width="2"'), text(490, 257, "2 €", 12, C["ink"], font=SANS, weight="bold")]
    b.append(circ(482, 262, 9, C["skin"]))
    b.append(bubble(358, 34, 180, 40, "La ligne jaune ?", (440, 150)))
    return wrap(b)


def lea_2_lady():
    b = tiles()
    b += [rect(496, 24, 128, 100, C["yellow"], rx=14), text(560, 52, "LIGNE", 15, C["ink"], font=SANS, weight="bold"),
          poly([(516, 88), (558, 88), (558, 70), (600, 92), (558, 114), (558, 96), (516, 96)], C["ink"])]
    b.append(person(190, 388, h=230, coat=C["sage_d"], look=1, arms=((168, 262), (214, 262))))
    b.append(person(440, 388, h=215, coat=C["plum"], hair="#cfcfcf", style="bun", scarf=C["teal"], arms=(None, (556, 150))))
    b.append(bubble(24, 74, 170, 40, "Excusez-moi !", (185, 168)))
    b.append(bubble(250, 64, 205, 40, "Là-bas, à droite !", (440, 176)))
    return wrap(b)


def lea_2_metro():
    b = [rect(0, 0, W, H, "#ecd27a"), rect(0, 0, W, 34, "#cdb55c")]
    for wx in (36, 196):
        b.append(rect(wx, 60, 140, 100, "#2a3548", rx=10))
        for k in range(6):
            b.append(rect(wx + 10 + k * 22, 100 + (k % 2) * 14, 12, 4, "#f3e3b0", extra='opacity=".8"'))
    b += [rect(470, 50, 140, 270, "#d8bd5a", rx=6), rect(482, 64, 56, 168, "#2a3548", rx=4), rect(546, 64, 56, 168, "#2a3548", rx=4),
          rect(0, 340, W, 60, "#7f8a8d")]
    b.append(person(110, 392, h=232, coat=C["navy"], hair="#bdbdbd", style="short", mood="flat", skin=C["skin2"]))
    b.append(person(545, 392, h=228, coat=C["terra"], hair="#2f2622", mood="flat"))
    b.append(person(395, 390, h=236, coat=C["plum"], hair="#4a3a32", style="short", mood="flat", skin=C["skin2"]))
    b.append(person(335, 380, h=210, coat="#6f8790", hair="#3a2e28", style="short", mood="flat"))
    b.append(rect(255, 34, 11, 310, "#b9bfc1") + rect(255, 34, 4, 310, "#dfe3e4"))
    b.append(suitcase(215, 396, 60, 80))
    b.append(person(262, 404, h=262, coat=C["sage_d"], cheeks=True, look=1, arms=(None, (260, 156))))
    return wrap(b)


def lea_2_park():
    b = [rect(0, 0, W, 270, "#cfe8ee"), sun(540, 62, 30), cloud(90, 70, 1.0), cloud(330, 40, .7),
         ell(160, 272, 260, 70, "#a9c3ac"), ell(500, 285, 300, 80, C["sage"]), rect(0, 270, W, 130, "#9fc09a"),
         poly([(236, 400), (404, 400), (350, 268), (298, 268)], C["sand"])]
    for tx, base, s in [(60, 330, 170), (585, 322, 160), (165, 292, 95), (470, 288, 95), (250, 275, 60)]:
        b.append(tree(tx, base, s))
    rnd = random.Random(7)
    cols = [C["pink"], C["yellow"], "#f4f0e6", "#d98f8a", "#b49ad0"]
    for _ in range(46):
        side = rnd.choice((0, 1))
        fx = rnd.uniform(40, 215) if side == 0 else rnd.uniform(425, 600)
        fy = rnd.uniform(300, 385)
        b.append(flower(fx, fy, rnd.choice(cols)))
    b.append(person(320, 384, h=200, coat=C["sage_d"], mood="open", cheeks=True, arms=((262, 214), (378, 214))))
    return wrap(b)


# ------------------------------------------------------------------ le parapluie jaune

THOMAS = dict(coat="#2f5f6b", hair="#2b2622", skin="#d9a984", pants="#3f4750", style="short")


def pj_rain():
    b = [rect(0, 0, W, H, "#b7c3c8")]
    cols = [("#d9b77a", "#6f8f8a"), ("#d99f90", "#6f8f8a"), ("#c98a62", "#7a8f98"), ("#e5d6b8", "#6f8f8a")]
    x = -10
    for i, hgt in enumerate([190, 220, 170, 210, 180, 230, 190]):
        w = 98
        f, sh = cols[i % 4]
        b.append(building(x, 292, w, hgt, f, "#8fa4ab", cols=2, rows=int(hgt / 42), roof="#8a8f94", shutter=sh))
        x += w + 1
    b += [rect(0, 292, W, 108, "#8e9aa0"), rect(0, 292, W, 8, "#a3adb2")]
    for yy, ww in ((330, 220), (360, 300), (388, 160)):
        b.append(rect(60 + yy % 7 * 30, yy, ww, 4, "#a6b2b7", rx=2))
    b.append(person(292, 392, h=232, mood="sad", legs=((268, 392), (320, 386)), arms=(None, (322, 260)), **THOMAS))
    b.append(umbrella_open(322, 146, 200, 114))
    b.append(circ(400, 150, 9, "#f4f1ea") + circ(382, 170, 6, "#f4f1ea") + circ(368, 188, 4, "#f4f1ea"))
    b.append(cloud(472, 70, 1.5, "#f4f1ea"))
    b += [rect(490, 90, 9, 54, C["brown"]), rect(490, 114, 92, 24, "#6f9aa0", rx=4), rect(490, 132, 92, 6, C["brown"]),
          ell(514, 110, 17, 9, C["white"]), text(598, 102, "Z", 22, "#6f9aa0", weight="bold"), text(612, 80, "z", 16, "#6f9aa0", weight="bold")]
    b.append(rain(0, W, 0, 400, 70, color="#5f7882"))
    return wrap(b)


def pj_bus():
    b = [rect(0, 0, W, H, "#d8d2c0"), rect(24, 56, 592, 126, "#9fb1b8", rx=10), rect(0, 340, W, 60, "#6b7478")]
    for xx in (216, 408):
        b.append(rect(xx, 56, 8, 126, "#d8d2c0"))
    b.append(rain(30, 610, 60, 170, 40, seed=5, color="#dbe8ec", length=26))
    b += [rect(430, 200, 200, 100, C["terra_d"], rx=14)]
    b.append(person(525, 396, h=220, coat=C["plum"], hair="#cfcfcf", style="bun", mood="sad", scarf="#6f9aa0",
                    show_legs=False, arms=((436, 238), (600, 300))))
    b.append(rect(420, 290, 220, 56, C["terra"], rx=10))
    b.append(rect(118, 36, 11, 310, "#b9bfc1") + rect(118, 36, 4, 310, "#dfe3e4"))
    b.append(person(222, 400, h=252, mood="smile", arms=((124, 176), (350, 240)), **THOMAS))
    b.append(umbrella_closed(348, 242, 440, 232))
    b.append(circ(438, 236, 9, C["skin"]))
    b.append(bubble(370, 70, 225, 40, "Merci, jeune homme !", (520, 176)))
    return wrap(b)


def pj_run():
    b = [rect(0, 0, W, H, "#b7c3c8"), rect(370, 112, 280, 14, C["brown"]), rect(380, 124, 260, 176, "#d9b77a"),
         rect(416, 140, 190, 52, C["deep"], rx=6), text(511, 178, "GARE", 36, C["white"], font=SANS, weight="bold"),
         rect(468, 214, 84, 86, "#f3e3b0"), rect(498, 214, 4, 86, "#d9c58a"),
         rect(0, 300, W, 100, "#8e9aa0"), rect(0, 300, W, 8, "#a3adb2")]
    for ex, ey, ew in ((120, 352, 90), (340, 372, 110), (470, 335, 70)):
        b.append(ell(ex, ey, ew, 7, "#a6b2b7"))
    b.append(person(258, 384, h=230, mood="open", cheeks=True, legs=((222, 384), (298, 346)),
                    arms=((190, 254), (312, 236)), **dict(THOMAS, hair="#1f1a17")))
    for dx, dy in ((226, 160), (296, 154), (302, 190), (214, 188)):
        b.append(circ(dx, dy, 3.5, "#7fb3c7"))
    b.append(path("M205,382 q-8,-20 -22,-22 M215,380 q-2,-20 -14,-28", "none", 'stroke="#c8d5da" stroke-width="3" stroke-linecap="round"'))
    b.append(rain(0, W, 0, 400, 95, seed=9, color="#5f7882", length=24))
    return wrap(b)


def pj_cake():
    b = [rect(0, 0, W, H, "#dfeef0"), sun(80, 70, 34), cloud(270, 56, .9), cloud(470, 96, .7)]
    x = 110
    for i, (hgt, f) in enumerate([(150, "#d9b77a"), (190, "#d99f90"), (160, "#c98a62"), (180, "#e5d6b8"), (140, "#d9b77a")]):
        b.append(building(x, 250, 100, hgt, f, "#8fa4ab", cols=2, rows=int(hgt / 42), roof="#8a8f94", shutter="#6f8f8a"))
        x += 104
    b += [rect(0, 250, W, 150, "#d9cfb8"), rect(0, 250, W, 8, "#c4b99a")]
    b += [rect(56, 112, 9, 270, "#7f8a8d"), rect(22, 100, 78, 72, C["deep"], rx=12), text(61, 128, "ARRÊT", 16, C["white"], font=SANS, weight="bold"),
          rect(36, 138, 50, 22, C["white"], rx=5), circ(48, 164, 5, C["ink"]), circ(74, 164, 5, C["ink"])]
    b.append(person(320, 386, h=218, coat=C["plum"], hair="#cfcfcf", style="bun", scarf="#6f9aa0", arms=((262, 276), (396, 252))))
    b.append(umbrella_closed(396, 252, 452, 236))
    b += [ell(262, 286, 44, 9, C["white"]), rect(236, 252, 52, 32, "#5a3a2a", rx=6), ell(262, 252, 26, 8, "#7a4a35"),
          path("M236,254 q6,16 12,0 q6,18 12,0 q6,14 12,0 q6,16 16,0", "#7a4a35"), circ(262, 246, 5, C["red"])]
    b.append(person(512, 390, h=236, mood="smile", cheeks=True, arms=((446, 240), None), **THOMAS))
    b.append(bubble(212, 86, 150, 40, "Pour vous !", (320, 170)))
    b.append(bubble(520, 54, 104, 40, "Merci !", (516, 150)))
    return wrap(b)


SCENES = {
    "lea-1-train": lea_1_train, "lea-1-platform": lea_1_platform, "lea-1-cafe": lea_1_cafe, "lea-1-sun": lea_1_sun,
    "lea-2-map": lea_2_map, "lea-2-lady": lea_2_lady, "lea-2-metro": lea_2_metro, "lea-2-park": lea_2_park,
    "pj-rain": pj_rain, "pj-bus": pj_bus, "pj-run": pj_run, "pj-cake": pj_cake,
}


def load_scene_modules():
    """Extra scenes live in tools/scenes/*.py; each defines SCENES = {image_id: function returning an SVG string}
    and imports the drawing helpers with `from make_images import *`."""
    import importlib.util
    import sys
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    for f in sorted((here / "scenes").glob("*.py")):
        spec = importlib.util.spec_from_file_location(f"scenes_{f.stem}", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        SCENES.update(mod.SCENES)


def main():
    load_scene_modules()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in SCENES.items():
        svg = fn()
        (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(f"{name}.svg  {len(svg) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
