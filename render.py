#!/usr/bin/env python3
"""Render entry.png for news-image-20261122-v6 — 'the map, perfected'.

A one-image front page of Sunday 22 November 2026: a hand-drawn world map
(equirectangular lon/lat polygons) with eleven numbered story markers and a
two-column legend. Drawn entirely with Pillow; deterministic output.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (26, 26, 26)
RED = (163, 22, 33)
OCEAN = (219, 228, 231)
LAND = (176, 194, 163)
LAND_EDGE = (110, 128, 96)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

# ---------------------------------------------------------------- map geometry
# Map panel (pixels)
MX0, MY0, MX1, MY1 = 28, 176, 996, 676
# Longitude/latitude window projected onto the panel
LON0, LON1 = -170.0, 182.0
LAT0, LAT1 = 84.0, -57.0


def px(lon, lat):
    x = MX0 + (lon - LON0) / (LON1 - LON0) * (MX1 - MX0)
    y = MY0 + (LAT0 - lat) / (LAT0 - LAT1) * (MY1 - MY0)
    return (x, y)


def poly(points):
    return [px(lon, lat) for lon, lat in points]


NORTH_AMERICA = [
    (-166, 68), (-161, 70), (-156, 71), (-148, 70), (-140, 70), (-132, 69),
    (-125, 71), (-117, 72), (-110, 73), (-102, 73), (-95, 79), (-90, 79),
    (-85, 79), (-82, 73), (-88, 69), (-93, 66), (-95, 63), (-92, 58),
    (-88, 55), (-84, 55), (-82, 51), (-79, 51), (-80, 47), (-76, 44),
    (-71, 45), (-69, 44), (-70, 42), (-73, 40), (-74, 39), (-76, 36),
    (-76, 35), (-79, 33), (-81, 31), (-81, 26), (-80, 27), (-82, 28),
    (-84, 30), (-87, 30), (-89, 30), (-92, 29), (-95, 29), (-97, 28),
    (-97, 26), (-97, 23), (-95, 19), (-94, 18), (-91, 19), (-88, 16),
    (-85, 12), (-83, 9), (-79, 9), (-81, 12), (-84, 15), (-88, 14),
    (-92, 15), (-96, 16), (-101, 18), (-104, 20), (-105, 22), (-108, 24),
    (-110, 24), (-112, 29), (-114, 31), (-117, 33), (-120, 34), (-122, 37),
    (-124, 42), (-124, 46), (-123, 49), (-127, 52), (-131, 55), (-136, 57),
    (-141, 60), (-147, 61), (-152, 59), (-156, 58), (-160, 59), (-164, 60),
    (-166, 61), (-168, 66),
]
GREENLAND = [
    (-46, 60), (-42, 62), (-40, 64), (-32, 68), (-22, 70), (-18, 74),
    (-22, 79), (-32, 82), (-48, 81), (-56, 78), (-57, 74), (-54, 70),
    (-52, 65), (-53, 62),
]
SOUTH_AMERICA = [
    (-78, 7), (-77, 4), (-80, 1), (-81, -4), (-79, -8), (-76, -14),
    (-72, -18), (-70, -20), (-70, -27), (-71, -33), (-72, -38), (-73, -44),
    (-74, -50), (-71, -54), (-68, -55), (-67, -51), (-65, -45), (-62, -41),
    (-58, -37), (-52, -33), (-49, -29), (-42, -23), (-40, -21), (-39, -15),
    (-35, -8), (-38, -5), (-44, -3), (-50, 0), (-52, 4), (-56, 6),
    (-60, 8), (-64, 11), (-68, 11), (-72, 12), (-76, 10), (-78, 8),
]
EUROPE = [
    (-9, 37), (-6, 36), (-2, 37), (0, 38), (2, 40), (3, 42), (0, 43),
    (-2, 44), (-1, 46), (-2, 48), (-5, 48), (-4, 49), (-1, 50), (2, 51),
    (4, 52), (6, 53), (8, 54), (8, 56), (8, 57), (10, 58), (6, 58),
    (5, 60), (5, 61), (9, 63), (12, 65), (13, 67), (14, 68), (19, 69),
    (25, 71), (31, 70), (38, 68), (44, 67), (46, 65), (45, 60), (42, 56),
    (39, 53), (36, 51), (33, 50), (30, 50), (28, 47), (29, 46), (25, 45),
    (28, 41), (26, 40), (23, 39), (23, 36), (22, 37), (19, 40), (16, 40),
    (15, 38), (16, 39), (18, 40), (19, 42), (15, 44), (13, 45), (12, 44),
    (10, 44), (8, 44), (7, 43), (3, 43),
]
ITALY = [
    (8, 44), (10, 44), (13, 45), (13, 43), (14, 42), (16, 40), (18, 40),
    (17, 40), (16, 38), (16, 39), (15, 40), (13, 41), (11, 43), (9, 44),
]
BRITAIN = [
    (-5, 50), (-3, 51), (-1, 52), (0, 53), (-1, 55), (-2, 57), (-4, 58),
    (-6, 57), (-5, 55), (-5, 53), (-3, 53), (-5, 51),
]
AFRICA = [
    (-6, 35), (-2, 35), (3, 37), (10, 37), (11, 34), (15, 32), (20, 32),
    (25, 32), (30, 31), (32, 31), (33, 29), (34, 28), (35, 25), (37, 22),
    (38, 21), (39, 20), (40, 15), (43, 12), (46, 11), (50, 12), (51, 11),
    (48, 7), (44, 2), (41, -2), (40, -7), (40, -12), (39, -17), (37, -21),
    (36, -25), (33, -27), (31, -29), (29, -32), (26, -34), (20, -35),
    (19, -34), (17, -32), (16, -29), (15, -26), (14, -21), (13, -17),
    (12, -13), (13, -9), (13, -5), (10, -1), (9, 2), (9, 4), (6, 4),
    (3, 6), (-1, 5), (-4, 5), (-8, 5), (-12, 8), (-15, 10), (-17, 13),
    (-17, 16), (-16, 20), (-16, 24), (-14, 27), (-11, 30), (-9, 32),
]
MADAGASCAR = [
    (44, -13), (47, -14), (49, -15), (50, -17), (48, -21), (47, -23),
    (45, -25), (44, -24), (43, -21), (43, -17), (44, -14),
]
ASIA = [
    (27, 37), (30, 36), (33, 36), (36, 36), (35, 30), (34, 28), (36, 24),
    (38, 21), (40, 15), (42, 13), (44, 12), (49, 12), (53, 15), (55, 17),
    (58, 21), (59, 22), (59, 23), (57, 25), (54, 26), (52, 25), (50, 27),
    (50, 29), (48, 30), (51, 29), (54, 27), (57, 27), (59, 25), (61, 25),
    (64, 25), (66, 25), (68, 23), (70, 22), (72, 20), (73, 17), (74, 13),
    (76, 9), (77, 8), (79, 10), (80, 13), (81, 16), (84, 19), (87, 21),
    (89, 22), (91, 22), (92, 20), (92, 16), (94, 16), (97, 14), (99, 10),
    (100, 7), (101, 5), (103, 8), (105, 9), (107, 11), (109, 14),
    (107, 16), (109, 19), (108, 21), (110, 20), (113, 22), (116, 23),
    (118, 25), (120, 27), (121, 29), (122, 31), (120, 33), (121, 35),
    (119, 36), (122, 37), (124, 39), (126, 40), (127, 40), (126, 38),
    (127, 35), (129, 33), (130, 34), (129, 36), (127, 39), (130, 42),
    (132, 43), (135, 45), (138, 46), (141, 45), (140, 42), (142, 46),
    (142, 50), (143, 52), (146, 52), (150, 52), (152, 55), (156, 51),
    (157, 53), (160, 55), (162, 58), (162, 60), (166, 60), (170, 60),
    (173, 64), (178, 65), (179, 66), (178, 68), (173, 69), (168, 69),
    (162, 70), (156, 70), (150, 71), (143, 72), (136, 72), (129, 72),
    (122, 73), (115, 73), (108, 74), (100, 77), (93, 76), (86, 74),
    (79, 73), (72, 73), (68, 70), (66, 69), (66, 66), (67, 62), (66, 58),
    (64, 55), (60, 55), (56, 52), (52, 50), (49, 48), (46, 47), (41, 47),
    (38, 47), (35, 46), (32, 46), (30, 45), (28, 42), (30, 41), (27, 41),
]
SUMATRA = [
    (95, 5), (98, 3), (100, 0), (102, -2), (104, -4), (106, -6), (104, -5),
    (101, -3), (98, 1), (96, 4),
]
BORNEO = [
    (109, 1), (110, 3), (113, 4), (116, 6), (118, 4), (119, 1), (118, -1),
    (116, -3), (113, -3), (110, -2), (109, 0),
]
JAVA = [
    (106, -6), (109, -6), (112, -7), (114, -8), (114, -9), (110, -8),
    (107, -8), (106, -7),
]
SULAWESI = [
    (119, 0), (120, 1), (122, 0), (120, -1), (121, -3), (120, -5),
    (119, -3), (119, -1),
]
NEW_GUINEA = [
    (131, -1), (134, -2), (138, -2), (141, -3), (144, -4), (147, -6),
    (150, -9), (149, -10), (146, -8), (142, -8), (138, -6), (134, -4),
    (132, -3),
]
JAPAN = [
    (130, 31), (131, 32), (133, 34), (135, 34), (137, 35), (139, 36),
    (140, 37), (141, 39), (141, 41), (142, 43), (143, 44), (142, 45),
    (141, 44), (140, 42), (140, 40), (139, 38), (137, 37), (135, 35),
    (133, 34), (131, 33), (130, 32),
]
AUSTRALIA = [
    (113, -22), (114, -26), (115, -31), (115, -34), (117, -35), (120, -34),
    (124, -33), (129, -32), (132, -32), (134, -33), (136, -35), (137, -35),
    (138, -36), (140, -38), (144, -38), (146, -39), (149, -38), (150, -37),
    (152, -33), (153, -30), (153, -27), (152, -25), (149, -20), (146, -19),
    (143, -17), (142, -14), (142, -11), (141, -13), (141, -17), (140, -18),
    (137, -16), (136, -15), (135, -12), (133, -11), (131, -12), (129, -13),
    (126, -14), (124, -16), (122, -17), (119, -20), (116, -21), (114, -22),
]
NEW_ZEALAND = [
    (167, -45), (169, -44), (171, -42), (173, -41), (174, -39), (176, -38),
    (175, -37), (173, -39), (172, -41), (170, -43), (168, -46),
]

LANDMASSES = [
    NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, ITALY, BRITAIN,
    AFRICA, MADAGASCAR, ASIA, SUMATRA, BORNEO, JAVA, SULAWESI, NEW_GUINEA,
    JAPAN, AUSTRALIA, NEW_ZEALAND,
]

# name -> (lon, lat, disc offset dx, dy)  offsets declutter the Europe cluster
MARKERS = {
    1: (30.7, 36.9, 0, 0),      # Antalya, Turkey (lead)
    2: (19.0, 52.0, -16, -6),   # Poland
    3: (20.1, 32.1, 0, 4),      # Benghazi, Libya
    4: (50.6, 26.2, 6, 6),      # Bahrain / Hormuz
    5: (95.5, 17.5, 0, 0),      # Myanmar
    6: (30.5, 50.4, 16, -8),    # Kyiv, Ukraine
    7: (5.5, 5.0, 0, 0),        # Nigeria
    8: (-107.5, 24.8, 0, 0),    # Sinaloa, Mexico
    9: (107.0, -6.8, 0, 0),     # Indonesia
    10: (-1.5, 52.8, -4, 0),    # Britain / EU
    11: (127.8, 26.3, 10, 10),  # Okinawa, Japan
}

CONTINENT_LABELS = [
    ("NORTH AMERICA", -103, 47),
    ("SOUTH AMERICA", -60, -22),
    ("EUROPE", -14, 64),
    ("AFRICA", 23, -4),
    ("ASIA", 88, 52),
    ("AUSTRALIA", 134, -26),
]

# ------------------------------------------------------------------- drawing
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def centered(text, y, fnt, fill, cx=W // 2):
    box = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (box[2] - box[0]) / 2 - box[0], y), text, font=fnt, fill=fill)


def marker(cx, cy, num, r=19, lead=False):
    """Red disc with white halo ring and bold white number."""
    if lead:  # clean red outer ring, drawn first so the disc sits inside it
        rr = r + 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=RED, width=4)
    d.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4], fill=WHITE)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    f = font(SANS_B, 21 if num < 10 else 19)
    t = str(num)
    box = d.textbbox((0, 0), t, font=f)
    d.text((cx - (box[2] - box[0]) / 2 - box[0],
            cy - (box[3] - box[1]) / 2 - box[1]), t, font=f, fill=WHITE)


# Masthead
centered("THE WORLD IN ONE IMAGE", 18, font(SERIF_B, 54), INK)

# Date band
d.rectangle([0, 88, W, 164], fill=RED)
centered("SUNDAY 22 NOVEMBER 2026", 100, font(SANS_B, 55), WHITE)

# Map panel
d.rectangle([MX0, MY0, MX1, MY1], fill=OCEAN)
for shape in LANDMASSES:
    d.polygon(poly(shape), fill=LAND, outline=LAND_EDGE, width=2)

lab_f = font(SANS_B, 17)
for name, lon, lat in CONTINENT_LABELS:
    x, y = px(lon, lat)
    box = d.textbbox((0, 0), name, font=lab_f)
    d.text((x - (box[2] - box[0]) / 2, y), name, font=lab_f, fill=(104, 118, 92))

# True-location dots under offset discs, then the discs
for num, (lon, lat, dx, dy) in MARKERS.items():
    x, y = px(lon, lat)
    if dx or dy:
        d.line([x, y, x + dx, y + dy], fill=RED, width=2)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=RED, outline=WHITE, width=1)
for num, (lon, lat, dx, dy) in MARKERS.items():
    x, y = px(lon, lat)
    if num == 1:
        marker(x + dx, y + dy, num, r=25, lead=True)
    else:
        marker(x + dx, y + dy, num, r=19)

# -------------------------------------------------------------------- legend
LY = 692
# Lead line, full width
marker(52, LY + 24, 1, r=23)
d.text((92, LY), "COP31 CLIMATE TALKS END WITHOUT A DEAL",
       font=font(SANS_B, 30), fill=INK)
d.text((94, LY + 38),
       "Antalya, Turkey — nearly 200 nations split over fossil fuels and finance",
       font=font(SANS, 21), fill=GREY)
d.line([28, LY + 72, 996, LY + 72], fill=INK, width=2)

ENTRIES = [
    (2, "MISSILES LAND IN POLAND", "NATO calls it a violation"),
    (3, "SEA DRONES HIT WARSHIP", "Russian ship at Benghazi, Libya"),
    (4, "IRAN ATTACK IN BAHRAIN", "Plant hit; tankers near Hormuz"),
    (5, "ICJ: MYANMAR GENOCIDE", "Court rules on the Rohingya"),
    (6, "FIVE KILLED IN UKRAINE", "Kyiv flats; hometown struck"),
    (7, "FUNERAL BOAT CAPSIZES", "Nigeria: at least 24 dead"),
    (8, "CARTEL LEADER CAPTURED", "Mexico: El Chapo Isidro; 11 dead"),
    (9, "SEARCH FOR 34 MISSING", "Indonesia candy factory fire"),
    (10, "BRITAIN & EU: CLOSER TIES", "Major post-Brexit agreement"),
    (11, "SHURI CASTLE RESTORED", "Okinawa hall, 7 years after fire"),
]
HEAD_F = font(SANS_B, 22)
CAP_F = font(SANS, 19)
COL_X = [28, 524]
ROW_Y = LY + 88
PITCH = 45
for i, (num, head, cap) in enumerate(ENTRIES):
    col = 0 if i < 5 else 1
    row = i % 5
    x = COL_X[col]
    y = ROW_Y + row * PITCH
    marker(x + 15, y + 14, num, r=15)
    d.text((x + 40, y), head, font=HEAD_F, fill=INK)
    d.text((x + 41, y + 26), cap, font=CAP_F, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png")
