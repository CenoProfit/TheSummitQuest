# -*- coding: utf-8 -*-
"""Companions 5-9: hawk, eagle, two golems, a drake."""
from pixlib import *
import math

def eye(g, x, y, r=2.8):
    disc(g, x, y, r, 'o'); disc(g, x - r*0.25, y - r*0.25, r*0.5, 'W')

def talon(g, cx, top, bot, w=5):
    taper(g, cx, top, cx, bot, w, w*0.7, 'C')
    for i in range(3):
        taper(g, cx, bot, cx - 6 + i*6, bot + 5, 3.5, 1.6, 'C')
    taper(g, cx, bot, cx - 4, bot + 2, 3, 1.4, 'C')

# --------------------------------------------------------------- 5 hawk
def raptor(step):
    g = blank()
    poly(g, [(20, 30), (4, 46), (3, 58), (18, 48), (24, 38)], 'A')      # long tail
    for i in range(4):
        line_on(g, 18, 36 + i*4, 4, 48 + i*2, 'd', 'A')
    ellipse(g, 32, 32, 19, 16, 'A')
    ellipse(g, 48, 18, 12, 11, 'A')
    poly(g, [(53, 12), (60, 15), (63, 22), (56, 22), (54, 26), (52, 20)], 'C')  # hooked beak
    poly(g, [(41, 10), (56, 10), (58, 15), (42, 16)], 'A')              # heavy brow
    if step:
        poly(g, [(26, 22), (16, 4), (36, 12), (44, 28), (30, 34)], 'A') # wing raised
        for i in range(4): line_on(g, 20, 8 + i*4, 40, 20 + i*3, 'd', 'A')
    else:
        poly(g, [(24, 26), (24, 44), (42, 48), (48, 32), (36, 22)], 'A')
        for i in range(4): line_on(g, 25, 30 + i*4, 45, 34 + i*3, 'd', 'A')
    g = shadeform(g)
    talon(g, 29, 44, 56); talon(g, 40, 44, 56)
    eye(g, 51, 16, 3.4)
    return dump(outline(despeckle(g)))

# -------------------------------------------------------------- 6 eagle
def eagle(step):
    g = blank()
    L = 0 if step else 6                                      # wings up / down
    for s in (-1, 1):
        poly(g, [(32 + s*7, 24), (32 + s*31, 10 + L), (32 + s*31, 24 + L),
                 (32 + s*10, 34)], 'A')
        for i in range(5):                                    # separated primaries
            a = 0.15 + i*0.16
            x0 = 32 + s*(10 + 20*a); y0 = 26 + L*a
            poly(g, [(x0, y0), (x0 + s*9, y0 + 12), (x0 + s*4, y0 + 14), (x0 - s*2, y0 + 6)], 'A')
        for i in range(4):
            line_on(g, 32 + s*12, 22 + i*3 + L*0.3, 32 + s*29, 14 + i*3 + L, 'd', 'A')
    ellipse(g, 32, 30, 11, 16, 'A')                           # body
    ellipse(g, 32, 14, 9, 8, 'A')                             # head
    poly(g, [(28, 16), (32, 26), (36, 16)], 'C')              # beak toward you
    poly(g, [(24, 44), (40, 44), (36, 60), (28, 60)], 'A')    # fanned tail
    for i in range(3): line_on(g, 27 + i*3, 46, 29 + i*2, 59, 'd', 'A')
    g = shadeform(g)
    talon(g, 26, 42, 52, 4); talon(g, 38, 42, 52, 4)
    eye(g, 28, 12, 2.4); eye(g, 36, 12, 2.4)
    return dump(outline(despeckle(g)))

# -------------------------------------------------------- 7 small golem
def golem_small(step):
    g = blank()
    k = 1 if step else -1
    poly(g, [(14, 24), (50, 24), (54, 34), (50, 48), (14, 48), (10, 34)], 'A')  # torso
    poly(g, [(22, 10), (42, 10), (44, 22), (20, 22)], 'A')                      # head
    for s in (-1, 1):                                                           # arms
        poly(g, [(32 + s*18, 26), (32 + s*28, 28 + k*2), (32 + s*27, 42 + k*2),
                 (32 + s*17, 40)], 'A')
        poly(g, [(32 + s*23, 40 + k*2), (32 + s*31, 40 + k*2),
                 (32 + s*31, 50 + k*2), (32 + s*22, 50 + k*2)], 'A')
    for s in (-1, 1):                                                           # legs
        poly(g, [(32 + s*13, 46), (32 + s*4, 46), (32 + s*5, 60), (32 + s*15, 60)], 'A')
    g = shadeform(g)
    for (ax, ay, bx, by) in ((16, 30, 30, 36), (34, 28, 48, 38), (20, 42, 36, 44)):
        line_on(g, ax, ay, bx, by, 'o', 'A')                                    # cracks
    for ex in (26, 38): disc(g, ex, 16, 3.2, 'C'); put(g, ex - 1, 15, 'W')       # eyes
    poly(g, [(27, 30), (37, 30), (35, 42), (29, 42)], 'C')                      # seam
    return dump(outline(despeckle(g)))

