#!/usr/bin/env python3
"""Draw the Frost Front Page for Thursday 26 November 2026.

A 1024x1024 news front page: masthead, one lead story, twelve story
cards and a compact one-line list for breadth. Everything is drawn
with PIL primitives; no photos, no downloaded assets.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (25, 25, 25)
NAVY = (20, 33, 61)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
CARD = (255, 255, 255)
GREY = (90, 90, 90)
LINE = (205, 198, 184)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width, using real glyph measurements."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def draw_icon(d, kind, x, y, size, colour):
    """A small flat glyph drawn from primitives inside a colour chip."""
    d.rounded_rectangle([x, y, x + size, y + size], radius=6, fill=colour)
    cx, cy = x + size // 2, y + size // 2
    w = (255, 255, 255)
    if kind == "flame":
        d.polygon([(cx, y + 6), (cx + 9, cy + 2), (cx + 6, y + size - 7),
                   (cx - 6, y + size - 7), (cx - 9, cy + 2)], fill=w)
        d.ellipse([cx - 4, cy + 2, cx + 4, y + size - 8], fill=colour)
    elif kind == "globe":
        d.ellipse([x + 6, y + 6, x + size - 6, y + size - 6], outline=w, width=2)
        d.line([x + 6, cy, x + size - 6, cy], fill=w, width=2)
        d.ellipse([cx - 4, y + 6, cx + 4, y + size - 6], outline=w, width=2)
    elif kind == "ship":
        d.polygon([(x + 7, cy + 2), (x + size - 7, cy + 2),
                   (x + size - 11, y + size - 7), (x + 11, y + size - 7)], fill=w)
        d.rectangle([cx - 1, y + 7, cx + 1, cy], fill=w)
        d.polygon([(cx + 1, y + 7), (cx + 9, cy - 1), (cx + 1, cy - 1)], fill=w)
    elif kind == "rocket":
        d.polygon([(cx, y + 5), (cx + 6, cy + 4), (cx + 4, y + size - 9),
                   (cx - 4, y + size - 9), (cx - 6, cy + 4)], fill=w)
        d.polygon([(cx - 3, y + size - 9), (cx + 3, y + size - 9),
                   (cx, y + size - 3)], fill=(255, 200, 80))
    elif kind == "book":
        d.rectangle([x + 7, y + 8, x + size - 7, y + size - 8], outline=w, width=2)
        d.line([cx, y + 8, cx, y + size - 8], fill=w, width=2)
        d.line([x + 10, y + 13, cx - 3, y + 13], fill=w, width=2)
        d.line([cx + 3, y + 13, x + size - 10, y + 13], fill=w, width=2)
    elif kind == "candle":
        d.rectangle([cx - 4, y + 10, cx + 4, y + size - 7], fill=w)
        d.ellipse([cx - 3, y + 5, cx + 3, y + 11], fill=(255, 200, 80))
    elif kind == "chart":
        d.line([x + 7, y + size - 8, x + size - 7, y + size - 8], fill=w, width=2)
        d.rectangle([x + 9, cy + 2, x + 14, y + size - 10], fill=w)
        d.rectangle([cx - 2, cy - 4, cx + 3, y + size - 10], fill=w)
        d.rectangle([x + size - 14, y + 8, x + size - 9, y + size - 10], fill=w)
    elif kind == "chip":
        d.rectangle([x + 8, y + 8, x + size - 8, y + size - 8], outline=w, width=2)
        d.line([x + 12, cy, x + size - 12, cy], fill=w, width=2)
        d.line([cx, y + 12, cx, y + size - 12], fill=w, width=2)
    elif kind == "ball":
        d.ellipse([x + 7, y + 7, x + size - 7, y + size - 7], outline=w, width=2)
        d.arc([x + 7, y + 7, x + size - 7, y + size - 7], 200, 340, fill=w, width=2)
    elif kind == "knight":
        d.ellipse([cx - 7, y + 8, cx + 7, y + 22], fill=w)
        d.rectangle([x + 8, y + size - 10, x + size - 8, y + size - 6], fill=w)
    elif kind == "flag":
        d.rectangle([x + 10, y + 6, x + 12, y + size - 6], fill=w)
        d.polygon([(x + 12, y + 6), (x + size - 8, y + 10),
                   (x + 12, y + 15)], fill=w)
    elif kind == "scale":
        d.line([cx, y + 7, cx, y + size - 8], fill=w, width=2)
        d.line([x + 8, y + 11, x + size - 8, y + 11], fill=w, width=2)
        d.polygon([(x + 8, y + 11), (x + 13, y + 11), (cx - 6, y + 20)], fill=w)
        d.polygon([(x + size - 8, y + 11), (x + size - 13, y + 11),
                   (cx + 6, y + 20)], fill=w)
    else:  # star
        d.polygon([(cx, y + 6), (cx + 3, cy - 2), (cx + 10, cy - 2),
                   (cx + 5, cy + 3), (cx + 7, y + size - 7), (cx, cy + 6),
                   (cx - 7, y + size - 7), (cx - 5, cy + 3),
                   (cx - 10, cy - 2), (cx - 3, cy - 2)], fill=w)


LEAD = {
    "tag": "EGYPT",
    "colour": (178, 34, 34),
    "icon": "flame",
    "headline": "FIRE ON CAIRO RING ROAD KILLS AT LEAST 30",
    "summary": "A fuel tanker crash ignites a huge blaze on the highway circling "
               "Egypt's capital; 25 more are injured and cars are left charred.",
}

CARDS = [
    ("TRADE", (146, 90, 20), "globe",
     "US UNVEILS NEW TARIFFS ON CHINA, EU, BRAZIL",
     "Washington announces broad new duties on imports, citing subsidised factories abroad."),
    ("LIBYA", (90, 60, 120), "ship",
     "LIBYA VOWS REVENGE AFTER OFFICERS DIE",
     "Two naval officers die of wounds from Ukraine's drone strike on a Russian ship in Libya."),
    ("INDIA", (178, 34, 34), "candle",
     "MUMBAI REMEMBERS 26/11, 18 YEARS ON",
     "India marks 18 years since the attacks that killed more than 160 people in Mumbai."),
    ("INDIA", (34, 90, 140), "book",
     "INDIA MARKS 77 YEARS OF ITS CONSTITUTION",
     "Constitution Day honours the charter adopted on 26 November 1949."),
    ("SPACE", (20, 60, 120), "rocket",
     "FIRST PAKISTANI ASTRONAUT TO SPACE STATION",
     "Muhammad Zeeshan Ali joins China's Shenzhou-24 mission to the Tiangong station."),
    ("BANGLADESH", (20, 120, 60), "chart",
     "BANGLADESH RAISES GARMENT PAY 36%",
     "Minimum pay for entry-level garment workers rises in a win for millions."),
    ("KOREA", (120, 40, 90), "flag",
     "NORTH KOREA ORDERS SWISS OFFICE TO CLOSE",
     "Pyongyang orders the Swiss diplomatic office in the capital to shut."),
    ("CRICKET", (20, 110, 60), "ball",
     "SOORYAVANSHI, 15, HITS 204 OFF 53 BALLS",
     "The teenager sets a List A record with the fastest double century ever."),
    ("CHESS", (60, 60, 60), "knight",
     "GUKESH'S TITLE DEFENCE REACHES GAME THREE",
     "The world chess champion faces Sindarov in Geneva; the opener ended drawn."),
    ("USA", (150, 40, 40), "flame",
     "US ARMY BLOWS UP ITS LEAD AZIDE STOCKPILE",
     "The nation's entire store of the explosive chemical is destroyed in Iowa."),
    ("TECH", (20, 80, 140), "chip",
     "VANCE: NVIDIA CHIEF NEEDS NO PARDON",
     "The vice president plays down talk of a pardon as scrutiny of Nvidia grows."),
    ("BUSINESS", (120, 90, 20), "chart",
     "FLIPKART CHIEF TO STEP DOWN IN DECEMBER",
     "Kalyan Krishnamurthy prepares to leave the Walmart-owned retailer."),
]

BRIEF = [
    "India pledges Rs 15,000-crore aid package for Nepal",
    "IITs to add 6,000 seats in robotics, AI and space tech",
    "Ukraine strikes two Russian oil refineries overnight",
    "LPG tanker hits a naval mine in the Strait of Hormuz",
    "Israel kills Hamas security chief in Gaza strike",
    "Six missing after plane crashes into Gulf of Mexico",
    "US shelves Russia business-deal peace plan - FT",
    "India urges human control over AI in warfare",
    "Hasina seeks return to Bangladesh on 16 December",
    "IPL 2027 auction draws 1,220 player registrations",
    "Two Indians hurt in Riyadh attack leave hospital",
    "Colombia police free 20 hostages in supermarket siege",
    "Russia's own toll: nearly 500,000 war dead in Ukraine",
    "Duterte family to appeal court ruling on arrest",
    "Brazil: mosquito release cuts viral infections 68%",
    "Biovac to scale up African vaccine output on EU loan",
    "Cabinet clears Rs 4,288-crore Kamarajar port terminal",
    "US attorney general sidesteps Nvidia probe questions",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    title_f = font(SERIF_B, 58)
    title = "FROST FRONT PAGE"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 14), title, font=title_f, fill=(255, 255, 255))
    date_f = font(SANS_B, 19)
    date_line = "THURSDAY, 26 NOVEMBER 2026  \u2022  THE WORLD IN ONE PAGE"
    dw = d.textlength(date_line, font=date_f)
    d.text(((W - dw) / 2, 84), date_line, font=date_f, fill=(201, 162, 39))

    # ---- Lead story ----
    lx, ly, lw, lh = 24, 134, W - 48, 158
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=8, fill=CARD)
    d.rounded_rectangle([lx, ly, lx + 8, ly + lh], radius=4, fill=RED)
    tag_f = font(SANS_B, 14)
    d.text((lx + 22, ly + 12), LEAD["tag"], font=tag_f, fill=RED)
    draw_icon(d, LEAD["icon"], lx + lw - 118, ly + 16, 96, RED)
    head_f = font(SANS_B, 26)
    lines = wrap(d, LEAD["headline"], head_f, lw - 170)
    y = ly + 36
    for line in lines[:2]:
        d.text((lx + 22, y), line, font=head_f, fill=INK)
        y += 32
    sum_f = font(SANS, 16)
    slines = wrap(d, LEAD["summary"], sum_f, lw - 170)
    y += 4
    for line in slines[:2]:
        d.text((lx + 22, y), line, font=sum_f, fill=(60, 60, 60))
        y += 21

    # ---- Card grid: 3 columns x 4 rows ----
    cols, rows = 3, 4
    cw = (W - 48 - (cols - 1) * 8) // cols
    ch = 118
    gx, gy = 24, 304
    for i, (tag, colour, icon, headline, summary) in enumerate(CARDS):
        r, c = divmod(i, cols)
        x = gx + c * (cw + 8)
        y = gy + r * (ch + 8)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=8, fill=CARD)
        d.rectangle([x, y, x + cw, y + 4], fill=colour)
        tag_f2 = font(SANS_B, 12)
        d.text((x + 12, y + 12), tag, font=tag_f2, fill=colour)
        draw_icon(d, icon, x + cw - 44, y + 10, 32, colour)
        head_f2 = font(SANS_B, 16)
        # Leave the top-right corner free for the icon chip.
        lines = wrap(d, headline, head_f2, cw - 24 - 48)
        ty = y + 32
        for line in lines[:2]:
            d.text((x + 12, ty), line, font=head_f2, fill=INK)
            ty += 20
        sum_f2 = font(SANS, 12)
        slines = wrap(d, summary, sum_f2, cw - 24)
        ty += 2
        for line in slines[:2]:
            d.text((x + 12, ty), line, font=sum_f2, fill=(70, 70, 70))
            ty += 16

    # ---- Compact list for breadth ----
    list_y = gy + rows * (ch + 8) + 4
    d.line([24, list_y, W - 24, list_y], fill=LINE, width=2)
    head_f3 = font(SANS_B, 15)
    d.text((24, list_y + 8), "ALSO TODAY \u2014 IN BRIEF", font=head_f3, fill=NAVY)
    item_f = font(SANS, 13)
    col_w = (W - 48 - 30) // 2
    per_col = (len(BRIEF) + 1) // 2
    for i, item in enumerate(BRIEF):
        col, row = divmod(i, per_col)
        x = 24 + col * (col_w + 30)
        y = list_y + 32 + row * 16
        d.ellipse([x, y + 5, x + 6, y + 11], fill=NAVY)
        d.text((x + 12, y), item, font=item_f, fill=INK)

    # ---- Footer ----
    foot_f = font(SANS, 11)
    foot = ("All stories happened or were first reported on Thursday 26 November 2026.  "
            "Sources: AP, CNN, BBC, Reuters, The Guardian.")
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, H - 22), foot, font=foot_f, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
