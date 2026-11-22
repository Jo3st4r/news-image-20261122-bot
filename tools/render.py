#!/usr/bin/env python3
"""Render the news-image-20261122 poster: 50 real stories from Sunday
22 November 2026 on one 1024x1024 page.

Layout (newspaper front page, adapted from the proven 20261121 pattern):
  masthead -> 3 lead stories -> around-the-world band -> 47 more stories -> date check
The renderer is deterministic: fixed strings, fixed colours, no clock, no random.
Run:  python3 tools/render.py        (writes assets/entry.png)

Spot-checks done before rendering (22 Nov 2026):
  - Peru quake is magnitude 6.7, USGS-reviewed (early 6.9 readings were
    superseded); later casualty reports conflicted, so the headline stays
    neutral: "Peru 6.7 quake shakes the Andes".
  - COP31 Antalya: draft cover decision dropped every mention of fossil
    fuels; talks spilled into overtime; protesters disrupted the plenary
    ("failure" banner, demonstrator interrupting the president).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAPER = (246, 241, 231)
INK = (22, 21, 19)
RED = (179, 32, 44)
NAVY = (24, 38, 64)
GREY = (110, 104, 92)
LIGHT = (255, 255, 255)
RULE = (200, 190, 170)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_text(draw, text, fnt, max_w):
    """Return text shortened with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "..."
    while text and draw.textlength(text + ell, font=fnt) > max_w:
        text = text[:-1]
    return text + ell


# --- colours per beat -------------------------------------------------------
C_JUSTICE = (96, 44, 140)
C_POLITICS = (26, 84, 160)
C_MARKETS = (18, 120, 70)
C_CONFLICT = (179, 32, 44)
C_HEALTH = (12, 130, 130)
C_SPORT = (210, 110, 10)
C_TECH = (110, 60, 180)
C_CLIMATE = (40, 130, 50)
C_INDIA = (190, 110, 0)
C_SCIENCE = (0, 130, 160)
C_WORLD = (90, 90, 90)

LEADS = [
    {
        "num": "1",
        "kicker": "CONFLICT  ·  KUWAIT",
        "color": C_CONFLICT,
        "headline": "Iran strikes US air base in Kuwait",
        "summary": "Tehran hits the base and targets Bahrain as the war widens; Washington weighs its reply.",
    },
    {
        "num": "2",
        "kicker": "CLIMATE  ·  ANTALYA",
        "color": C_CLIMATE,
        "headline": "COP31 deadlocked over fossil fuels",
        "summary": "Draft deal drops every mention of fossil fuels; talks spill into overtime as protesters cry failure.",
    },
    {
        "num": "3",
        "kicker": "CONFLICT  ·  UKRAINE",
        "color": C_CONFLICT,
        "headline": "Russia fires 400 drones, 110 missiles",
        "summary": "Eight killed across Ukraine; missiles enter Poland as Kyiv's air defences are stretched thin.",
    },
]