# -------------------------------------------------------- 8 titan golem
def golem_large(step):
    g = blank()
    k = 1 if step else -1
    poly(g, [(8, 16), (56, 16), (52, 30), (46, 44), (18, 44), (12, 30)], 'A')   # huge shoulders
    poly(g, [(24, 6), (40, 6), (42, 17), (22, 17)], 'A')                        # small sunk head
    for s in (-1, 1):
        poly(g, [(32 + s*22, 18), (32 + s*31, 20 + k), (32 + s*30, 44 + k),
                 (32 + s*20, 42)], 'A')                                         # long arms
        poly(g, [(32 + s*18, 42 + k), (32 + s*31, 42 + k),
                 (32 + s*31, 56 + k), (32 + s*17, 56 + k)], 'A')                # big fists
    for s in (-1, 1):
        poly(g, [(32 + s*15, 42), (32 + s*3, 42), (32 + s*4, 62), (32 + s*17, 62)], 'A')
    g = shadeform(g)
    disc(g, 32, 30, 8, 'C'); disc(g, 32, 29, 5, 'W')                            # core
    for a in range(6):                                                          # seams out of it
        th = a*math.pi/3
        line_on(g, 32 + 8*math.cos(th), 30 + 8*math.sin(th),
                   32 + 22*math.cos(th), 30 + 22*math.sin(th), 'C', 'A')
    for ex in (27, 37): disc(g, ex, 11, 2.6, 'C'); put(g, ex - 1, 10, 'W')
    for (ax, ay, bx, by) in ((10, 22, 24, 26), (42, 22, 54, 26), (20, 50, 28, 58)):
        line_on(g, ax, ay, bx, by, 'o', 'A')
    return dump(outline(despeckle(g)))

# -------------------------------------------------------------- 9 drake
def wing(g, S, T, arc, bites):
    poly(g, [S, T] + arc, 'C')
    for (cx, cy, r) in bites: disc(g, cx, cy, r, '.')
    line_on(g, S[0], S[1], T[0], T[1], 'c', 'C')
    for p in arc[:-1]: line_on(g, S[0], S[1], p[0], p[1], 'c', 'C')

def drake(step):
    g = blank(); L = -5 if step else 0
    wing(g, (27, 31), (4, 7 + L), [(2, 21 + L), (7, 33), (19, 38)],
         [(2.0, 15.0 + L, 3.2), (4.6, 28.0, 3.4), (12.4, 37.4, 3.6)])
    wing(g, (37, 31), (60, 7 + L), [(62, 21 + L), (57, 33), (45, 38)],
         [(62.0, 15.0 + L, 3.2), (59.4, 28.0, 3.4), (51.6, 37.4, 3.6)])
    taper(g, 24, 41, 12, 50, 10, 5, 'A'); taper(g, 12, 50, 3, 56, 5, 2, 'A')
    poly(g, [(5, 55), (1, 50), (0, 60), (6, 59)], 'C')
    taper(g, 27, 42, 23, 54, 11, 7, 'A'); poly(g, [(17, 53), (26, 53), (26, 60), (18, 60)], 'A')
    taper(g, 39, 42, 42, 54, 10, 6, 'A'); poly(g, [(38, 53), (47, 53), (46, 60), (38, 60)], 'A')
    for fx in (18.5, 21.5, 24.5): disc(g, fx, 59, 1.7, 'C')
    for fx in (39.5, 42.5, 45.5): disc(g, fx, 59, 1.7, 'C')
    ellipse(g, 32, 38, 12, 9, 'A')
    poly(g, [(24, 44), (42, 44), (40, 48), (26, 48)], 'C')
    poly(g, [(26, 40), (41, 40), (41, 44), (25, 44)], 'C')
    for i in range(4): line_on(g, 27 + i*4, 39, 27 + i*4, 48, 'c', 'C')
    taper(g, 36, 36, 45, 20, 13, 9, 'A')
    ellipse(g, 49, 15, 8, 6, 'A')
    poly(g, [(53, 11), (62, 14), (62, 20), (53, 20)], 'A')
    poly(g, [(53, 18), (62, 18), (62, 20), (53, 21)], 'c')
    for jx in (55, 58, 61): disc(g, jx, 18.6, 0.9, 'W')
    poly(g, [(47, 10), (36, 1), (44, 12)], 'C')
    poly(g, [(51, 8), (44, 0), (53, 11)], 'C')
    disc(g, 54, 13, 2.2, 'c'); disc(g, 54.4, 12.4, 1.0, 'W')
    for (sx, sy, h) in [(42, 25, 5), (37, 30, 6), (30, 29, 6), (24, 33, 5), (17, 44, 4), (10, 50, 3)]:
        poly(g, [(sx, sy), (sx - h, sy - 1), (sx - 1, sy + h)], 'C')
    g = shadeform(g)
    return dump(outline(despeckle(g)))

SHAPES = []
for fn in (raptor, eagle, golem_small, golem_large, drake):
    SHAPES += [fn(False), fn(True)]
