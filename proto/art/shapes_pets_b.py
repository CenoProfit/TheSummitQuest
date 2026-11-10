# -*- coding: utf-8 -*-
"""Companions 5-9: hawk, eagle, two golems, a drake."""
from pixlib import *
import math

def eye(g, x, y, r=2.8, iris='C'):
    disc(g, x, y, r + 0.7, 'q')
    disc(g, x, y, r, iris)
    disc(g, x + r*0.12, y + r*0.12, r*0.50, 'x')
    disc(g, x - r*0.34, y - r*0.38, r*0.30, 'Z')

def talon(g, cx, top, bot, w=5):
    taper(g, cx, top, cx, bot, w, w*0.7, 'C')
    hornridge(g, cx, top, cx, bot, 4)          # scaled leg
    for i in range(3):
        taper(g, cx, bot, cx - 6 + i*6, bot + 5, 3.5, 1.6, 'C')
        disc(g, cx - 6 + i*6, bot + 5.6, 1.2, 'x')
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
    poly(g, [(43, 11), (55, 11), (56, 13), (44, 14)], 'd')
    if step:
        poly(g, [(26, 22), (16, 4), (36, 12), (44, 28), (30, 34)], 'A') # wing raised
        featherrows(g, 19, 10, 40, 24, 4, 7)
    else:
        poly(g, [(24, 26), (24, 44), (42, 48), (48, 32), (36, 22)], 'A')
        featherrows(g, 26, 28, 46, 40, 4, 8)
    featherrows(g, 8, 44, 22, 36, 2, 6)                                  # tail
    talon(g, 29, 44, 56); talon(g, 40, 44, 56)
    eye(g, 51, 16, 3.4)
    return dump(paint(g, 0.10))

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
        featherrows(g, 32 + s*11, 24 + L*0.3, 32 + s*29, 16 + L, 3, 6)
    ellipse(g, 32, 30, 11, 16, 'A')                           # body
    for r in range(5):                                        # breast feathers
        y = 22 + r*4
        for i in range(4):
            disc(g, 26 + i*4 + (2 if r % 2 else 0), y, 1.7, 'A')
            put(g, 26 + i*4 + (2 if r % 2 else 0), y + 1.6, 'd')
            put(g, 25 + i*4 + (2 if r % 2 else 0), y - 1.4, 'B')
    ellipse(g, 32, 14, 9, 8, 'A')                             # head
    poly(g, [(28, 16), (32, 27), (36, 16)], 'C')              # beak toward you
    line_on(g, 32, 17, 32, 26, 'x', 'C', 0.9)
    poly(g, [(24, 44), (40, 44), (36, 60), (28, 60)], 'A')    # fanned tail
    for i in range(4): line_on(g, 26 + i*3.2, 46, 28 + i*2.6, 59, 'q', 'A', 1.1)
    talon(g, 26, 42, 52, 4); talon(g, 38, 42, 52, 4)
    eye(g, 28, 12, 2.6); eye(g, 36, 12, 2.6)
    return dump(paint(g, 0.10))

# -------------------------------------------------------- 7 small golem
def golem_small(step):
    g = blank()
    k = 1 if step else -1
    poly(g, [(14, 24), (50, 24), (54, 34), (50, 48), (14, 48), (10, 34)], 'A')  # torso
    poly(g, [(22, 10), (42, 10), (44, 22), (20, 22)], 'A')                      # head
    poly(g, [(26, 18), (38, 18), (38, 27), (26, 27)], 'A')                      # neck
    # Without the neck the head stopped two rows above the shoulders and
    # the golem's head simply floated over its body.
    for s in (-1, 1):                                                           # arms
        poly(g, [(32 + s*18, 26), (32 + s*28, 28 + k*2), (32 + s*27, 42 + k*2),
                 (32 + s*17, 40)], 'A')
        poly(g, [(32 + s*23, 40 + k*2), (32 + s*31, 40 + k*2),
                 (32 + s*31, 50 + k*2), (32 + s*22, 50 + k*2)], 'A')
    for s in (-1, 1):                                                           # legs
        poly(g, [(32 + s*13, 46), (32 + s*4, 46), (32 + s*5, 60), (32 + s*15, 60)], 'A')
    g = shadeform(g)
    for (ax, ay, bx, by) in ((16, 30, 30, 36), (34, 28, 48, 38), (20, 42, 36, 44),
                             (12, 36, 22, 30), (40, 44, 52, 36)):
        line_on(g, ax, ay, bx, by, 'q', 'A', 1.2)                               # cracks
        line_on(g, ax, ay + 1.2, bx, by + 1.2, 'B', 'A', 0.8)
    for (mx, my, mr) in ((20, 28, 2.4), (44, 32, 2.0), (30, 44, 2.2), (38, 20, 1.8)):
        disc(g, mx, my, mr, 'd'); disc(g, mx - 0.6, my - 0.8, mr * 0.5, 'B')    # pits
    for ex in (26, 38): gem(g, ex, 16, 3.4, 'C', 5)                             # eyes
    poly(g, [(27, 30), (37, 30), (35, 42), (29, 42)], 'C')                      # seam
    gem(g, 32, 36, 3.6, 'C', 6)
    return dump(paint(g, 0.10))

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
    disc(g, 32, 30, 9, 'x'); gem(g, 32, 30, 7.6, 'C', 8)                        # core
    for a in range(8):                                                          # seams out of it
        th = a*math.pi/4
        line_on(g, 32 + 9*math.cos(th), 30 + 9*math.sin(th),
                   32 + 24*math.cos(th), 30 + 24*math.sin(th), 'C', 'A', 1.3)
        line_on(g, 32 + 9*math.cos(th), 31 + 9*math.sin(th),
                   32 + 24*math.cos(th), 31 + 24*math.sin(th), 'x', 'C', 0.8)
    for ex in (27, 37): gem(g, ex, 11, 2.8, 'C', 5)
    for (ax, ay, bx, by) in ((10, 22, 24, 26), (42, 22, 54, 26), (20, 50, 28, 58),
                             (8, 34, 18, 40), (46, 34, 56, 40)):
        line_on(g, ax, ay, bx, by, 'q', 'A', 1.2)
        line_on(g, ax, ay + 1.2, bx, by + 1.2, 'B', 'A', 0.8)
    for (mx, my, mr) in ((16, 26, 2.6), (48, 28, 2.4), (28, 52, 2.2), (40, 50, 2.0)):
        disc(g, mx, my, mr, 'd'); disc(g, mx - 0.7, my - 0.9, mr * 0.5, 'B')
    return dump(paint(g, 0.10))

