# -*- coding: utf-8 -*-
"""Four pairs. Drawn as a pair with a gap, and the left one of each pair
   turned a little so they look worn rather than stamped."""
from pixlib import *

def boot(g, cx, lean, shaft_top, w, toe=10):
    poly(g, [(cx - w + lean, shaft_top), (cx + w + lean, shaft_top),
             (cx + w, 48), (cx - w, 48)], 'A')
    poly(g, [(cx - w, 44), (cx + w, 44), (cx + w + 2, 56), (cx - toe, 56)], 'A')

def sole(g, cx, w, toe=10, ch='C'):
    poly(g, [(cx - toe - 1, 54), (cx + w + 3, 54), (cx + w + 3, 59), (cx - toe - 1, 59)], ch)

def sh_trail():
    g = blank()
    for (cx, lean) in ((18, -2), (45, 1)):
        boot(g, cx, lean, 12, 9)
    g = shadeform(g, 'A', 'd', 'B')
    for (cx, lean) in ((18, -2), (45, 1)):
        poly(g, [(cx - 11 + lean, 12), (cx + 11 + lean, 12), (cx + 10, 20), (cx - 10, 20)], 'G')
        for y in (26, 32, 38):                             # laces
            line_on(g, cx - 8, y, cx + 8, y + 2, 'C', 'A')
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
        ring(g, cx, 28, 9, 2.4, 'C'); stud(g, cx, 28, 2.6)
        for y in (34, 40, 46): line_on(g, cx - 9, y, cx + 9, y, 'c', 'A')
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
        line(g, cx - 7 + lean, 26, cx + 7 + lean, 22, 'C', 3)
        sole(g, cx, 11, 12)
    return g

def sh_cuffed():
    g = blank()
    for (cx, lean) in ((18, -2), (45, 1)):
        boot(g, cx, lean, 18, 9)
        ellipse(g, cx + lean, 16, 14, 7, 'G')              # fleece cuff
    g = shadeform(g, 'A', 'd', 'B')
    for (cx, lean) in ((18, -2), (45, 1)):
        for fx in range(-12, 13, 5): disc(g, cx + lean + fx, 15, 2.6, 'H')
        poly(g, [(cx - 10, 36), (cx + 10, 36), (cx + 10, 42), (cx - 10, 42)], 'C')
        stud(g, cx + 6, 39, 2.2, 'A', 'W')
        sole(g, cx, 9)
    return g

SHAPES = [dump(outline(despeckle(f()))) for f in
          (sh_trail, sh_greaves, sh_sandals, sh_cuffed)]
