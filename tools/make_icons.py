#!/usr/bin/env python3
"""Generate flat PWA icons (192, 512, 512 maskable) into docs/icons/. Needs Pillow."""
import glob
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "docs" / "icons"
BG, FG, ACCENT = (79, 124, 130), (250, 247, 240), (214, 195, 160)


def find_font():
    for pattern in ("/usr/share/fonts/**/Gelasio*.ttf", "/usr/share/fonts/**/DejaVuSerif*.ttf", "/usr/share/fonts/**/*.ttf"):
        hits = sorted(glob.glob(pattern, recursive=True))
        if hits:
            return hits[0]
    return None


def draw(size, maskable):
    img = Image.new("RGBA", (size, size), BG + (255,))
    d = ImageDraw.Draw(img)
    if not maskable:  # rounded-square, transparent corners
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius=size // 5, fill=255)
        img.putalpha(mask)
    scale = 0.62 if maskable else 0.8  # maskable keeps the glyph in the safe zone
    box = size * scale
    x0, y0 = (size - box) / 2, (size - box) / 2
    # open book: two pages
    pw, ph = box * 0.46, box * 0.62
    top = y0 + box * 0.12
    d.rounded_rectangle([x0, top, x0 + pw, top + ph], radius=box * 0.05, fill=FG)
    d.rounded_rectangle([x0 + box - pw, top, x0 + box, top + ph], radius=box * 0.05, fill=FG)
    # text lines on the pages
    for i in range(3):
        y = top + ph * (0.25 + 0.2 * i)
        d.rectangle([x0 + pw * 0.15, y, x0 + pw * 0.8, y + box * 0.025], fill=ACCENT)
        d.rectangle([x0 + box - pw + pw * 0.2, y, x0 + box - pw * 0.15, y + box * 0.025], fill=ACCENT)
    # accent bookmark ribbon
    d.rectangle([x0 + box / 2 - box * 0.03, top - box * 0.02, x0 + box / 2 + box * 0.03, top + ph * 0.5], fill=ACCENT)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    draw(192, False).save(OUT / "icon-192.png")
    draw(512, False).save(OUT / "icon-512.png")
    draw(512, True).save(OUT / "icon-512-maskable.png")
    print("icons written to", OUT)


if __name__ == "__main__":
    main()
