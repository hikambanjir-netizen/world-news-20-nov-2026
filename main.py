#!/usr/bin/env python3
"""The World Today - 20 November 2026.
One page, the whole world. Entry for the make.fun bounty
news-image-20261120. Pure Python 3.13 standard library only.

Draws a 1024x1024 front-page infographic (hand-built PNG via zlib)
summarising the verified world news of Friday 20 November 2026 and
writes it to /output/entry.png. Deterministic: two runs produce the
same bytes.
"""

import os
import struct
import sys
import zlib

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
PAPER = (245, 239, 224)
INK = (27, 23, 18)
RED = (179, 39, 30)
BLUE = (31, 58, 95)
GOLD = (201, 162, 39)
TEAL = (14, 107, 107)
GREY = (90, 84, 72)
WHITE = (255, 255, 255)
BLACK = (12, 12, 12)
LIGHT = (232, 224, 205)

# --- 5x7 bitmap font (uppercase, digits, punctuation) ----------------------
# Each glyph is 7 rows of 5 characters; '#' is ink, '.' is empty.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".....", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    "+": (".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."),
    "=": (".....", ".....", ".###.", ".....", ".###.", ".....", "....."),
    "*": (".....", ".#.#.", ".###.", "#####", ".###.", ".#.#.", "....."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "#": (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    "@": (".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
}

CHAR_W = 6  # glyph width (5) + 1 px spacing, in font units


def text_width(s, scale):
    """Pixel width of string s rendered at the given scale."""
    return len(s) * CHAR_W * scale - scale


def wrap_text(s, max_w, scale):
    """Greedy word wrap; returns a list of lines fitting max_w pixels."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# --- canvas ----------------------------------------------------------------
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def hline(self, x, y, w, color, t=1):
        self.fill_rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.fill_rect(x, y, t, h, color)

    def rect(self, x, y, w, h, color, t=1):
        self.hline(x, y, w, color, t)
        self.hline(x, y + h - t, w, color, t)
        self.vline(x, y, h, color, t)
        self.vline(x + w - t, y, h, color, t)

    def line(self, x0, y0, x1, y1, color, t=1):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.fill_rect(x0 - t // 2, y0 - t // 2, t, t, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) ** 2) ** 0.5)
            self.fill_rect(cx - dx, yy, 2 * dx + 1, 1, color)

    def ring(self, cx, cy, r, color, t=2):
        for k in range(t):
            rr = r - k
            for yy in range(cy - rr, cy + rr + 1):
                dx = int((rr * rr - (yy - cy) ** 2) ** 0.5)
                self.set(cx - dx, yy, color)
                self.set(cx + dx, yy, color)

    def disc_row(self, cx, cy, r, y, color):
        """Fill one horizontal row of a disc (used for clipped stripes)."""
        dy = y - cy
        if abs(dy) > r:
            return
        dx = int((r * r - dy * dy) ** 0.5)
        self.fill_rect(cx - dx, y, 2 * dx + 1, 1, color)

    def text(self, x, y, s, scale, color, align="left"):
        if align == "center":
            x -= text_width(s, scale) // 2
        elif align == "right":
            x -= text_width(s, scale)
        for ch in s:
            glyph = FONT.get(ch.upper(), FONT[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "#":
                        self.fill_rect(x + col * scale, y + row * scale,
                                       scale, scale, color)
            x += CHAR_W * scale
        return x


# --- PNG encoding (deterministic, stdlib only) ------------------------------
def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr)
           + _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + _chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# --- artwork ----------------------------------------------------------------
def star(c, cx, cy, r, color):
    """Five-point star drawn as five lines from centre to points."""
    import math
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        x = int(cx + r * math.cos(a))
        y = int(cy + r * math.sin(a))
        c.line(cx, cy, x, y, color, 2)
        a2 = a + math.pi / 5
        x2 = int(cx + (r * 0.45) * math.cos(a2))
        y2 = int(cy + (r * 0.45) * math.sin(a2))
        c.line(cx, cy, x2, y2, color, 2)


def flag_us(c, cx, cy, r):
    """Stars-and-stripes disc: red field, white stripes, blue canton."""
    for yy in range(cy - r, cy + r + 1):
        band = (yy - (cy - r)) * 7 // (2 * r + 1)
        c.disc_row(cx, cy, r, yy, WHITE if band % 2 else RED)
    # blue canton, upper left quarter of the disc
    for yy in range(cy - r, cy - r + (2 * r) * 4 // 7):
        dy = yy - cy
        dx = int((r * r - dy * dy) ** 0.5)
        x0 = cx - dx
        x1 = min(cx - r // 6, cx + dx)
        if x1 > x0:
            c.fill_rect(x0, yy, x1 - x0, 1, BLUE)
    for sx in range(-2, 1):
        for sy in range(-2, 1):
            c.set(cx - r // 2 + sx * 9, cy - r // 2 + sy * 9, WHITE)


def flag_cn(c, cx, cy, r):
    """China disc: red field, one gold star."""
    c.disc(cx, cy, r, RED)
    star(c, cx - r // 5, cy - r // 5, r // 2, GOLD)


def flag_ru(c, cx, cy, r):
    """Russia disc: white, blue and red horizontal thirds."""
    for yy in range(cy - r, cy + r + 1):
        frac = (yy - (cy - r)) / (2 * r + 1)
        col = WHITE if frac < 1 / 3 else (BLUE if frac < 2 / 3 else RED)
        c.disc_row(cx, cy, r, yy, col)


def scales_of_justice(c, x, y, s, color):
    """Small scales icon: post, beam, two pans."""
    cx = x + 24 * s // 2
    c.vline(cx, y, 30 * s, color, 2)
    c.hline(x, y + 4 * s, 24 * s, color, 2)
    c.disc(cx, y + 2 * s, 2 * s, color)
    for side in (-1, 1):
        px = cx + side * 11 * s
        c.line(cx, y + 4 * s, px, y + 12 * s, color, 1)
        c.line(px - 6 * s, y + 12 * s, px + 6 * s, y + 12 * s, color, 2)
        # pan bowl: short arc of dots
        import math
        for a in range(0, 181, 15):
            ax = int(px + 6 * s * math.cos(math.radians(a)))
            ay = int(y + 12 * s + 6 * s * math.sin(math.radians(a)))
            c.fill_rect(ax - 1, ay - 1, 2, 2, color)


def cyclone_spiral(c, cx, cy, r, color):
    """Spiral storm icon."""
    import math
    prev = None
    for deg in range(0, 720, 6):
        a = math.radians(deg)
        rr = r * deg / 720.0
        x = int(cx + rr * math.cos(a))
        y = int(cy + rr * math.sin(a))
        if prev is not None:
            c.line(prev[0], prev[1], x, y, color, 2)
        prev = (x, y)


def kicker(c, x, y, scale, color, text):
    """Section kicker: red square bullet + small caps text."""
    c.fill_rect(x, y + 1, 10, 10, color)
    c.text(x + 16, y, text, 2, color)
    return y + 18


def headline(c, x, y, lines, scale, color=INK):
    for ln in lines:
        c.text(x, y, ln, scale, color)
        y += 7 * scale + 6
    return y


def body(c, x, y, text, max_w, scale=2, color=INK, gap=17):
    for ln in wrap_text(text, max_w, scale):
        c.text(x, y, ln, scale, color)
        y += gap
    return y


# --- the front page ----------------------------------------------------------
def build():
    c = Canvas(W, H, PAPER)
    # double border frame
    c.rect(10, 10, W - 20, H - 20, INK, 3)
    c.rect(20, 20, W - 40, H - 40, INK, 1)

    # ---- masthead -----------------------------------------------------------
    c.text(512, 40, "THE WORLD TODAY", 8, INK, align="center")
    c.hline(36, 112, 952, INK, 2)
    c.text(36, 122, "FRIDAY, 20 NOVEMBER 2026", 2, INK)
    c.text(512, 122, "ONE PAGE - THE WHOLE WORLD", 2, GREY, align="center")
    c.text(988, 122, "No. 324", 2, INK, align="right")
    c.hline(36, 146, 952, RED, 4)
    c.hline(36, 154, 952, INK, 1)

    # ---- lead story: the Shenzhen trilateral -------------------------------
    kicker(c, 36, 168, 2, RED, "SHENZHEN, CHINA - THE FIRST TRILATERAL")
    headline(c, 36, 196, ["TRUMP, XI AND PUTIN", "ISSUE JOINT", "'PEACE DECLARATION'"], 5)
    # three leaders, one table: flag discs over a round table
    flag_us(c, 700, 232, 50)
    flag_cn(c, 806, 214, 50)
    flag_ru(c, 912, 232, 50)
    c.ring(700, 232, 50, INK, 2)
    c.ring(806, 214, 50, INK, 2)
    c.ring(912, 232, 50, INK, 2)
    c.line(640, 292, 972, 292, INK, 3)          # tabletop
    c.line(680, 292, 668, 322, INK, 3)          # table legs
    c.line(932, 292, 944, 322, INK, 3)
    c.text(806, 326, "ONE TABLE, THREE POWERS", 2, GREY, align="center")
    y = body(c, 36, 330,
         "The leaders of the United States, China and Russia met for the "
         "first time in Shenzhen on Thursday and issued a four-point "
         "'peace declaration': reform the UN, boost fuel supplies, curb "
         "the world court, and talk on cutting nuclear risks.",
         580)
    body(c, 36, y + 4,
         "Ukraine and Iran were not mentioned. Europe called it a photo "
         "op; Macron said it would not 'reorganise the world'.",
         580)
    # the declaration, in four points
    c.fill_rect(640, 344, 348, 112, LIGHT)
    c.rect(640, 344, 348, 112, INK, 1)
    c.text(656, 356, "THE DECLARATION IN BRIEF", 2, RED)
    pts = ["1. REFORM THE UNITED NATIONS",
           "2. MORE FUEL FOR ALL NATIONS",
           "3. CURB THE WORLD COURT",
           "4. NO NUCLEAR WAR, EVER"]
    yy = 382
    for p in pts:
        c.text(656, yy, p, 2, INK)
        yy += 18
    c.hline(36, 478, 952, INK, 2)

    # ---- row two: justice and the cyclone -----------------------------------
    kicker(c, 36, 492, 2, RED, "THE HAGUE - JUSTICE")
    scales_of_justice(c, 452, 492, 1, BLUE)
    headline(c, 36, 520, ["MYANMAR GUILTY OF", "GENOCIDE"], 3)
    body(c, 36, 584,
         "The world court ruled on Thursday that Myanmar committed "
         "genocide against the Rohingya in 2017 - the first time in 80 "
         "years it has found a state guilty of genocide. Judges ordered "
         "reparations and the refugees' safe return.",
         460)
    c.vline(508, 492, 196, GREY, 1)
    kicker(c, 528, 492, 2, RED, "ODISHA, INDIA - WEATHER")
    cyclone_spiral(c, 940, 516, 22, TEAL)
    headline(c, 528, 520, ["CYCLONE AKVAN", "HITS INDIA TODAY"], 3)
    body(c, 528, 584,
         "Severe Cyclone Akvan was due to cross the coast near Gopalpur "
         "around noon today, with winds of 90-100 km/h. More than "
         "300,000 people were moved to safety and 69 trains cancelled.",
         460)
    c.hline(36, 700, 952, INK, 2)

    # ---- row three: space, games, Washington --------------------------------
    cols = [
        (36, "SPACE", ["VOYAGER 1, ONE", "LIGHT-DAY OUT"],
         "NASA confirmed that Voyager 1 is the first craft to fly a "
         "light-day from Earth - 26 billion km."),
        (360, "GAMES", ["GTA 6 SALES PASS", "$1.8 BILLION"],
         "GTA VI has sold past $1.8 billion worldwide, overtaking the "
         "global run of the film The Odyssey."),
        (684, "WASHINGTON", ["TRUMP PUTS IRAN", "DECISION TO 2027"],
         "President Trump said he is in no rush on Iran and will 'see "
         "what happens' after 1 January."),
    ]
    for x, kick, head, txt in cols:
        kicker(c, x, 714, 2, RED, kick)
        headline(c, x, 742, head, 3)
        body(c, x, 742 + len(head) * 27, txt, 300)
    c.vline(348, 714, 156, GREY, 1)
    c.vline(672, 714, 156, GREY, 1)
    c.hline(36, 882, 952, INK, 2)

    # ---- ticker --------------------------------------------------------------
    c.fill_rect(36, 892, 952, 52, BLACK)
    c.text(52, 900, "VAN GOGH SELLS FOR RECORD $190.4M  -  HAYABUSA2 SCRAPS ASTEROID LANDING", 2, WHITE)
    c.text(52, 922, "EUROPE OPEN TO RUSSIA TALKS  -  NICHOLLS 113* AS NZ BAT INDIA", 2, WHITE)

    # ---- footer --------------------------------------------------------------
    c.text(36, 958, "SOURCES: REUTERS, BBC, CNN, CFR, IMD - 20 NOV 2026.", 2, GREY)
    c.text(988, 958, "MAKE.FUN NEWS-IMAGE-20261120", 2, GREY, align="right")
    return c


def main():
    out = os.environ.get("ENTRY_OUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    canvas = build()
    n = write_png(out, canvas)
    print(f"wrote {out}: {canvas.w}x{canvas.h}, {n} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())