# 47 more stories: (headline, beat colour). Every headline was checked
# against reporting from Reuters, BBC, AP, CNN, The Guardian or UN News.
GRID = [
    ("Protesters disrupt COP31 plenary", C_CLIMATE),
    ("Two tankers hit near Oman; ADNOC vessel, 1 crew missing", C_CONFLICT),
    ("Houthi attack damages PIF Tower, Riyadh", C_CONFLICT),
    ("Strike on Zelenskyy's hometown kills 2, injures ~60", C_CONFLICT),
    ("Russian strikes hit 18 Ukraine sites, embassies damaged", C_CONFLICT),
    ("Trump\u2013Xi\u2013Putin summit in Shenzhen, no breakthrough", C_POLITICS),
    ("Vance refuses to back Trump Iran strikes", C_POLITICS),
    ("Qatari delegation in Tehran", C_POLITICS),
    ("Witkoff\u2013Kushner meet Qatari mediators", C_POLITICS),
    ("Estonia to close Russia border, \u2018new Iron Curtain\u2019", C_POLITICS),
    ("France marches: 82,500 protest", C_WORLD),
    ("France\u2013US UN resolution on post-UNIFIL vacuum", C_POLITICS),
    ("3 French police guilty of racist violence (Zecler case)", C_JUSTICE),
    ("Depardieu + Houellebecq investigated for sexual assault", C_JUSTICE),
    ("UK\u2013EU begin Brexit rollback, Blair warning", C_POLITICS),
    ("Finland cargo ship to Kaliningrad hit by drones", C_CONFLICT),
    ("Russia designates Insider journalist Panov \u2018foreign agent\u2019", C_POLITICS),
    ("Drone damages Russian merchant vessel", C_CONFLICT),
    ("Wildberries CEO Kim steps down after EU sanctions", C_MARKETS),
    ("Peru 6.7 quake shakes the Andes", C_WORLD),
    ("Assam 3.6 quake", C_WORLD),
    ("Cyclone Akvan weakens, 14 Ranchi flights cancelled", C_CLIMATE),
    ("Basra power-facility fire kills 4, injures 35", C_WORLD),
    ("Tbilisi gas explosion kills 6 incl. child", C_WORLD),
    ("\u2018El Chapo Isidro\u2019 arrested", C_WORLD),
    ("S. Korea court overturns ex-PM Han's 15-year sentence", C_JUSTICE),
    ("Bukele to register for 3rd term, vote 28 Feb 2027", C_POLITICS),
    ("Bolsonaro in ICU, stable", C_WORLD),
    ("US court lets Trump end TPS for ~600,000 Venezuelans", C_JUSTICE),
    ("13 first-time Black lawmakers in US Congress", C_POLITICS),
    ("S&P \u22123.7%, Dow \u2212950 on 7th down day; Bitcoin ~$60,000", C_MARKETS),
    ("Japan GDP \u22120.1% annualised; Tokyo \u22125%, Seoul \u22125.2%", C_MARKETS),
    ("India inflation breaches 6%", C_INDIA),
    ("India forex reserves $705.3bn, 3-month low", C_INDIA),
    ("Crude oil futures \u22123%+", C_MARKETS),
    ("EU proposes Big Tech tax + 2028\u201334 budget cuts", C_POLITICS),
    ("US approved ~900,000 AI chips for China in 6 months", C_TECH),
    ("COP31 AI pledge fails to attract major US tech", C_TECH),
    ("Taiwan: 8 Chinese aircraft cross median line, 9 naval vessels", C_CONFLICT),
    ("China snubs Japan PM Takaichi", C_POLITICS),
    ("Carney tours 5 continents, 32 countries in 113 days", C_POLITICS),
    ("Air Niugini emergency landing, all 146 survive", C_WORLD),
    ("NY weighs tougher e-bike battery laws, 406 fires this year", C_WORLD),
    ("DR Congo Ebola: 11,613 cases, 5,678 deaths", C_HEALTH),
    ("Sudan: 2,500+ displaced; drones killed 1,630+ in 2026", C_CONFLICT),
    ("Ireland 20\u201317 South Africa; Springboks in Nations final", C_SPORT),
    ("India v NZ 1st Test at Wellington; KL Rahul in focus", C_SPORT),
]

TIMELINE = ["ANTALYA", "KUWAIT", "KYIV", "SHENZHEN", "LIMA", "NEW YORK"]


def draw_masthead(d):
    x0, x1 = 28, W - 28
    title = "THE WORLD IN ONE IMAGE"
    f_title = font(SERIF_B, 52)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 22), title, font=f_title, fill=INK)
    d.line([(x0, 88), (x1, 88)], fill=RED, width=4)
    f_date = font(SANS_B, 18)
    left = "SUNDAY, 22 NOVEMBER 2026"
    right = "50 STORIES  \u00b7  ONE PAGE"
    d.text((x0, 98), left, font=f_date, fill=INK)
    rw = d.textlength(right, font=f_date)
    d.text((x1 - rw, 98), right, font=f_date, fill=RED)
    d.line([(x0, 126), (x1, 126)], fill=RULE, width=1)


