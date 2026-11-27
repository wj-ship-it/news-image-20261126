#!/usr/bin/env python3
"""Render a 1024x1024 newspaper front page summarising world news
for 26 November 2026. Pure PIL, run locally to produce news-frontpage.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "news-frontpage.png")

PAPER = (248, 244, 232)
INK = (18, 18, 18)
RED = (158, 28, 28)
GREY = (90, 86, 76)
RULE = (160, 152, 132)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MARGIN = 52
CONTENT_W = W - 2 * MARGIN


def wrap(draw, text, font, max_w):
    """Greedy word wrap by measured width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, y, kicker, headline, summary, head_font, body_font,
               kick_font, max_lines_head=2, max_lines_body=2):
    """Draw one story block; return the y just below it (before rule)."""
    draw.text((MARGIN, y), kicker, font=kick_font, fill=RED)
    y += 24
    h_lines = wrap(draw, headline, head_font, CONTENT_W)[:max_lines_head]
    for line in h_lines:
        draw.text((MARGIN, y), line, font=head_font, fill=INK)
        y += 33
    b_lines = wrap(draw, summary, body_font, CONTENT_W)[:max_lines_body]
    for line in b_lines:
        draw.text((MARGIN, y), line, font=body_font, fill=INK)
        y += 25
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    masthead = ImageFont.truetype(SERIF_B, 72)
    sub_font = ImageFont.truetype(SANS, 22)
    date_font = ImageFont.truetype(SANS_B, 20)
    kick_font = ImageFont.truetype(SANS_B, 17)
    head_font = ImageFont.truetype(SERIF_B, 29)
    body_font = ImageFont.truetype(SERIF, 20)

    y = 36
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=masthead)
    d.text(((W - tw) / 2, y), title, font=masthead, fill=INK)
    y += 80

    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 10
    dateline = "Thursday  \u00b7  26 November 2026  \u00b7  World News in One Page"
    dw = d.textlength(dateline, font=date_font)
    d.text(((W - dw) / 2, y), dateline, font=date_font, fill=INK)
    y += 30
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=3)
    y += 20

    stories = [
        ("TRADE",
         "U.S. Proposes New Tariffs on 14 Partners",
         "Washington cites structural overcapacity. China faces the highest "
         "rate, capped at 20% on top of existing duties; a public hearing on "
         "25 January comes before anything takes effect."),
        ("ENERGY  \u00b7  STRAIT OF HORMUZ",
         "Tanker Strikes Mine, Iran Claims",
         "Iran's Revolutionary Guard says a supertanker carrying over 2 million "
         "barrels of oil hit a mine near Khasab. The claim is unverified; a "
         "separate blast was reported west of Dubai."),
        ("ISRAEL",
         "Judge Urges Dropping Bribery Charge Against Netanyahu",
         "Judges hearing the corruption trial suggested prosecutors drop the "
         "sole bribery count, known as Case 4000."),
        ("EGYPT",
         "Fuel Truck Fire in Giza Kills 31",
         "A truck carrying petroleum products crashed and caught fire in Giza, "
         "killing 31 people."),
        ("UNITED KINGDOM",
         "Net Migration Falls to 77,000",
         "Net migration to Britain fell to 77,000 in the year to June 2026 \u2014 "
         "the lowest since 1997 outside the pandemic years."),
        ("NEW YORK",
         "Macy's Thanksgiving Parade Delayed by Storm",
         "The 100th Macy's Thanksgiving Day Parade moves to Saturday 28 November "
         "at 8:30 a.m. \u2014 the first weather delay in its history."),
    ]

    for i, (kicker, headline, summary) in enumerate(stories):
        y = draw_block(d, y, kicker, headline, summary,
                       head_font, body_font, kick_font)
        y += 4
        if i < len(stories) - 1:
            d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
            y += 12

    # Footer, kept well clear of the last story.
    y += 10
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=2)
    y += 12
    foot = "Sources: Reuters, Al Jazeera, CNA, NDTV, CNN, USA Today, Xinhua"
    fw = d.textlength(foot, font=sub_font)
    d.text(((W - fw) / 2, y), foot, font=sub_font, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes; last content y =", y)


if __name__ == "__main__":
    main()