# -------------------------------------------------------------- 9 drake
def wing(g, S, T, arc, bites):
    poly(g, [S, T] + arc, 'C')
    for (cx, cy, r) in bites: disc(g, cx, cy, r, '.')
    line_on(g, S[0], S[1], T[0], T[1], 'x', 'C', 1.4)          # leading bone
    line_on(g, S[0], S[1] - 1, T[0], T[1] - 1, 'Z', 'C', 0.9)
    for p in arc[:-1]:
        line_on(g, S[0], S[1], p[0], p[1], 'x', 'C', 1.2)      # finger struts
        line_on(g, S[0] + 1, S[1], p[0] + 1, p[1], 'Y', 'C', 0.8)
    for i, p in enumerate(arc[:-1]):                           # veins between them
        mid = ((p[0] + arc[i+1][0]) / 2.0, (p[1] + arc[i+1][1]) / 2.0)
        line_on(g, (S[0]*2 + p[0])/3.0, (S[1]*2 + p[1])/3.0, mid[0], mid[1], 'c', 'C', 0.8)

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
    scales(g, 23, 41, 30, 40, 3.0, 1.6)                       # hide
    poly(g, [(24, 44), (42, 44), (40, 48), (26, 48)], 'C')
    poly(g, [(26, 40), (41, 40), (41, 44), (25, 44)], 'C')
    for i in range(5):
        line_on(g, 26 + i*3.6, 39, 26 + i*3.6, 48, 'x', 'C', 1.1)
        line_on(g, 27 + i*3.6, 39, 27 + i*3.6, 48, 'Z', 'C', 0.8)
    taper(g, 36, 36, 45, 20, 13, 9, 'A')
    ellipse(g, 49, 15, 8, 6, 'A')
    poly(g, [(53, 11), (62, 14), (62, 20), (53, 20)], 'A')
    poly(g, [(53, 18), (62, 18), (62, 20), (53, 21)], 'c')
    for jx in (55, 58, 61): disc(g, jx, 18.6, 0.9, 'W')
    poly(g, [(47, 10), (36, 1), (44, 12)], 'C'); hornridge(g, 45, 11, 37, 2, 4)
    poly(g, [(51, 8), (44, 0), (53, 11)], 'C'); hornridge(g, 51, 9, 45, 1, 4)
    eye(g, 54, 13, 2.4, 'C')
    for (nx, ny) in ((60, 16), (58, 15.4)): disc(g, nx, ny, 0.9, 'q')
    for (sx, sy, h) in [(42, 25, 5), (37, 30, 6), (30, 29, 6), (24, 33, 5),
                        (17, 44, 4), (10, 50, 3)]:
        poly(g, [(sx, sy), (sx - h, sy - 1), (sx - 1, sy + h)], 'C')
        line_on(g, sx - 1, sy, sx - h + 1, sy, 'Z', 'C', 0.9)
    scales(g, 8, 20, 48, 56, 3.4, 1.7)                        # tail and haunch
    g = shadeform(g)
    return dump(paint(g, 0.10))

SHAPES = []
for fn in (raptor, eagle, golem_small, golem_large, drake):
    SHAPES += [fn(False), fn(True)]
