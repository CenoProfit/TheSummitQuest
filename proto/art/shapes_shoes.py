# -*- coding: utf-8 -*-
"""Four pairs. Drawn as a pair with a gap, and the left one of each pair
   turned a little so they look worn rather than stamped."""
from pixlib import *

def boot(g, cx, lean, shaft_top, w, toe=10):
    poly(g, [(cx - w + lean, shaft_top), (cx + w + lean, shaft_top),
             (cx + w, 48), (cx - w, 48)], 'A')
    poly(g, [(cx - w, 44), (cx + w, 44), (cx + w + 2, 56), (cx - toe, 56)], 'A')

def sole(g, cx, w, toe=10, ch='C', tread=True):
    poly(g, [(cx - toe - 1, 54), (cx + w + 3, 54), (cx + w + 3, 59), (cx - toe - 1, 59)], ch)
    line_on(g, cx - toe - 1, 55, cx + w + 3, 55, 'Z', ch, 0.9)
    if tread:
        for i in range(5):
            x = cx - toe + i * ((toe + w + 3) / 5.0)
            line_on(g, x, 56, x, 59, 'x', ch, 1.0)

def eyelets(g, cx, ys, k=7):
    """laced eyelets up the front of a boot, crossed between them"""
    for y in ys:
        nails(g, [(cx - k, y), (cx + k, y)], 1.1)
    for i in range(len(ys) - 1):
        line(g, cx - k, ys[i], cx + k, ys[i + 1], 'H', 1)
        line(g, cx + k, ys[i], cx - k, ys[i + 1], 'H', 1)

def buckle(g, cx, cy, w=7, h=5):
    poly(g, [(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy + h), (cx - w, cy + h)], 'G')
    rect(g, cx + w * 0.2, cy - h * 0.7, cx + w * 0.95, cy + h * 0.7, 'C')
    rect(g, cx + w * 0.45, cy - h * 0.3, cx + w * 0.7, cy + h * 0.3, 'x')

def sh_trail():
    g = blank()
    for (cx, lean) in ((18, -2), (45, 1)):
        boot(g, cx, lean, 12, 9)
    g = shadeform(g, 'A', 'd', 'B')
    for (cx, lean) in ((18, -2), (45, 1)):
        poly(g, [(cx - 11 + lean, 12), (cx + 11 + lean, 12), (cx + 10, 20), (cx - 10, 20)], 'G')
        line_on(g, cx - 11 + lean, 13, cx + 11 + lean, 13, 'K', 'G', 0.9)
        eyelets(g, cx, (26, 32, 38, 44), 7)
        buckle(g, cx, 22, 8, 4)
        sole(g, cx, 9)
    return g

def sh_greaves():
    g = blank()
    for (cx, lean) in ((18, -1), (45, 1)):
        poly(g, [(cx - 10 + lean, 6), (cx + 10 + lean, 6), (cx + 9, 26), (cx - 9, 26)], 'A')
        disc(g, cx, 28, 11, 'A')                           # knee cop
        poly(g, [(cx - 9, 30), (cx + 9, 30), (cx + 10, 52), (cx - 10, 52)], 'A')
        poly(g, [(cx - 10, 50), (cx + 11, 50), (cx + 12, 58), (cx - 12, 58)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    for cx in (18, 45):
        ring(g, cx, 28, 9.5, 2.4, 'C'); gem(g, cx, 28, 3.6, 'A', 5)
        lames(g, cx - 9, cx + 9, 32, 50, 4)
        nails(g, [(cx - 8, 10), (cx + 8, 10)], 1.3)
        buckle(g, cx, 16, 8, 4)
        sole(g, cx, 11, 12)
    return g

def sh_sandals():
    g = blank()
    for (cx, lean) in ((18, -1), (45, 1)):
        poly(g, [(cx - 9, 40), (cx + 10, 40), (cx + 11, 52), (cx - 11, 52)], 'A')
        poly(g, [(cx - 12, 50), (cx + 12, 50), (cx + 12, 56), (cx - 12, 56)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    for (cx, lean) in ((18, -1), (45, 1)):
        for (ax, ay, bx, by) in ((-9, 42, 9, 26), (9, 42, -9, 26), (-7, 28, 7, 28)):
            line(g, cx + ax, ay, cx + bx + lean, by, 'G', 3)
            line(g, cx + ax, ay - 1, cx + bx + lean, by - 1, 'K', 2)
        buckle(g, cx + 2, 24, 7, 4)
        nails(g, [(cx - 8, 34), (cx + 8, 34), (cx, 44)], 1.2)
        sole(g, cx, 11, 12)
    return g

def sh_cuffed():
    g = blank()
    for (cx, lean) in ((18, -2), (45, 1)):
        boot(g, cx, lean, 18, 9)
        ellipse(g, cx + lean, 16, 14, 7, 'G')              # fleece cuff
    g = shadeform(g, 'A', 'd', 'B')
    for (cx, lean) in ((18, -2), (45, 1)):
        furtrim(g, [(cx + lean + fx, 15) for fx in range(-12, 13, 4)], 3.2)
        furtrim(g, [(cx + lean + fx, 19) for fx in range(-10, 11, 4)], 2.4)
        poly(g, [(cx - 10, 36), (cx + 10, 36), (cx + 10, 42), (cx - 10, 42)], 'G')
        buckle(g, cx + 1, 39, 9, 4)
        eyelets(g, cx, (26, 31), 6)
        sole(g, cx, 9)
    return g

SHAPES = [dump(paint(f())) for f in
          (sh_trail, sh_greaves, sh_sandals, sh_cuffed)]
