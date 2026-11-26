#!/usr/bin/env python3
"""Render the make.fun news-image-20261126 front page (1024x1024 PNG).

Deterministic: no randomness, no timestamps, fixed drawing order.
Only PIL + the DejaVu fonts shipped on this machine.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

CREAM = (247, 241, 222)
PAPER = (252, 248, 236)
INK = (20, 20, 20)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
BLUE = (29, 78, 216)
GREEN = (27, 122, 61)
AMBER = (180, 83, 9)
TEAL = (13, 115, 119)
SKY = (186, 214, 235)
SAND = (232, 220, 186)
GREY = (90, 90, 90)
LIGHTGREY = (220, 212, 190)

BADGE_COLORS = {
    "CONFIRMED": GREEN,
    "OFFICIAL": BLUE,
    "REPORTED": AMBER,
    "CLAIM": RED,
}


def font(size, bold=False, serif=False):
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit_font(draw, text, max_w, start, bold=False, serif=False):
    size = start
    while size > 8 and draw.textlength(text, font=font(size, bold, serif)) > max_w:
        size -= 1
    return font(size, bold, serif)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def draw_wrapped(draw, text, fnt, x, y, max_w, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.25)
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=fnt, fill=fill)
    return y + len(lines) * lh


def badge(draw, x, y, label, h=13):
    """Certainty badge; returns width used."""
    fnt = font(8, bold=True)
    w = int(draw.textlength(label, font=fnt)) + 10
    color = BADGE_COLORS[label]
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=color)
    draw.text((x + 5, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


def scene_sky(draw, x, y, w, h, sky_color):
    draw.rectangle([x, y, x + w, y + h], fill=sky_color)


def scene_ground(draw, x, y, w, h, color):
    draw.rectangle([x, y, x + w, y + h], fill=color)


# ---------------------------------------------------------------- scenes
def scene_tariff(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (198, 222, 240))
    scene_ground(d, x, y + h - 18, w, 18, (120, 140, 160))
    # cargo ship hull + containers
    d.polygon([(x + 12, y + h - 34), (x + w - 12, y + h - 34),
               (x + w - 26, y + h - 18), (x + 26, y + h - 18)], fill=(139, 0, 0))
    for i, c in enumerate([(178, 34, 34), (29, 78, 216), (27, 122, 61), (232, 180, 40)]):
        cx = x + 22 + i * 34
        d.rectangle([cx, y + h - 58, cx + 30, y + h - 36], fill=c, outline=INK)
    # big % sign
    d.text((x + w - 52, y + 4), "%", font=font(30, bold=True), fill=RED)


def scene_gulf(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (240, 200, 130))
    scene_ground(d, x, y + h - 16, w, 16, (90, 70, 50))
    # refinery towers
    for i, tx in enumerate([x + 18, x + 52, x + 88]):
        d.rectangle([tx, y + 22 + i * 6, tx + 22, y + h - 16], fill=(70, 70, 70))
        d.rectangle([tx + 4, y + 12 + i * 6, tx + 18, y + 24 + i * 6], fill=(50, 50, 50))
    # flame
    d.polygon([(x + w - 46, y + 30), (x + w - 30, y + 6), (x + w - 14, y + 30)],
              fill=(255, 140, 0))
    d.polygon([(x + w - 40, y + 30), (x + w - 30, y + 14), (x + w - 20, y + 30)],
              fill=(255, 220, 0))
    # tanker ship on the water, hull low in the frame
    d.polygon([(x + 8, y + h - 26), (x + 78, y + h - 26),
               (x + 70, y + h - 16), (x + 16, y + h - 16)], fill=(139, 0, 0))
    d.rectangle([x + 18, y + h - 38, x + 34, y + h - 26], fill=(200, 200, 200))
    d.rectangle([x + 40, y + h - 34, x + 68, y + h - 26], fill=(29, 78, 216))
    # oil barrel with $ — the market figure, not the claim
    d.ellipse([x + w - 78, y + h - 34, x + w - 52, y + h - 16], fill=(20, 20, 20))
    d.text((x + w - 74, y + h - 30), "$", font=font(11, bold=True), fill=(255, 255, 255))


def scene_cairo(d, x, y, w, h):
    # AFTERMATH, not the blaze: the fire burned Wednesday night; on 26 Nov
    # officials count the dead among the charred wreckage. No live flames.
    scene_sky(d, x, y, w, h, (215, 205, 190))
    scene_ground(d, x, y + h - 16, w, 16, (50, 50, 50))
    # scorched patch of road
    d.ellipse([x + 10, y + h - 26, x + w - 10, y + h - 10], fill=(30, 30, 30))
    # charred tanker: blackened tank + cab, tilted, wheels askew
    d.rounded_rectangle([x + 16, y + h - 50, x + w - 60, y + h - 22], radius=12,
                        fill=(60, 60, 60), outline=INK)
    d.rectangle([x + w - 58, y + h - 48, x + w - 16, y + h - 22], fill=(90, 40, 40),
                outline=INK)
    d.rectangle([x + w - 52, y + h - 44, x + w - 34, y + h - 34], fill=(120, 120, 120))
    for wx in (x + 30, x + 78, x + w - 36):
        d.ellipse([wx, y + h - 24, wx + 16, y + h - 8], fill=INK)
    # thin smoke wisps only — the fire is out
    for i, (sx, sy, sr) in enumerate([(x + 90, y + 8, 7), (x + 104, y + 16, 5),
                                      (x + 78, y + 18, 4)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(160, 160, 160))
    # two wrecked cars beside the tanker
    d.rectangle([x + 150, y + h - 30, x + 186, y + h - 18], fill=(40, 40, 40))


def scene_eu(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (29, 78, 216))
    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        import math
        a = math.pi * 2 * i / 12 - math.pi / 2
        sx, sy = cx + int(30 * math.cos(a)), cy + int(30 * math.sin(a))
        d.polygon([(sx, sy - 4), (sx + 1, sy - 1), (sx + 4, sy), (sx + 1, sy + 1),
                   (sx, sy + 4), (sx - 1, sy + 1), (sx - 4, sy), (sx - 1, sy - 1)],
                  fill=(255, 220, 0))
    d.text((cx - 11, cy - 13), "€", font=font(24, bold=True), fill=(255, 255, 255))


def scene_uk(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (186, 214, 235))
    scene_ground(d, x, y + h - 12, w, 12, (27, 122, 61))
    # house
    d.rectangle([x + 14, y + 22, x + 66, y + h - 12], fill=(178, 34, 34))
    d.polygon([(x + 8, y + 24), (x + 40, y + 6), (x + 72, y + 24)], fill=(90, 30, 30))
    d.rectangle([x + 34, y + 36, x + 46, y + h - 12], fill=(60, 40, 20))
    # lightning bolt + pound
    d.polygon([(x + 92, y + 8), (x + 78, y + 30), (x + 88, y + 30),
               (x + 76, y + 50), (x + 96, y + 26), (x + 86, y + 26)], fill=(255, 220, 0))
    d.text((x + w - 34, y + h - 26), "£", font=font(22, bold=True), fill=INK)


def scene_greece(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (220, 235, 245))
    scene_ground(d, x, y + h - 12, w, 12, (150, 150, 150))
    # marching crowd: heads + bodies + placard
    for i, px in enumerate([x + 16, x + 44, x + 72, x + 100, x + 128]):
        d.ellipse([px, y + 18, px + 14, y + 32], fill=(240, 200, 160))
        d.rectangle([px - 2, y + 34, px + 16, y + h - 12],
                    fill=[RED, BLUE, GREEN, (232, 180, 40), (90, 90, 90)][i])
    d.rectangle([x + 150, y + 8, x + 190, y + 22], fill=(255, 255, 255), outline=INK)
    d.text((x + 154, y + 10), "STRIKE", font=font(8, bold=True), fill=RED)


def scene_canary(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (135, 206, 235))
    # sea
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(29, 78, 216))
    d.arc([x + 6, y + h - 22, x + 60, y + h - 6], 0, 180, fill=(255, 255, 255), width=2)
    d.arc([x + 120, y + h - 22, x + 174, y + h - 6], 0, 180, fill=(255, 255, 255), width=2)
    # crowded wooden dinghy — no sail, no mast: a migrant boat, not a yacht
    d.polygon([(x + 34, y + h - 42), (x + 166, y + h - 42), (x + 152, y + h - 24),
               (x + 48, y + h - 24)], fill=(120, 80, 40))
    d.rectangle([x + 34, y + h - 42, x + 166, y + h - 36], fill=(90, 60, 30))
    # many people packed shoulder to shoulder
    for px in (x + 44, x + 62, x + 80, x + 98, x + 116, x + 134, x + 150):
        d.ellipse([px, y + h - 56, px + 11, y + h - 45], fill=(240, 200, 160))
        d.rectangle([px - 1, y + h - 45, px + 12, y + h - 40],
                    fill=[RED, BLUE, GREEN, (232, 180, 40)][px % 4])


def scene_nigeria(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (220, 240, 220))
    scene_ground(d, x, y + h - 12, w, 12, (120, 120, 120))
    # lab flask
    d.polygon([(x + 84, y + 8), (x + 112, y + 8), (x + 112, y + 22),
               (x + 132, y + h - 14), (x + 64, y + h - 14), (x + 84, y + 22)],
              fill=(255, 255, 255), outline=INK)
    d.polygon([(x + 72, y + h - 24), (x + 124, y + h - 24), (x + 120, y + h - 16),
               (x + 76, y + h - 16)], fill=(27, 122, 61))
    # seized sacks
    for i, sx in enumerate([x + 14, x + 44]):
        d.ellipse([sx, y + h - 30, sx + 26, y + h - 12], fill=(232, 180, 40), outline=INK)
    d.text((x + 150, y + 10), "$227M", font=font(13, bold=True), fill=RED)


def scene_space(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (15, 23, 42))
    for sx, sy in [(x + 12, y + 8), (x + 40, y + 20), (x + 170, y + 10),
                   (x + 150, y + 30), (x + 70, y + 6), (x + 190, y + 26)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # station: hub + panels (crew already aboard; NO launch rocket —
    # Shenzhou-24 launched 25 Nov and docked the same day)
    d.rectangle([x + 70, y + 18, x + 130, y + 34], fill=(200, 200, 200), outline=INK)
    d.rectangle([x + 30, y + 22, x + 68, y + 30], fill=(29, 78, 216))
    d.rectangle([x + 132, y + 22, x + 170, y + 30], fill=(29, 78, 216))
    d.ellipse([x + 92, y + 8, x + 108, y + 20], fill=(255, 220, 0))
    # docked capsule beneath the hub (no flame, no liftoff)
    d.rounded_rectangle([x + 92, y + 38, x + 108, y + 54], radius=4,
                        fill=(255, 255, 255), outline=INK)
    # small Pakistan flag: first Pakistani astronaut aboard
    d.rectangle([x + 14, y + 40, x + 44, y + 56], fill=(27, 122, 61), outline=INK)
    d.ellipse([x + 20, y + 44, x + 30, y + 52], fill=(255, 255, 255))
    d.ellipse([x + 23, y + 44, x + 32, y + 52], fill=(27, 122, 61))


def scene_korea(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (220, 230, 240))
    scene_ground(d, x, y + h - 12, w, 12, (100, 100, 100))
    # bank building
    d.rectangle([x + 50, y + 18, x + 150, y + h - 12], fill=(230, 230, 230), outline=INK)
    d.polygon([(x + 44, y + 20), (x + 100, y + 4), (x + 156, y + 20)], fill=RED)
    for i in range(3):
        d.rectangle([x + 62 + i * 28, y + 30, x + 78 + i * 28, y + h - 12], fill=(29, 78, 216))
    # rising arrow
    d.line([x + 12, y + h - 20, x + 34, y + 26, x + 48, y + 32], fill=GREEN, width=4)
    d.polygon([(x + 34, y + 18), (x + 48, y + 26), (x + 34, y + 34)], fill=GREEN)


def scene_storm(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (120, 140, 170))
    # clouds
    for cx, cy in [(x + 20, y + 10), (x + 90, y + 6), (x + 150, y + 14)]:
        d.ellipse([cx, cy, cx + 44, cy + 18], fill=(230, 230, 230))
    # rain
    for rx in range(x + 10, x + w - 10, 18):
        d.line([rx, y + 30, rx - 4, y + 42], fill=(29, 78, 216), width=2)
    # calendar: parade moved to Sat 28 Nov — no balloon flies on 26 Nov
    d.rectangle([x + 74, y + h - 34, x + 126, y + h - 10], fill=(255, 255, 255), outline=INK)
    d.rectangle([x + 74, y + h - 34, x + 126, y + h - 24], fill=RED)
    d.text((x + 92, y + h - 22), "28", font=font(13, bold=True), fill=INK)
    d.text((x + 88, y + h - 33), "NOV", font=font(8, bold=True), fill=(255, 255, 255))


def scene_colombia(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (255, 220, 150))
    scene_ground(d, x, y + h - 12, w, 12, (90, 90, 90))
    # building + door
    d.rectangle([x + 40, y + 10, x + 150, y + h - 12], fill=(200, 180, 140), outline=INK)
    d.rectangle([x + 86, y + 30, x + 106, y + h - 12], fill=(60, 40, 20))
    for wy in (y + 16, y + 34):
        d.rectangle([x + 50, wy, x + 70, wy + 10], fill=SKY, outline=INK)
        d.rectangle([x + 120, wy, x + 140, wy + 10], fill=SKY, outline=INK)
    # shield with check
    d.polygon([(x + 162, y + 12), (x + 186, y + 12), (x + 186, y + 28),
               (x + 174, y + 40), (x + 162, y + 28)], fill=GREEN)
    d.line([x + 166, y + 24, x + 172, y + 30, x + 182, y + 18], fill=(255, 255, 255), width=3)
    # freed people
    for px in (x + 14, x + 26):
        d.ellipse([px, y + h - 26, px + 9, y + h - 17], fill=(240, 200, 160))
        d.rectangle([px - 1, y + h - 16, px + 10, y + h - 12], fill=BLUE)


def scene_fcc(d, x, y, w, h):
    scene_sky(d, x, y, w, h, (15, 23, 42))
    for sx, sy in [(x + 10, y + 8), (x + 60, y + 6), (x + 180, y + 12),
                   (x + 150, y + 30), (x + 30, y + 30), (x + 120, y + 8)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # earth arc
    d.ellipse([x + 20, y + h - 26, x + 180, y + h + 30], fill=(29, 78, 216))
    d.ellipse([x + 40, y + h - 20, x + 90, y + h + 6], fill=(27, 122, 61))
    # satellites
    for sx, sy in [(x + 60, y + 12), (x + 110, y + 8), (x + 150, y + 16)]:
        d.rectangle([sx, sy, sx + 14, sy + 8], fill=(200, 200, 200), outline=INK)
        d.rectangle([sx - 10, sy + 2, sx, sy + 6], fill=(29, 78, 216))
        d.rectangle([sx + 14, sy + 2, sx + 24, sy + 6], fill=(29, 78, 216))


SCENES = {
    "tariff": scene_tariff, "gulf": scene_gulf, "cairo": scene_cairo,
    "eu": scene_eu, "uk": scene_uk, "greece": scene_greece,
    "canary": scene_canary, "nigeria": scene_nigeria, "space": scene_space,
    "korea": scene_korea, "storm": scene_storm, "colombia": scene_colombia,
    "fcc": scene_fcc,
}


def blit_scene(img, name, x, y, w, h):
    """Render a scene at its native 200x62 geometry, then scale to the box.

    Keeps every scene valid at any target height (feature strips are 36px).
    """
    tmp = Image.new("RGB", (200, 62), CREAM)
    td = ImageDraw.Draw(tmp)
    SCENES[name](td, 0, 0, 200, 62)
    img.paste(tmp.resize((w, h), Image.LANCZOS), (x, y))


# ---------------------------------------------------------------- data
MAIN_PANELS = [
    dict(num=1, label="14 NATIONS · UP TO 25%", scene="tariff", badge="OFFICIAL",
         source="USTR · REUTERS",
         headline="US PROPOSES NEW TARIFFS ON 14 PARTNERS",
         sub="India faces 25% — 17% if a trade deal is struck."),
    dict(num=2, label="BRENT $94.71 · 01:37 UTC", scene="gulf", badge="CLAIM",
         source="REUTERS · ARAB NEWS",
         headline="HOUTHI, IRAN CLAIMS RATTLE GULF OIL",
         sub="Houthis claim Ras Tanura hit; Iran claims mines."),
    dict(num=3, label="31 DEAD · 21 INJURED", scene="cairo", badge="OFFICIAL",
         source="EGYPT HEALTH MINISTRY · CNN",
         headline="CAIRO TANKER FIRE KILLS 31, INJURES 21",
         sub="Toll confirmed 26 Nov after Wednesday night fire."),
]

FEATURES = [
    dict(num=4, label="€1.58T", scene="eu", badge="REPORTED", source="Reuters",
         headline="EU DEBATES €1.58 TRILLION BUDGET",
         sentence="Leaders meet in Brussels; deal sought in Dec."),
    dict(num=5, label="£2,166 / YR", scene="uk", badge="REPORTED", source="BBC",
         headline="UK ENERGY BILLS TO JUMP 26% IN JAN",
         sentence="Typical household to pay £2,166 a year."),
    dict(num=6, label="15,000 MARCH", scene="greece", badge="REPORTED", source="Euronews",
         headline="GREECE STRIKES, ATHENS MARCHES",
         sentence="About 15,000 march in a general strike."),
    dict(num=7, label="1,990 IN A DAY", scene="canary", badge="REPORTED", source="Africanews",
         headline="1,990 MIGRANTS REACH CANARY ISLANDS",
         sentence="Fifteen boats arrive in a single day."),
    dict(num=8, label="$227M · 1.5 T", scene="nigeria", badge="OFFICIAL", source="NDLEA",
         headline="NIGERIA BUSTS $227M METH LAB",
         sentence="Agents seize 1.5 tonnes of meth."),
    dict(num=9, label="TIANGONG", scene="space", badge="REPORTED", source="Guardian",
         headline="FIRST PAKISTANI ASTRONAUT ABOARD TIANGONG",
         sentence="First foreign visitor aboard; stays about a week."),
    dict(num=10, label="3.25%", scene="korea", badge="OFFICIAL", source="Bank of Korea",
         headline="BANK OF KOREA LIFTS RATE TO 3.25%",
         sentence="Rate up 25 bps; 2027 growth seen at 4.1%."),
    dict(num=11, label="PARADE DELAYED", scene="storm", badge="REPORTED", source="BBC",
         headline="STORM DELAYS 100TH MACY'S PARADE",
         sentence="Parade moves to Sat 28 Nov; 6,000+ flights delayed."),
    dict(num=12, label="76 FREED", scene="colombia", badge="REPORTED", source="BBC",
         headline="COLOMBIA FREES 76 HOSTAGES",
         sentence="Police end 17-hour siege; total put at 76 on 26 Nov."),
    dict(num=13, label="1M SATELLITES", scene="fcc", badge="OFFICIAL", source="FCC · CNBC",
         headline="FCC CLEARS 1 MILLION SPACEX SATELLITES",
         sentence="First US approval for orbital data centres."),
]

# 21 one-line items (3 big + 10 features + 21 = 34 stories).
ALSO = [
    ("Poland plans no-fly zone at Ukraine border", "Reuters", "REPORTED"),
    ("UniCredit takes control of Commerzbank", "Reuters", "REPORTED"),
    ("34 nations urge Russia to halt chemical weapons", "OPCW", "OFFICIAL"),
    ("US urges citizens to leave Iran", "Euronews", "REPORTED"),
    ("Israeli strike kills Hamas official; 11 dead in Gaza", "BBC", "REPORTED"),
    ("Iraqi court seizes Kurdistan oil", "Al Jazeera", "REPORTED"),
    ("S. Africa voids Phala Phala report, $580k", "France 24", "REPORTED"),
    ("Drone attack kills 15 in Sudan", "AllAfrica", "REPORTED"),
    ("Bangladesh raises garment pay to 17,000 taka", "AFP", "REPORTED"),
    ("Nepal: 213 Indians presumed dead in floods", "The Hindu", "REPORTED"),
    ("Kim Jong Un urges tactical nuclear push", "KCNA via Reuters", "OFFICIAL"),
    ("N. Korea expels Swiss diplomat in 48 hours", "KCNA via Reuters", "OFFICIAL"),
    ("USTR's Greer: new tariffs months away", "IANS", "REPORTED"),
    ("Java gold-mine flood kills at least 13", "ANSA", "REPORTED"),
    ("FedEx jet slips off Miami runway; no injuries", "FAA", "OFFICIAL"),
    ("US core inflation 3.3%; Dec 9 Fed hike odds ~99%", "CME FedWatch", "REPORTED"),
    ("Abrego Garcia in Spain after 20-month fight", "Euronews", "REPORTED"),
    ("Brazil recalls ambassador from Argentina", "MercoPress", "REPORTED"),
    ("Puerto Rico court voids Luma deal 5-4", "GlobeTV", "REPORTED"),
    ("Earth above 2°C for 6 days; record 2.24°C", "Copernicus", "REPORTED"),
    ("Hera snaps giant crater on asteroid Dimorphos", "BBC", "REPORTED"),
]

NUMBERS = [
    ("€1.58T", "EU BUDGET PLAN 2028-34"),
    ("1,000,000", "SPACEX SATELLITES APPROVED BY FCC"),
    ("$227M", "METH SEIZED IN NIGERIA"),
    ("1,990", "CANARY ARRIVALS IN ONE DAY"),
    ("76", "HOSTAGES FREED IN CARTAGENA"),
    ("$94.71", "BRENT CRUDE AT 01:37 UTC"),
]

REGIONS = [
    ("EUROPE", 7, BLUE), ("N. AMERICA", 6, RED), ("MIDDLE EAST", 4, AMBER),
    ("AFRICA", 4, GREEN), ("E. ASIA", 4, TEAL), ("S. ASIA", 3, (120, 60, 160)),
    ("S. AMERICA", 2, (200, 100, 0)), ("GLOBAL", 3, GREY), ("SE ASIA", 1, (0, 120, 120)),
]

# (lon, lat) pins for panels 1-13 — spread so no two pins touch
PINS = {
    1: (-85, 36), 2: (50, 27), 3: (32, 29), 4: (7, 50), 5: (-4, 54),
    6: (19, 41), 7: (-16, 28), 8: (8, 9), 9: (70, 30), 10: (127, 37),
    11: (-72, 42), 12: (-75, 10), 13: (-99, 31),
}


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)

    # ---- masthead
    title = "Thursday 26 November 2026"
    fnt = fit_font(d, title, 1000, 48, bold=True, serif=True)
    tw = d.textlength(title, font=fnt)
    d.text(((W - tw) / 2, 12), title, font=fnt, fill=INK)
    d.line([12, 66, W - 12, 66], fill=INK, width=2)

    # ---- red bar: three biggest stories
    d.rectangle([8, 70, W - 8, 98], fill=RED)
    red_text = "US PROPOSES TARIFFS ON 14 NATIONS  ·  GULF ESCALATION — BRENT $94.71  ·  CAIRO TANKER FIRE: 31 DEAD"
    rf = fit_font(d, red_text, 996, 14, bold=True)
    d.text(((W - d.textlength(red_text, font=rf)) / 2, 78), red_text,
           font=rf, fill=(255, 255, 255))

    # ---- meta line
    meta = "THE WORLD IN ONE DAY  ·  34 STORIES  ·  9 REGIONS  ·  ALL DATED 26 NOV 2026 UTC"
    mf = font(12, bold=True)
    d.text(((W - d.textlength(meta, font=mf)) / 2, 104), meta, font=mf, fill=INK)
    d.line([12, 122, W - 12, 122], fill=INK, width=1)

    # ---- THE DAY IN NUMBERS (6 KPIs, one from a Lead story: Brent)
    d.text((12, 126), "THE DAY IN NUMBERS", font=font(11, bold=True), fill=RED)
    col_w, x0 = 168, 12
    for i, (num, label) in enumerate(NUMBERS):
        x = x0 + i * col_w
        nf = fit_font(d, num, 160, 24, bold=True)
        d.text((x, 142), num, font=nf, fill=RED if i % 2 == 0 else BLUE)
        draw_wrapped(d, label, font(8, bold=True), x, 170, 160, fill=INK, leading=10)
        if i:
            d.line([x - 6, 142, x - 6, 194], fill=LIGHTGREY, width=1)
    d.line([12, 198, W - 12, 198], fill=INK, width=1)

    # ---- timeline (UTC) — six real stamps, morning to midday, all INSIDE
    # the strip: times below the line, event names under the times.
    d.text((12, 202), "TIMELINE · UTC", font=font(10, bold=True), fill=BLUE)
    tl = [("01:00", "BOK RAISES RATE"), ("01:40", "FEDEX SLIPS, MIAMI"),
          ("02:18", "34 NATIONS URGE RUSSIA"), ("02:56", "CARTAGENA COUNT: 76"),
          ("07:57", "GREER: TARIFFS MONTHS AWAY"), ("12:00", "EU SUMMIT, BRUSSELS")]
    d.line([120, 214, W - 16, 214], fill=GREY, width=2)
    seg = (W - 16 - 120) / len(tl)
    for i, (t, label) in enumerate(tl):
        cx = int(120 + seg * i + seg / 2)
        d.ellipse([cx - 5, 209, cx + 5, 219], fill=RED, outline=INK)
        tf = font(9, bold=True)
        tw2 = d.textlength(t, font=tf)
        d.text((cx - tw2 / 2, 221), t, font=tf, fill=RED)
        lf = font(8, bold=True)
        lw = d.textlength(label, font=lf)
        d.text((max(8, min(cx - lw / 2, W - 16 - lw)), 231), label, font=lf, fill=INK)
    d.line([12, 240, W - 12, 240], fill=INK, width=1)

    # ---- three main panels: illustration ~30% of card height, headline
    # ~19px serif bold so it stays readable at 300px, source on every card
    y0, ph, pw = 246, 164, 328
    for i, p in enumerate(MAIN_PANELS):
        x = 8 + i * (pw + 8)
        d.rectangle([x, y0, x + pw, y0 + ph], fill=PAPER, outline=INK, width=1)
        # number chip
        d.rectangle([x, y0, x + 22, y0 + 22], fill=INK)
        d.text((x + 7, y0 + 4), str(p["num"]), font=font(12, bold=True), fill=(255, 255, 255))
        # illustration
        blit_scene(img, p["scene"], x + 1, y0 + 23, pw - 2, 50)
        # big label bar
        d.rectangle([x + 1, y0 + 73, x + pw - 1, y0 + 91], fill=DARKRED)
        lf = fit_font(d, p["label"], pw - 16, 13, bold=True)
        d.text(((2 * x + pw - d.textlength(p["label"], font=lf)) / 2, y0 + 77),
               p["label"], font=lf, fill=(255, 255, 255))
        draw_wrapped(d, p["headline"], font(19, bold=True, serif=True), x + 6, y0 + 94,
                     pw - 12, leading=21)
        d.text((x + 6, y0 + 139), p["sub"], font=font(10), fill=INK)
        d.text((x + 6, y0 + ph - 13), p["source"], font=font(9, bold=True), fill=BLUE)
        badge(d, x + pw - 62, y0 + ph - 14, p["badge"])

    # ---- ten feature panels, 2 rows x 5
    d.text((12, 416), "THE WORLD IN DETAIL", font=font(11, bold=True), fill=RED)
    fw, fh = 196, 116
    for idx, p in enumerate(FEATURES):
        row, col = divmod(idx, 5)
        x = 8 + col * (fw + 6)
        y = 434 + row * (fh + 4)
        d.rectangle([x, y, x + fw, y + fh], fill=PAPER, outline=INK, width=1)
        blit_scene(img, p["scene"], x + 1, y + 1, fw - 2, 36)
        d.rectangle([x, y, x + 20, y + 18], fill=INK)
        d.text((x + 6, y + 3), str(p["num"]), font=font(11, bold=True), fill=(255, 255, 255))
        lf = fit_font(d, p["label"], fw - 12, 10, bold=True)
        d.text((x + 6, y + 40), p["label"], font=lf, fill=RED)
        draw_wrapped(d, p["headline"], font(10, bold=True), x + 6, y + 53, fw - 12,
                     leading=11)
        draw_wrapped(d, p["sentence"], font(8), x + 6, y + 77, fw - 12, leading=10)
        d.text((x + 6, y + fh - 15), p["source"], font=font(8, bold=True), fill=BLUE)
        badge(d, x + fw - 66, y + fh - 16, p["badge"])

    # ---- ALSO ON THURSDAY 26 NOVEMBER: 21 one-liners, 2 cols x 11,
    # numbered 14-34. Plain number markers — no badge-coloured squares,
    # so the colours never clash with the region bar below.
    d.text((12, 676), "ALSO ON THURSDAY 26 NOVEMBER", font=font(11, bold=True), fill=RED)
    d.line([12, 692, W - 12, 692], fill=INK, width=1)
    for i, (head, src, bdg) in enumerate(ALSO):
        col, row = divmod(i, 11)
        x = 8 + col * 504
        y = 698 + row * 13
        nf = font(9, bold=True)
        d.text((x, y), "%d." % (14 + i), font=nf, fill=RED)
        text = "%s (%s · %s)" % (head, src, bdg)
        lf = fit_font(d, text, 472, 9)
        d.text((x + 24, y), text, font=lf, fill=INK)

    # ---- mini world map "WHERE IT HAPPENED" + proportional region bar
    d.text((12, 840), "WHERE IT HAPPENED — PINS 1–13 MATCH THE PANELS ABOVE",
           font=font(11, bold=True), fill=RED)
    d.text((656, 840), "STORIES BY REGION — 34 TOTAL",
           font=font(10, bold=True), fill=RED)
    mx, my, mw, mh = 8, 854, 640, 76
    d.rectangle([mx, my, mx + mw, my + mh], fill=(210, 226, 238), outline=INK, width=1)

    def mxy(lon, lat):
        return (mx + (lon + 170) / 360.0 * mw,
                my + (75 - lat) / 130.0 * mh)

    continents = [
        [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
         (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-110, 23), (-125, 40), (-150, 60)],
        [(-80, 10), (-60, 5), (-35, -5), (-40, -20), (-55, -35), (-70, -50),
         (-75, -30), (-80, -5)],
        [(-10, 36), (0, 50), (-5, 58), (10, 60), (20, 70), (30, 70), (40, 60),
         (30, 45), (20, 40), (10, 38), (0, 36)],
        # United Kingdom
        [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 57), (1, 52), (-1, 51)],
        [(-17, 15), (-10, 30), (10, 37), (30, 32), (35, 28), (43, 12), (51, 10),
         (40, -5), (35, -20), (20, -35), (15, -25), (12, 5), (-5, 5)],
        [(40, 70), (60, 70), (90, 75), (120, 72), (150, 70), (170, 66), (160, 60),
         (140, 50), (130, 35), (120, 25), (105, 10), (100, 5), (90, 15), (80, 8),
         (70, 20), (60, 25), (50, 30), (43, 40), (40, 55)],
        # Korean peninsula
        [(126, 35), (126, 39), (128, 42), (130, 39), (129, 35), (127, 34)],
        # Japan
        [(130, 31), (132, 33), (134, 34), (137, 35), (139, 37), (141, 39),
         (142, 42), (140, 44), (138, 40), (135, 36), (132, 33)],
        # Indonesia archipelago
        [(95, 5), (98, 3), (100, 0), (104, -3), (108, -6), (112, -7),
         (116, -8), (120, -9), (124, -9), (128, -8), (131, -4), (136, -4),
         (140, -6), (138, -8), (132, -9), (124, -10), (118, -10), (112, -8),
         (106, -7), (102, -4), (98, -1), (95, 2)],
        # Australia
        [(113, -22), (122, -14), (132, -11), (142, -11), (146, -19), (150, -23),
         (153, -27), (150, -32), (146, -39), (140, -38), (135, -35), (129, -32),
         (124, -33), (118, -35), (114, -30), (113, -26)],
    ]
    for poly in continents:
        d.polygon([mxy(lon, lat) for lon, lat in poly],
                  fill=(198, 204, 188), outline=GREY)
    for num in range(1, 14):
        lon, lat = PINS[num]
        px, py = mxy(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        nf = font(8, bold=True)
        nw = d.textlength(str(num), font=nf)
        d.text((px - nw / 2, py - 5), str(num), font=nf, fill=(255, 255, 255))
    # region bar: one horizontal bar, segment widths proportional to counts
    bx, by, bw, bh = 656, 854, 360, 18
    total = sum(c for _, c, _ in REGIONS)
    cx = bx
    for name, count, color in REGIONS:
        seg_w = bw * count / total
        d.rectangle([cx, by, cx + seg_w, by + bh], fill=color, outline=(255, 255, 255))
        if seg_w >= 20:
            cf = font(9, bold=True)
            cw = d.textlength(str(count), font=cf)
            d.text((cx + (seg_w - cw) / 2, by + 4), str(count), font=cf,
                   fill=(255, 255, 255))
        cx += seg_w
    # legend: colour swatch + name + count, 3 columns x 3 rows
    for i, (name, count, color) in enumerate(REGIONS):
        col, row = divmod(i, 3)
        lx = 656 + col * 122
        ly = 880 + row * 15
        d.rectangle([lx, ly, lx + 12, ly + 10], fill=color)
        d.text((lx + 16, ly - 1), "%s %d" % (name, count), font=font(9, bold=True),
               fill=INK)

    # ---- DATE CHECK red box
    d.rectangle([8, 934, W - 8, 992], fill=(255, 235, 235), outline=RED, width=2)
    d.text((16, 938), "DATE CHECK", font=font(11, bold=True), fill=RED)
    dc1 = ("Every story here happened or was first reported on Thursday 26 November 2026 "
           "(UTC). Announced 25 Nov but confirmed or developed on 26 Nov — Poland "
           "no-fly zone, Swiss diplomat expulsion, USTR tariff proposal, Cairo toll — are framed "
           "as 26 Nov developments.")
    dc2 = ("EXCLUDED (24 Nov): Huawei verdict (10 of 12) · China probes Shanghai party chief "
           "Chen Jining. EXCLUDED (25 Nov): Champions League Matchday 5 · Australia–Solomon "
           "Islands pact · Steelers release Aaron Rodgers · Jensen Huang's Nvidia return.")
    y = draw_wrapped(d, dc1, font(9), 16, 950, 992, fill=INK, leading=10)
    draw_wrapped(d, dc2, font(9, bold=True), 16, y + 1, 992, fill=DARKRED, leading=10)

    # ---- footer legend: colour swatches in front of each certainty level
    legend_parts = [
        ("CERTAINTY: ", None, None),
        ("CONFIRMED", "CONFIRMED", " = verified 2+ outlets  ·  "),
        ("OFFICIAL", "OFFICIAL", " = official source  ·  "),
        ("REPORTED", "REPORTED", " = single-outlet report  ·  "),
        ("CLAIM", "CLAIM", " = one-sided claim. "),
        ("US market close excluded — that was the Wed 25 Nov session.", None, None),
    ]
    lf = font(9)
    total_w = 0
    for text, swatch, tail in legend_parts:
        if swatch:
            total_w += 14
        total_w += d.textlength(text, font=lf)
        if tail:
            total_w += d.textlength(tail, font=lf)
    lx = (W - total_w) / 2
    ly = 995
    for text, swatch, tail in legend_parts:
        if swatch:
            d.rectangle([lx, ly + 1, lx + 11, ly + 10], fill=BADGE_COLORS[swatch])
            lx += 14
        d.text((lx, ly), text, font=lf, fill=INK)
        lx += d.textlength(text, font=lf)
        if tail:
            d.text((lx, ly), tail, font=lf, fill=INK)
            lx += d.textlength(tail, font=lf)
    credit = "Original graphics, not photos  ·  34 stories  ·  9 regions  ·  All figures as reported 26 Nov 2026 UTC"
    cf = font(8)
    d.text(((W - d.textlength(credit, font=cf)) / 2, 1007), credit, font=cf, fill=GREY)
    return img, d


if __name__ == "__main__":
    image, _ = render()
    out = os.path.join(HERE, "entry.png")
    image.save(out, format="PNG")
    print("wrote %s %s" % (out, image.size))
