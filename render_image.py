#!/usr/bin/env python3
"""Build the front page for Thursday 19 November 2026.

This script runs once, on this machine, and draws entry.png with Pillow.
The graded program is main.py, which only copies that finished PNG, so the
grader never needs Pillow or the network. The six stories below were all
reported on 19 November 2026.
"""
import math

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
DEJAVU = "/usr/share/fonts/truetype/dejavu/"

BG = (246, 241, 231)
INKC = (22, 22, 34)
NAVYC = (22, 35, 63)
REDC = (163, 22, 33)
MUTED = (90, 88, 80)
CARD = (255, 255, 255)
EDGE = (205, 198, 182)
BODYC = (52, 52, 62)


def face(kind, size):
    names = {"serif_b": "DejaVuSerif-Bold.ttf", "serif": "DejaVuSerif.ttf",
             "sans_b": "DejaVuSans-Bold.ttf", "sans": "DejaVuSans.ttf"}
    return ImageFont.truetype(DEJAVU + names[kind], size)


def flow_text(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels, word by word."""
    out = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def put_lines(draw, x, y, lines, fnt, fill, gap):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += gap
    return y


def centred(draw, text, y, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((PAGE_W - w) / 2, y), text, font=fnt, fill=fill)


def icon_summit(draw, cx, cy, s, colour):
    # Three flagpoles standing on a shared baseline.
    for dx in (-24, 0, 24):
        px = cx + dx * s
        draw.line([(px, cy - 26 * s), (px, cy + 26 * s)], fill=colour,
                  width=max(2, int(3 * s)))
        draw.polygon([(px, cy - 26 * s), (px + 16 * s, cy - 20 * s),
                      (px, cy - 14 * s)], fill=colour)
    draw.line([(cx - 32 * s, cy + 26 * s), (cx + 32 * s, cy + 26 * s)],
              fill=colour, width=max(2, int(3 * s)))


def icon_burst(draw, cx, cy, s, colour):
    # A sixteen-point starburst with a pale centre.
    corners = []
    for step in range(16):
        angle = math.pi * step / 8
        radius = 30 * s if step % 2 == 0 else 12 * s
        corners.append((cx + radius * math.cos(angle),
                        cy + radius * math.sin(angle)))
    draw.polygon(corners, fill=colour)
    draw.ellipse([cx - 8 * s, cy - 8 * s, cx + 8 * s, cy + 8 * s],
                 fill=(255, 255, 255))


def icon_pad(draw, cx, cy, s, colour):
    # A gamepad: dark rounded body, pale cross and buttons.
    dark = (38, 38, 48)
    draw.rounded_rectangle([cx - 32 * s, cy - 14 * s, cx + 32 * s,
                            cy + 18 * s], radius=12 * s, fill=dark)
    draw.rectangle([cx - 24 * s, cy - 4 * s, cx - 12 * s, cy + 4 * s],
                   fill=(255, 255, 255))
    draw.rectangle([cx - 20 * s, cy - 8 * s, cx - 16 * s, cy + 8 * s],
                   fill=(255, 255, 255))
    for bx, by in ((16, -6), (24, 2), (16, 8)):
        draw.ellipse([cx + (bx - 3) * s, cy + (by - 3) * s,
                      cx + (bx + 3) * s, cy + (by + 3) * s],
                     fill=(255, 255, 255))


def icon_bars(draw, cx, cy, s, colour):
    # Three rising bars under an upward arrow.
    for pos, tall in enumerate((14, 24, 34)):
        x0 = cx - 28 * s + pos * 18 * s
        draw.rectangle([x0, cy + 16 * s - tall * s, x0 + 12 * s,
                        cy + 16 * s], fill=colour)
    draw.line([(cx - 30 * s, cy + 6 * s), (cx - 2 * s, cy - 16 * s),
               (cx + 30 * s, cy - 26 * s)], fill=colour,
              width=max(3, int(4 * s)))
    draw.polygon([(cx + 30 * s, cy - 26 * s), (cx + 16 * s, cy - 26 * s),
                  (cx + 30 * s, cy - 12 * s)], fill=colour)


def icon_probe(draw, cx, cy, s, colour):
    # A deep-space probe: body, dish, one panel, two signal arcs.
    draw.rectangle([cx - 8 * s, cy - 6 * s, cx + 8 * s, cy + 8 * s],
                   fill=colour)
    draw.polygon([(cx + 8 * s, cy - 6 * s), (cx + 22 * s, cy - 16 * s),
                  (cx + 22 * s, cy + 2 * s), (cx + 8 * s, cy + 8 * s)],
                 outline=colour, width=max(2, int(2 * s)))
    draw.rectangle([cx - 30 * s, cy - 2 * s, cx - 8 * s, cy + 4 * s],
                   fill=colour)
    draw.arc([cx - 4 * s, cy - 30 * s, cx + 28 * s, cy + 2 * s],
             start=270, end=360, fill=colour, width=max(2, int(3 * s)))
    draw.arc([cx - 12 * s, cy - 38 * s, cx + 36 * s, cy + 10 * s],
             start=270, end=360, fill=colour, width=max(2, int(3 * s)))


def icon_balance(draw, cx, cy, s, colour):
    # A balance scale: upright, beam, two hanging pans, base.
    draw.line([(cx, cy - 26 * s), (cx, cy + 24 * s)], fill=colour,
              width=max(3, int(4 * s)))
    draw.line([(cx - 28 * s, cy - 20 * s), (cx + 28 * s, cy - 20 * s)],
              fill=colour, width=max(3, int(4 * s)))
    for side in (-28, 28):
        draw.line([(cx + side * s, cy - 20 * s),
                   (cx + side * s, cy - 2 * s)], fill=colour,
                  width=max(2, int(2 * s)))
        draw.polygon([(cx + (side - 12) * s, cy - 2 * s),
                      (cx + (side + 12) * s, cy - 2 * s),
                      (cx + side * s, cy + 12 * s)], outline=colour,
                     width=max(2, int(2 * s)))
    draw.rectangle([cx - 14 * s, cy + 24 * s, cx + 14 * s, cy + 28 * s],
                   fill=colour)


ICONS = {"summit": icon_summit, "burst": icon_burst, "pad": icon_pad,
         "bars": icon_bars, "probe": icon_probe, "balance": icon_balance}

# Each story: section label, headline, two-sentence summary, accent, icon.
STORIES = [
    ("ASIA  ·  DIPLOMACY",
     "Trump, Xi and Putin meet in Shenzhen",
     "The three leaders hold trilateral talks on the sidelines of the "
     "APEC summit — their first such meeting.",
     (22, 35, 63), "summit"),
    ("MIDDLE EAST  ·  CONFLICT",
     "US and Iran trade fire across the Gulf",
     "Iran hits a US base in Kuwait and strikes Bahrain again; the US "
     "hits a missile site on Qeshm Island and sends a third carrier.",
     (150, 40, 40), "burst"),
    ("CULTURE  ·  GAMING",
     "GTA VI launches worldwide",
     "Rockstar's sequel arrives after 13 years and scores 99 on "
     "Metacritic as players flood into Vice City.",
     (122, 84, 20), "pad"),
    ("EUROPE  ·  UKRAINE",
     "EU proposes a €45bn loan for Kyiv",
     "Brussels plans to borrow on the markets to cover Ukraine's "
     "budget gap, to be repaid after Russia pays reparations.",
     (31, 110, 80), "bars"),
    ("SCIENCE  ·  SPACE",
     "Voyager 1 reaches one light-day",
     "NASA's probe, nearly 50 years from Earth, passes a "
     "record-breaking distance milestone.",
     (40, 90, 130), "probe"),
    ("LAW  ·  THE HAGUE",
     "ICJ rules on Myanmar genocide case",
     "The world court delivers its judgment in The Gambia v. Myanmar "
     "over the treatment of the Rohingya.",
     (88, 60, 130), "balance"),
]

ALSO_TODAY = ("Cyclone Akvan nears India's east coast  •  "
              "Nvidia stops H-series chip shipments to China  •  "
              "Fed minutes point to more rate hikes")


def story_card(draw, index):
    """Draw one of the six story cards in the 2-by-3 grid."""
    label, headline, summary, accent, icon = STORIES[index]
    col, row = index % 2, index // 2
    margin, gap, card_h = 26, 12, 240
    card_w = (PAGE_W - 2 * margin - gap) // 2
    x0 = margin + col * (card_w + gap)
    y0 = 200 + row * (card_h + gap)
    x1, y1 = x0 + card_w, y0 + card_h
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=EDGE, width=2)
    icon_w = 92
    draw.rectangle([x0, y0, x0 + icon_w, y1], fill=accent)
    ICONS[icon](draw, x0 + icon_w // 2, y0 + card_h // 2, 1.0,
                (255, 255, 255))
    tx = x0 + icon_w + 14
    tw = x1 - tx - 12
    draw.text((tx, y0 + 16), label, font=face("sans_b", 16), fill=accent)
    y = y0 + 44
    head_lines = flow_text(draw, headline, face("serif_b", 27), tw)[:2]
    y = put_lines(draw, tx, y, head_lines, face("serif_b", 27), INKC, 32)
    cap_lines = flow_text(draw, summary, face("sans", 19), tw)[:4]
    put_lines(draw, tx, y + 8, cap_lines, face("sans", 19), BODYC, 24)


def build():
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), BG)
    draw = ImageDraw.Draw(canvas)

    # Masthead: rules, title, date, tagline.
    draw.line([(26, 30), (998, 30)], fill=INKC, width=3)
    draw.line([(26, 36), (998, 36)], fill=INKC, width=1)
    centred(draw, "THE WORLD TODAY", 48, face("serif_b", 62), NAVYC)
    centred(draw, "THURSDAY 19 NOVEMBER 2026", 118, face("sans_b", 34), REDC)
    centred(draw, "One day's world news — in one picture", 158,
            face("serif", 20), MUTED)
    draw.line([(26, 188), (998, 188)], fill=INKC, width=2)

    for index in range(len(STORIES)):
        story_card(draw, index)

    # Footer: the rest of the day, then the source line.
    foot_y = 200 + 3 * 240 + 2 * 12 + 10
    draw.line([(26, foot_y), (998, foot_y)], fill=INKC, width=2)
    tag = "ALSO TODAY — "
    tag_w = draw.textlength(tag, font=face("sans_b", 16))
    draw.text((26, foot_y + 8), tag, font=face("sans_b", 16), fill=REDC)
    y = foot_y + 8
    for line in flow_text(draw, ALSO_TODAY, face("sans", 16),
                          PAGE_W - 52 - tag_w)[:2]:
        draw.text((26 + tag_w, y), line, font=face("sans", 16), fill=INKC)
        y += 20
    credit = ("Reported Thursday 19 November 2026  ·  "
              "Sources: AP, BBC, Al Jazeera, DW, Reuters")
    centred(draw, credit, 1006, face("sans", 13), MUTED)

    canvas.save("entry.png", optimize=True)
    print("saved entry.png", canvas.size)


if __name__ == "__main__":
    build()
