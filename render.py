#!/usr/bin/env python3
"""Render the make.fun news-image-20261121 entry: a one-day world newspaper.

Design: a broadsheet front page for Saturday 21 November 2026. A flat world
map up top carries six numbered pins for the day's biggest stories; below it,
six story cards (two rows of three) tell each story in a headline plus one
line; a footer ticker carries three more briefs. Everything is drawn with
Pillow from data in this file, so the image is fully reproducible.

Stories (all happened or first reported on 21 Nov 2026, cross-checked against
several news digests of the day):
  1. Russia's overnight attack on Ukraine: 400+ drones, 110 missiles; two
     Russian missiles and a suspected drone came down in Poland; PM Tusk
     calls it a deliberate provocation; NATO jets scrambled.
  2. AI sell-off: S&P 500 -3.7% and Nasdaq -5.28% into correction; Nvidia
     -14% as the SEC opens an accounting inquiry; Anthropic's record IPO
     slides on day two.
  3. ICJ rules 9-6 that Myanmar committed genocide against the Rohingya,
     the first time the court has held a state responsible; orders
     investigation and compensation.
  4. Trump defends his ties to Putin and Xi after the first three-way
     US-China-Russia summit in Shenzhen; calls the talks "very good".
  5. Magnitude 6.8 earthquake strikes Junin in central Peru; tremors felt
     320 km away in Lima.
  6. COP31 climate summit in Antalya misses its deadline; the draft drops
     any mention of fossil fuels.
Footer briefs: pancreatic-cancer pill trial (daraxonrasib), UK-EU trade and
youth-mobility deals, KL Rahul completing the SENA century set.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (179, 32, 44)
BLUE = (31, 78, 121)
OCEAN = (216, 230, 234)
LAND = (233, 221, 192)
LAND_EDGE = (138, 122, 90)
GREY = (90, 86, 76)
CARD_BG = (252, 250, 244)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading=None):
    """Draw lines left-aligned; returns the y just below the block."""
    lh = leading or int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- map data
# Simplified continent outlines as (lon, lat) pairs, drawn in an
# equirectangular projection. Deliberately stylised: a flat newspaper map,
# not a survey chart.
N_AMERICA = [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60),
             (-135, 58), (-130, 54), (-125, 49), (-124, 42), (-120, 34),
             (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-94, 17),
             (-90, 14), (-86, 12), (-83, 9), (-79, 9), (-80, 25),
             (-81, 31), (-76, 35), (-75, 39), (-70, 42), (-68, 45),
             (-65, 44), (-60, 47), (-55, 52), (-60, 55), (-65, 60),
             (-68, 58), (-78, 62), (-85, 66), (-92, 66), (-95, 69),
             (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68),
             (-22, 70), (-25, 76), (-35, 77), (-50, 76), (-58, 74),
             (-58, 70)]
S_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
             (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
             (-70, -52), (-66, -55), (-65, -50), (-62, -45), (-58, -38),
             (-52, -33), (-48, -28), (-41, -23), (-35, -9), (-35, -6),
             (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6),
             (-62, 9), (-68, 11), (-72, 12), (-76, 10)]
AFRICA = [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
          (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (35, 28),
          (37, 22), (39, 18), (43, 12), (48, 11), (51, 12), (46, 5),
          (41, 0), (40, -5), (40, -10), (36, -18), (33, -26), (28, -33),
          (20, -35), (17, -32), (15, -27), (12, -18), (13, -12),
          (12, -6), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)]
MADAGASCAR = [(44, -16), (47, -15), (50, -17), (49, -22), (45, -25),
              (43, -21)]
EURASIA = [(30, 62), (40, 68), (55, 68), (70, 72), (80, 73), (90, 75),
           (100, 77), (110, 74), (120, 73), (130, 72), (140, 72),
           (150, 70), (158, 66), (162, 60), (158, 55), (150, 59),
           (142, 55), (140, 50), (135, 45), (130, 42), (127, 40),
           (122, 38), (120, 34), (122, 30), (118, 25), (110, 21),
           (108, 18), (105, 10), (103, 8), (100, 8), (98, 12),
           (95, 16), (92, 21), (89, 22), (86, 20), (82, 17), (80, 13),
           (77, 8), (75, 12), (72, 20), (68, 23), (66, 25), (62, 25),
           (58, 26), (56, 27), (54, 26), (52, 28), (50, 29), (48, 30),
           (44, 29), (40, 28), (36, 36), (33, 36), (30, 36), (27, 37),
           (26, 38), (23, 36), (22, 37), (19, 40), (16, 40), (12, 42),
           (10, 44), (8, 44), (6, 43), (3, 43), (0, 40), (-2, 37),
           (-5, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
           (-2, 50), (0, 51), (3, 53), (5, 53), (8, 55), (8, 57),
           (10, 59), (12, 58), (18, 56), (21, 55), (24, 58), (28, 60)]
UK = [(-5, 50), (-3, 53), (-6, 55), (-5, 58), (-2, 57), (0, 54),
      (1, 51), (-1, 50)]
JAPAN = [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38),
         (141, 41), (143, 43), (145, 44), (142, 45), (140, 42),
         (139, 38), (137, 37), (134, 35), (131, 33)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (120, -34), (125, -32),
             (130, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
NEW_ZEALAND = [(167, -45), (170, -42), (174, -40), (177, -38),
               (175, -37), (173, -41), (170, -44), (167, -46)]
INDONESIA = [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8),
             (120, -10), (125, -9), (130, -3), (135, -3), (140, -4),
             (141, -8), (136, -9), (128, -8), (120, -6), (112, -7),
             (105, -6), (100, 2), (97, 5)]

CONTINENTS = [N_AMERICA, GREENLAND, S_AMERICA, AFRICA, MADAGASCAR,
              EURASIA, UK, JAPAN, AUSTRALIA, NEW_ZEALAND, INDONESIA]

# (number, label, lon, lat, label_dx, label_dy)
PINS = [
    (1, "KYIV & POLAND", 26, 51, 16, -32),
    (2, "NEW YORK", -74, 41, -118, 6),
    (3, "THE HAGUE", 4, 52, -102, 2),
    (4, "SHENZHEN", 114, 22, -96, 20),
    (5, "JUNIN, PERU", -75, -12, 14, -8),
    (6, "ANTALYA", 31, 37, 16, -6),
]


def project(lon, lat, box):
    """Equirectangular: lon -170..190, lat 78..-58 into box (x0,y0,x1,y1)."""
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170) / 360.0 * (x1 - x0)
    y = y0 + (78 - lat) / 136.0 * (y1 - y0)
    return (x, y)


def draw_map(draw, box):
    """Flat world map with graticule, continents and numbered story pins."""
    draw.rectangle(box, fill=OCEAN, outline=INK, width=2)
    # Graticule, faint.
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 78, box)
        draw.line([(x, box[1]), (x, box[3])], fill=(190, 205, 210), width=1)
    for lat in range(-60, 79, 30):
        _, y = project(0, lat, box)
        draw.line([(box[0], y), (box[2], y)], fill=(190, 205, 210), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # Red dashed arc: missile path from Russia toward Poland.
    import math
    p0 = project(42, 56, box)
    p2 = project(20, 52, box)
    for t in range(0, 101, 5):
        u = t / 100.0
        x = p0[0] + (p2[0] - p0[0]) * u
        y = p0[1] + (p2[1] - p0[1]) * u - 18 * math.sin(math.pi * u)
        draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=RED)
    # Pins with numbers and labels.
    lab_f = font(SANS_B, 15)
    num_f = font(SANS_B, 16)
    for num, label, lon, lat, dx, dy in PINS:
        cx, cy = project(lon, lat, box)
        r = 13
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        tw = draw.textlength(str(num), font=num_f)
        draw.text((cx - tw / 2, cy - 11), str(num), font=num_f,
                  fill=(255, 255, 255))
        draw.text((cx + dx, cy + dy), label, font=lab_f, fill=INK)


# ---------------------------------------------------------------- masthead
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 8], fill=RED)
    title_f = font(SERIF, 88)
    title = "THE WORLD"
    tw = draw.textlength(title, font=title_f)
    draw.text(((W - tw) / 2, 16), title, font=title_f, fill=INK)
    date_f = font(SANS_B, 30)
    date = "SATURDAY, 21 NOVEMBER 2026"
    tw = draw.textlength(date, font=date_f)
    draw.text(((W - tw) / 2, 112), date, font=date_f, fill=RED)
    draw.line([(24, 148), (W - 24, 148)], fill=INK, width=3)
    draw.line([(24, 153), (W - 24, 153)], fill=INK, width=1)


# ---------------------------------------------------------------- story cards
STORIES = [
    ("1", "KYIV  •  WAR IN EUROPE", "RUSSIAN MISSILES FALL IN POLAND",
     "400 drones, 110 missiles hit Ukraine; two fell in Poland. "
     "Warsaw: provocation."),
    ("2", "NEW YORK  •  MARKETS", "AI SELL-OFF DRAGS STOCKS INTO CORRECTION",
     "S&P 500 falls 3.7% and Nasdaq 5.3%; Nvidia drops 14% as the SEC "
     "opens an accounting inquiry."),
    ("3", "THE HAGUE  •  JUSTICE", "MYANMAR GUILTY OF GENOCIDE",
     "The UN court rules 9-6 that Myanmar committed genocide against the "
     "Rohingya."),
    ("4", "SHENZHEN  •  DIPLOMACY", "TRUMP DEFENDS PUTIN AND XI TIES",
     "After the first US-China-Russia summit, Trump calls the talks "
     "\u201cvery good\u201d."),
    ("5", "PERU  •  DISASTER", "QUAKE 6.8 SHAKES PERU",
     "A magnitude 6.8 earthquake strikes Junin in the Andes; tremors are "
     "felt 320 km away in Lima."),
    ("6", "ANTALYA  •  CLIMATE", "COP31 MISSES ITS DEADLINE",
     "Climate talks overrun in Turkey as the draft drops any mention of "
     "fossil fuels."),
]


def draw_cards(draw):
    kick_f = font(SANS_B, 15)
    head_f = font(SANS_B, 25)
    body_f = font(SANS, 17)
    num_f = font(SANS_B, 18)
    gx, gy = 24, 460
    cw, chh, gap = 318, 230, 8
    for i, (num, kicker, headline, body) in enumerate(STORIES):
        col, row = i % 3, i // 3
        x = gx + col * (cw + gap)
        y = gy + row * (chh + gap)
        draw.rectangle([x, y, x + cw, y + chh], fill=CARD_BG,
                       outline=INK, width=2)
        draw.rectangle([x, y, x + cw, y + 5], fill=RED)
        # Number badge + kicker.
        draw.ellipse([x + 12, y + 16, x + 40, y + 44], fill=RED)
        tw = draw.textlength(num, font=num_f)
        draw.text((x + 26 - tw / 2, y + 19), num, font=num_f,
                  fill=(255, 255, 255))
        draw.text((x + 50, y + 21), kicker, font=kick_f, fill=BLUE)
        # Headline, wrapped to the card width.
        lines = wrap(draw, headline, head_f, cw - 24)
        yy = draw_text_block(draw, x + 12, y + 56, lines, head_f, INK,
                             leading=29)
        draw.line([(x + 12, yy + 4), (x + 62, yy + 4)], fill=RED, width=3)
        # One-line story, wrapped to at most three lines.
        lines = wrap(draw, body, body_f, cw - 24)[:3]
        draw_text_block(draw, x + 12, yy + 14, lines, body_f, INK,
                        leading=21)


# ---------------------------------------------------------------- footer
def draw_footer(draw):
    y = 936
    draw.line([(24, y), (W - 24, y)], fill=INK, width=3)
    draw.line([(24, y + 5), (W - 24, y + 5)], fill=INK, width=1)
    tick_f = font(SANS_B, 17)
    tick = ("ALSO TODAY:  CANCER PILL MAKES TUMOURS UNDETECTABLE IN 1 IN 12 "
            "PATIENTS  •  UK AND EU SEAL TRADE AND YOUTH-MOBILITY DEALS  •  "
            "KL RAHUL COMPLETES THE SENA CENTURY SET")
    lines = wrap(draw, tick, tick_f, W - 48)
    yy = draw_text_block(draw, 24, y + 14, lines, tick_f, INK, leading=22)
    cred_f = font(SANS, 13)
    cred = "THE WORLD  •  21 NOVEMBER 2026  •  ONE DAY, SIX STORIES THAT MOVED THE WORLD"
    tw = draw.textlength(cred, font=cred_f)
    draw.text(((W - tw) / 2, yy + 6), cred, font=cred_f, fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_map(draw, (24, 160, W - 24, 452))
    draw.text((24, 162), "", font=font(SANS, 12), fill=INK)
    draw_cards(draw)
    draw_footer(draw)
    # Thin outer border.
    draw.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