def draw_leads(d, y):
    """Three stacked lead rows; returns the y after the section."""
    x0, x1 = 28, W - 28
    row_h = 78
    for lead in LEADS:
        # number chip
        d.rectangle([x0, y + 6, x0 + 46, y + 52], fill=lead["color"])
        num = lead["num"]
        f_num = font(SANS_B, 28)
        nw = d.textlength(num, font=f_num)
        d.text((x0 + (46 - nw) / 2, y + 10), num, font=f_num, fill=LIGHT)
        tx = x0 + 60
        f_kick = font(SANS_B, 13)
        d.text((tx, y + 2), lead["kicker"], font=f_kick, fill=lead["color"])
        f_head = font(SANS_B, 27)
        head = fit_text(d, lead["headline"], f_head, x1 - tx)
        d.text((tx, y + 20), head, font=f_head, fill=INK)
        f_sum = font(SANS, 15)
        summ = fit_text(d, lead["summary"], f_sum, x1 - tx)
        d.text((tx, y + 52), summ, font=f_sum, fill=(60, 56, 50))
        y += row_h
        if lead is not LEADS[-1]:
            d.line([(x0, y - 6), (x1, y - 6)], fill=RULE, width=1)
    return y


def draw_timeline(d, y):
    x0, x1 = 28, W - 28
    band_h = 64
    d.rectangle([x0, y, x1, y + band_h], fill=NAVY)
    f_lab = font(SANS_B, 13)
    label = "AROUND THE WORLD IN ONE DAY"
    d.text((x0 + 14, y + 5), label, font=f_lab, fill=(255, 214, 120))
    # city stops along a line
    line_y = y + 34
    d.line([(x0 + 14, line_y), (x1 - 14, line_y)], fill=(140, 160, 200), width=2)
    n = len(TIMELINE)
    span = (x1 - 14) - (x0 + 14)
    f_city = font(SANS_B, 12)
    for i, city in enumerate(TIMELINE):
        cx = x0 + 14 + (span * i // (n - 1) if n > 1 else 0)
        d.ellipse([cx - 5, line_y - 5, cx + 5, line_y + 5], fill=(255, 214, 120))
        cw = d.textlength(city, font=f_city)
        lx = min(max(cx - cw / 2, x0 + 8), x1 - cw - 8)
        d.text((lx, line_y + 9), city, font=f_city, fill=LIGHT)
    return y + band_h


def draw_grid(d, y, bottom):
    x0, x1 = 28, W - 28
    f_sec = font(SANS_B, 14)
    section = "THE DAY IN 47 MORE STORIES"
    d.text((x0, y + 2), section, font=f_sec, fill=RED)
    d.line([(x0 + d.textlength(section, font=f_sec) + 10, y + 10),
            (x1, y + 10)], fill=RULE, width=1)
    top = y + 24
    rows = (len(GRID) + 1) // 2
    row_h = (bottom - top) / rows
    f_item = font(SANS_B, 13)
    col_w = (x1 - x0 - 24) / 2
    for idx, (headline, color) in enumerate(GRID):
        r, c = divmod(idx, 2)
        gx = x0 + c * (col_w + 24)
        gy = top + r * row_h
        cy = gy + row_h / 2
        d.rectangle([gx, cy - 4, gx + 8, cy + 4], fill=color)
        text = fit_text(d, headline, f_item, col_w - 16)
        d.text((gx + 14, cy - 8), text, font=f_item, fill=INK)


def draw_footer(d):
    x0, x1 = 28, W - 28
    d.line([(x0, H - 44), (x1, H - 44)], fill=RULE, width=1)
    f_foot = font(SANS, 12)
    line1 = "DATE CHECK: every story first reported 21\u201322 Nov 2026  \u00b7  Sources: Reuters, BBC, AP, CNN, The Guardian, UN News"
    w1 = d.textlength(line1, font=f_foot)
    d.text(((W - w1) / 2, H - 38), line1, font=f_foot, fill=GREY)
    line2 = "THE WORLD IN ONE IMAGE  \u00b7  SUNDAY 22 NOVEMBER 2026  \u00b7  make.fun news-image-20261122"
    w2 = d.textlength(line2, font=f_foot)
    d.text(((W - w2) / 2, H - 20), line2, font=f_foot, fill=GREY)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    y = draw_leads(d, 140)
    y = draw_timeline(d, y + 8)
    draw_grid(d, y + 6, H - 52)
    draw_footer(d)
    out = os.path.join(ROOT, "assets", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, format="PNG", compress_level=9)
    return out


if __name__ == "__main__":
    path = render()
    print("wrote", path)
