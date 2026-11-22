#!/usr/bin/env python3
"""Draw the 1024x1024 news infographic for Sunday 22 November 2026.

Build-time only: run `python3 draw_infographic.py` to (re)generate entry.png.
Everything is drawn with Pillow primitives; no external assets, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

NAVY = (14, 27, 46)
NAVY_LIGHT = (24, 44, 71)
GOLD = (242, 183, 5)
CARD = (245, 247, 250)
INK = (16, 24, 40)
MUTED = (90, 104, 122)
FOOT = (159, 176, 195)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 52)
F_SUB = font("DejaVuSans.ttf", 22)
F_KICKER = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans-Bold.ttf", 24)
F_BODY = font("DejaVuSans.ttf", 17)
F_FOOT = font("DejaVuSans.ttf", 15)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_rocket(d, x, y, s, color):
    # Simple rocket: nose cone, body, fins, flame.
    d.polygon([(x + s * 0.5, y), (x + s * 0.72, y + s * 0.35),
               (x + s * 0.72, y + s * 0.75), (x + s * 0.5, y + s * 0.95),
               (x + s * 0.28, y + s * 0.75), (x + s * 0.28, y + s * 0.35)],
              fill=color)
    d.polygon([(x + s * 0.28, y + s * 0.6), (x, y + s * 0.95),
               (x + s * 0.28, y + s * 0.85)], fill=(200, 60, 40))
    d.polygon([(x + s * 0.72, y + s * 0.6), (x + s, y + s * 0.95),
               (x + s * 0.72, y + s * 0.85)], fill=(200, 60, 40))
    d.ellipse([x + s * 0.38, y + s * 0.3, x + s * 0.62, y + s * 0.54],
              fill=WHITE, outline=NAVY, width=2)


def draw_submarine(d, x, y, s, color):
    # Hull, conning tower, periscope, portholes, propeller.
    d.rounded_rectangle([x, y + s * 0.35, x + s, y + s * 0.75],
                        radius=int(s * 0.18), fill=color)
    d.rectangle([x + s * 0.38, y + s * 0.12, x + s * 0.6, y + s * 0.42],
                fill=color)
    d.rectangle([x + s * 0.46, y, x + s * 0.52, y + s * 0.16], fill=color)
    for cx in (0.22, 0.42, 0.62, 0.82):
        d.ellipse([x + s * cx - 5, y + s * 0.48, x + s * cx + 5,
                   y + s * 0.48 + 10], fill=WHITE)
    d.polygon([(x + s, y + s * 0.45), (x + s * 1.08, y + s * 0.32),
               (x + s * 1.08, y + s * 0.78), (x + s, y + s * 0.65)],
              fill=(120, 140, 160))


def draw_card_icon(d, x, y, s, color):
    # Credit card with a big "10%" on it.
    d.rounded_rectangle([x, y, x + s, y + s * 0.72], radius=6, fill=color)
    d.rectangle([x, y + s * 0.14, x + s, y + s * 0.26], fill=WHITE)
    d.text((x + 7, y + s * 0.34), "10%", font=font("DejaVuSans-Bold.ttf", 17),
           fill=WHITE)


def draw_scales(d, x, y, s, color):
    # Scales of justice: post, beam, two pans.
    d.rectangle([x + s * 0.47, y + s * 0.1, x + s * 0.53, y + s * 0.85],
                fill=color)
    d.rectangle([x + s * 0.05, y + s * 0.22, x + s * 0.95, y + s * 0.28],
                fill=color)
    d.rectangle([x + s * 0.3, y + s * 0.85, x + s * 0.7, y + s * 0.92],
                fill=color)
    for cx in (0.12, 0.88):
        d.line([(x + s * cx, y + s * 0.26), (x + s * (cx - 0.1), y + s * 0.55)],
               fill=color, width=2)
        d.line([(x + s * cx, y + s * 0.26), (x + s * (cx + 0.1), y + s * 0.55)],
               fill=color, width=2)
        d.pieslice([x + s * (cx - 0.12), y + s * 0.5, x + s * (cx + 0.12),
                    y + s * 0.74], 0, 180, fill=color)
    d.ellipse([x + s * 0.42, y, x + s * 0.58, y + s * 0.16], fill=GOLD)


def draw_globe_leaf(d, x, y, s, color):
    # Globe with a leaf: circle, meridians, leaf on top.
    d.ellipse([x, y + s * 0.08, x + s, y + s], outline=color, width=4)
    d.ellipse([x + s * 0.28, y + s * 0.08, x + s * 0.72, y + s],
              outline=color, width=3)
    d.line([(x, y + s * 0.54), (x + s, y + s * 0.54)], fill=color, width=3)
    d.arc([x - s * 0.2, y + s * 0.08, x + s * 1.2, y + s], 200, 340,
          fill=color, width=3)
    d.polygon([(x + s * 0.55, y), (x + s * 0.95, y - s * 0.28),
               (x + s * 0.98, y + s * 0.02), (x + s * 0.62, y + s * 0.14)],
              fill=(46, 160, 90))


def draw_medal(d, x, y, s, color):
    # Medal: ribbon V and a gold disc with a star.
    d.polygon([(x + s * 0.2, y), (x + s * 0.38, y),
               (x + s * 0.5, y + s * 0.45), (x + s * 0.32, y + s * 0.45)],
              fill=(200, 60, 40))
    d.polygon([(x + s * 0.8, y), (x + s * 0.62, y),
               (x + s * 0.5, y + s * 0.45), (x + s * 0.68, y + s * 0.45)],
              fill=(40, 90, 180))
    d.ellipse([x + s * 0.18, y + s * 0.4, x + s * 0.82, y + s],
              fill=GOLD, outline=(180, 130, 0), width=2)
    cx, cy, r = x + s * 0.5, y + s * 0.7, s * 0.16
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=WHITE)


ICONS = {
    "rocket": draw_rocket,
    "sub": draw_submarine,
    "card": draw_card_icon,
    "scales": draw_scales,
    "globe": draw_globe_leaf,
    "medal": draw_medal,
}

STORIES = [
    ("THE GULF", (200, 60, 40), "rocket",
     "Iran claims new strikes on US bases in Bahrain",
     "Tehran says its missiles and drones hit US Patriot radars; "
     "Bahrain says an industrial site was hit, with no injuries."),
    ("AUKUS", (40, 110, 180), "sub",
     "Australia hits back at US budget office",
     "Canberra rejects a warning that the submarine pact will shrink "
     "the US Navy's attack-submarine fleet."),
    ("UNITED STATES", (30, 120, 90), "card",
     "Trump vows 10% cap on card rates",
     "The president says he will work with the incoming Democratic "
     "Congress to cap credit-card interest."),
    ("PHILIPPINES", (150, 100, 10), "scales",
     "P568m gap at firm tied to VP Duterte",
     "Prosecutors question the vice president's defence as a "
     "tax-fraud probe opens into Cale88 Foods."),
    ("CLIMATE", (20, 140, 130), "globe",
     "COP31 talks in overtime, split on fossil fuels",
     "Negotiators miss their deadline as a draft drops fossil-fuel "
     "language and climate finance."),
    ("SPORT", (170, 60, 150), "medal",
     "Shimada wins Finlandia Trophy",
     "The 18-year-old Japanese skater takes her second Grand Prix "
     "title and books a Final spot."),
]


def main():
    img = Image.new("RGB", (1024, 1024), NAVY)
    d = ImageDraw.Draw(img)

    # Header.
    d.text((24, 18), "THE WORLD IN ONE IMAGE", font=F_KICKER, fill=GOLD)
    d.text((24, 44), "Sunday 22 November 2026", font=F_TITLE, fill=WHITE)
    d.text((24, 108), "Six stories, as reported today",
           font=F_SUB, fill=FOOT)
    d.line([(24, 148), (1000, 148)], fill=GOLD, width=3)

    # Cards: 2 columns x 3 rows.
    cw, ch, gap, top = 482, 246, 20, 164
    for i, (kicker, color, icon, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = 20 + col * (cw + gap)
        y = top + row * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=14, fill=CARD)
        d.rounded_rectangle([x, y, x + 10, y + ch], radius=5, fill=color)
        ICONS[icon](d, x + cw - 72, y + 10, 48, color)
        d.text((x + 24, y + 16), kicker, font=F_KICKER, fill=color)
        head_lines = wrap(d, head, F_HEAD, cw - 48)
        assert len(head_lines) <= 2, (head, head_lines)
        hy = y + 66
        for line in head_lines:
            d.text((x + 24, hy), line, font=F_HEAD, fill=INK)
            hy += 31
        body_lines = wrap(d, body, F_BODY, cw - 48)
        assert len(body_lines) <= 3, (head, body_lines)
        by = hy + 10
        for line in body_lines:
            d.text((x + 24, by), line, font=F_BODY, fill=(52, 64, 84))
            by += 24

    # Footer.
    d.text((24, 952),
           "Sources: Reuters · AP · GMA News · The Manila Times · The Japan Times",
           font=F_FOOT, fill=FOOT)
    d.text((24, 978), "Full source links in the README.",
           font=F_FOOT, fill=FOOT)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
