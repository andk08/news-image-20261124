#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Build-time only: the entry ships the rendered entry.png, and main.py
simply copies it to the output directory. Re-run this script whenever
a story label or layout changes; the committed PNG is the entry.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

INK = (16, 24, 40)          # near-black navy text
PAPER = (247, 243, 233)     # warm newsprint
NAVY = (13, 32, 61)         # header band
RED = (178, 34, 34)
GOLD = (201, 162, 39)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_flag(draw, x, y, w, h, stripes):
    """Horizontal stripes flag."""
    n = len(stripes)
    for i, col in enumerate(stripes):
        draw.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n],
                       fill=col)


def draw_building(draw, x, y, w, h, col):
    draw.rectangle([x, y, x + w, y + h], fill=col)
    for r in range(3):
        for c in range(3):
            wx = x + 8 + c * (w - 16) // 3
            wy = y + 10 + r * (h - 20) // 3
            draw.rectangle([wx, wy, wx + (w - 16) // 6, wy + (h - 20) // 6],
                           fill=(255, 214, 90))


def draw_smoke(draw, cx, cy, r, col=(120, 120, 120)):
    for dx, dy, rr in [(-r, r // 2, r), (0, 0, int(r * 1.25)),
                       (r, -r // 2, r), (r // 2, -r, int(r * 0.9))]:
        draw.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr,
                      cy + dy + rr], fill=col)


def draw_burst(draw, cx, cy, r, col=(255, 176, 32)):
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=col)


def draw_wave(draw, x, y, w, amp, col, phase=0.0):
    pts = [(x, y + amp)]
    for i in range(0, w + 1, 8):
        pts.append((x + i, y + amp * math.sin(i / w * math.pi * 2 + phase)))
    pts.append((x + w, y + amp))
    draw.polygon(pts, fill=col)


def draw_rocket(draw, cx, cy, s):
    # body
    draw.polygon([(cx, cy - 2.2 * s), (cx - 0.7 * s, cy + 0.6 * s),
                  (cx + 0.7 * s, cy + 0.6 * s)], fill=(230, 230, 230))
    draw.rectangle([cx - 0.7 * s, cy + 0.4 * s, cx + 0.7 * s, cy + 1.6 * s],
                   fill=(200, 30, 30))
    draw.ellipse([cx - 0.35 * s, cy + 0.9 * s, cx + 0.35 * s, cy + 1.6 * s],
                 fill=(90, 160, 220))
    draw.polygon([(cx - 0.7 * s, cy + 1.2 * s), (cx - 1.3 * s, cy + 2.0 * s),
                  (cx - 0.7 * s, cy + 1.9 * s)], fill=(200, 30, 30))
    draw.polygon([(cx + 0.7 * s, cy + 1.2 * s), (cx + 1.3 * s, cy + 2.0 * s),
                  (cx + 0.7 * s, cy + 1.9 * s)], fill=(200, 30, 30))
    draw.polygon([(cx - 0.35 * s, cy + 1.6 * s), (cx, cy + 2.6 * s),
                  (cx + 0.35 * s, cy + 1.6 * s)], fill=(255, 176, 32))


def draw_quake(draw, x, y, w, h, col=(178, 34, 34)):
    pts = [(x, y + h // 2)]
    seq = [0, -0.9, 0.5, -0.4, 0.9, -0.7, 0.2, -0.2, 0.6, -0.5, 0.1, 0]
    for i, v in enumerate(seq):
        pts.append((x + (i + 1) * w / (len(seq) + 1), y + h // 2 + v * h * 0.45))
    pts.append((x + w, y + h // 2))
    draw.line(pts, fill=col, width=4)


def draw_panel(draw, x, y, w, h, tag, accent, headline, detail, scene):
    # card
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14,
                           fill=(255, 255, 255), outline=(200, 196, 186),
                           width=2)
    # tag strip
    draw.rounded_rectangle([x, y, x + w, y + 34], radius=14, fill=accent)
    draw.rectangle([x, y + 20, x + w, y + 34], fill=accent)
    draw.rectangle([x, y, x + 14, y + 34], fill=accent)
    tf = font(SANS_B, 19)
    draw.text((x + 14, y + 7), tag, font=tf, fill=(255, 255, 255))
    # scene band
    sy = y + 34
    scene(draw, x, sy, w, 96)
    # headline
    hf = font(SANS_B, 30)
    lines = wrap(draw, headline, hf, w - 28)
    ty = sy + 104
    for ln in lines[:2]:
        draw.text((x + 14, ty), ln, font=hf, fill=INK)
        ty += 33
    # detail
    df = font(SANS, 19)
    dlines = wrap(draw, detail, df, w - 28)
    for ln in dlines[:2]:
        draw.text((x + 14, ty + 4), ln, font=df, fill=(70, 76, 90))
        ty += 23


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header band ----
    d.rectangle([0, 0, W, 160], fill=NAVY)
    d.rectangle([0, 160, W, 168], fill=GOLD)
    title_f = font(SERIF_B, 64)
    d.text((28, 10), "WORLD NEWS", font=title_f, fill=(255, 255, 255))
    date_f = font(SANS_B, 40)
    d.text((28, 88), "TUESDAY  \u2022  24 NOVEMBER 2026",
           font=date_f, fill=(255, 214, 90))

    # ---- scenes ----
    def scene_zaporizhzhia(dr, x, y, w, h):
        dr.rectangle([x, y, x + w, y + h], fill=(52, 68, 96))
        draw_building(dr, x + 30, y + h - 78, 74, 78, (30, 40, 58))
        draw_building(dr, x + 118, y + h - 62, 74, 62, (30, 40, 58))
        draw_building(dr, x + 206, y + h - 88, 74, 88, (30, 40, 58))
        draw_building(dr, x + 294, y + h - 70, 74, 70, (30, 40, 58))
        draw_smoke(dr, x + 245, y + 26, 15)
        draw_burst(dr, x + 330, y + 30, 26)
        draw_flag(dr, x + w - 74, y + 12, 52, 30,
                  [(0, 87, 184), (255, 213, 0)])

    def scene_gaza(dr, x, y, w, h):
        dr.rectangle([x, y, x + w, y + h], fill=(214, 178, 132))
        for bx, bh in [(20, 66), (90, 84), (170, 58), (250, 76), (330, 60)]:
            dr.rectangle([x + bx, y + h - bh, x + bx + 56, y + h],
                         fill=(120, 84, 60))
        draw_smoke(dr, x + 120, y + 30, 16, (90, 90, 90))
        draw_smoke(dr, x + 290, y + 22, 14, (90, 90, 90))
        draw_burst(dr, x + 205, y + 40, 22)

    def scene_libya(dr, x, y, w, h):
        dr.rectangle([x, y, x + w, y + h], fill=(28, 78, 120))
        draw_wave(dr, x, y + 62, w, 12, (16, 52, 88))
        dr.rectangle([x + 150, y + 34, x + 290, y + 66], fill=(70, 76, 84))
        dr.rectangle([x + 200, y + 16, x + 240, y + 36], fill=(70, 76, 84))
        dr.polygon([(x + 150, y + 34), (x + 290, y + 34), (x + 270, y + 66),
                    (x + 170, y + 66)], fill=(90, 96, 104))
        draw_burst(dr, x + 330, y + 30, 24)
        # drone
        dx, dy = x + 70, y + 26
        dr.ellipse([dx - 22, dy - 6, dx + 22, dy + 6], fill=(40, 40, 40))
        dr.ellipse([dx - 26, dy - 10, dx - 14, dy - 2], fill=(120, 120, 120))
        dr.ellipse([dx + 14, dy - 10, dx + 26, dy - 2], fill=(120, 120, 120))

    def scene_nepal(dr, x, y, w, h):
        dr.rectangle([x, y, x + w, y + h], fill=(176, 206, 226))
        dr.polygon([(x + 10, y + h), (x + 130, y + 12), (x + 250, y + h)],
                   fill=(90, 110, 140))
        dr.polygon([(x + 60, y + h), (x + 130, y + 12), (x + 200, y + h)],
                   fill=(240, 244, 248))
        dr.polygon([(x + 180, y + h), (x + 320, y + 26), (x + 420, y + h)],
                   fill=(70, 92, 122))
        draw_quake(dr, x + 30, y + 66, w - 60, 34)

    def scene_grok(dr, x, y, w, h):
        dr.rectangle([x, y, x + w, y + h], fill=(232, 228, 220))
        # courthouse
        dr.rectangle([x + 150, y + 18, x + 290, y + 34], fill=(120, 100, 80))
        for cx in (170, 210, 250, 270):
            dr.rectangle([x + cx, y + 34, x + cx + 12, y + 88],
                         fill=(150, 132, 110))
        dr.rectangle([x + 140, y + 88, x + 300, y + 100], fill=(120, 100, 80))
        # phone with warning
        dr.rounded_rectangle([x + 330, y + 14, x + 396, y + 100], radius=8,
                             fill=(20, 20, 24))
        dr.polygon([(x + 363, y + 26), (x + 388, y + 66), (x + 338, y + 66)],
                   fill=(255, 200, 0))
        dr.text((x + 358, y + 44), "!", font=font(SANS_B, 22), fill=(0, 0, 0))
        # scales
        dr.line([x + 60, y + 34, x + 60, y + 92], fill=(90, 80, 70), width=4)
        dr.line([x + 30, y + 38, x + 90, y + 38], fill=(90, 80, 70), width=4)
        dr.polygon([(x + 22, y + 52), (x + 38, y + 52), (x + 30, y + 66)],
                   fill=(90, 80, 70))
        dr.polygon([(x + 82, y + 52), (x + 98, y + 52), (x + 90, y + 66)],
                   fill=(90, 80, 70))

    def scene_space(dr, x, y, w, h):
        dr.rectangle([x, y, x + w, y + h], fill=(10, 14, 34))
        for sx, sy, sr in [(40, 24, 2), (120, 50, 3), (200, 18, 2),
                           (300, 44, 2), (380, 20, 3), (70, 80, 2),
                           (350, 82, 2), (250, 70, 2)]:
            dr.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                       fill=(255, 255, 255))
        draw_rocket(dr, x + 200, y + 18, 11)
        # station ring
        dr.ellipse([x + 320, y + 58, x + 400, y + 92], outline=(200, 200, 220),
                   width=4)
        dr.rectangle([x + 350, y + 68, x + 372, y + 82], fill=(200, 200, 220))

    stories = [
        ("UKRAINE", (0, 87, 184),
         "Strike on Zaporizhzhia kills 2, wounds 40",
         "Overnight Russian attack hits flats; four children among the wounded.",
         scene_zaporizhzhia),
        ("GAZA", (178, 34, 34),
         "Israeli strikes kill at least six in Gaza",
         "Two police officers among the dead, medics and police say.",
         scene_gaza),
        ("LIBYA", (16, 90, 120),
         "Ukraine drones hit Russian ships",
         "Kyiv says a warship was sunk off Benghazi; first reported today.",
         scene_libya),
        ("NEPAL", (150, 80, 20),
         "Magnitude 5.6 quake near the China border",
         "7:17 a.m. in Taplejung; felt in Kathmandu, no damage reported.",
         scene_nepal),
        ("UNITED STATES", (90, 40, 110),
         "Two states sue SpaceX over Grok deepfakes",
         "Virginia and Oregon are the first states to sue over sexual images.",
         scene_grok),
        ("SPACE", (40, 60, 110),
         "First foreign astronaut for Tiangong",
         "Pakistani Zeeshan Ali named in Shenzhou-24 crew; launch Wednesday.",
         scene_space),
    ]

    gx, gy = 24, 186
    pw, ph = 476, 258
    gap = 12
    for i, (tag, accent, head, detail, scene) in enumerate(stories):
        x = gx + (i % 2) * (pw + gap)
        y = gy + (i // 2) * (ph + gap)
        draw_panel(d, x, y, pw, ph, tag, accent, head, detail, scene)

    # ---- footer ----
    ff = font(SANS, 17)
    d.text((28, 994), "Events of Tuesday 24 November 2026, as reported that day.",
           font=ff, fill=(90, 96, 110))
    d.text((640, 994), "make.fun  \u2022  news-image-20261124",
           font=ff, fill=(90, 96, 110))

    img.save(OUT, optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
