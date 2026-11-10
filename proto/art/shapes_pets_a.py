# -*- coding: utf-8 -*-
"""Companions 0-4: two dogs, two amphibians, one songbird.
   SHAPES is [c0_A, c0_B, c1_A, c1_B, ...] — two frames per creature,
   and everything that is not moving is identical between them."""
from pixlib import *

def leg(g, hx, hy, kx, ky, fx, fy, w, claws=3, ch='A'):
    taper(g, hx, hy, kx, ky, w, w*0.72, ch)
    taper(g, kx, ky, fx, fy, w*0.72, w*0.6, ch)
    poly(g, [(fx - w*0.5, fy - 2), (fx + w*0.9, fy - 2), (fx + w*0.9, fy + 3), (fx - w*0.5, fy + 3)], ch)
    for i in range(claws):
        disc(g, fx - w*0.3 + i*(w*0.55), fy + 3, 1.3, 'C')

def eye(g, x, y, r=2.6):
    disc(g, x, y, r, 'o'); disc(g, x - r*0.25, y - r*0.25, r*0.5, 'W')

def tufts(g, pts, r=2.4, ch='A'):
    for (x, y) in pts: disc(g, x, y, r, ch)

# ------------------------------------------------------------ 0 terrier
def dog_small(step):
    g = blank()
    taper(g, 16, 30, 6, 14, 6, 3, 'A')                         # tail, up and back
    if step:
        leg(g, 24, 40, 20, 50, 19, 56, 7); leg(g, 40, 40, 44, 50, 45, 56, 7)
        leg(g, 30, 42, 29, 51, 28, 57, 6); leg(g, 45, 42, 47, 51, 48, 57, 6)
    else:
        leg(g, 24, 40, 22, 50, 22, 56, 7); leg(g, 40, 40, 41, 50, 41, 56, 7)
        leg(g, 31, 42, 33, 51, 34, 57, 6); leg(g, 46, 42, 44, 51, 43, 57, 6)
    ellipse(g, 30, 33, 17, 11, 'A')                            # body
    ellipse(g, 48, 24, 10, 9, 'A')                             # head
    poly(g, [(54, 20), (63, 23), (63, 30), (54, 30)], 'A')     # muzzle
    poly(g, [(41, 17), (44, 4), (50, 16)], 'A')                # ears
    poly(g, [(51, 15), (57, 3), (58, 15)], 'A')
    tufts(g, [(18, 26), (24, 24), (36, 24), (44, 30), (20, 40), (34, 42)])
    g = shadeform(g)
    disc(g, 63, 26, 3.0, 'C')                                  # nose
    eye(g, 51, 22)
    poly(g, [(54, 29), (63, 29), (63, 31), (54, 32)], 'c')     # mouth line
    return dump(paint(g, 0.10))

# -------------------------------------------------------------- 1 hound
def dog_large(step):
    g = blank()
    taper(g, 14, 34, 3, 44, 5, 2, 'A')                         # long low tail
    if step:
        leg(g, 22, 38, 17, 49, 16, 58, 7); leg(g, 42, 38, 47, 49, 48, 58, 7)
        leg(g, 28, 40, 27, 50, 26, 58, 6); leg(g, 47, 40, 49, 50, 50, 58, 6)
    else:
        leg(g, 22, 38, 19, 49, 19, 58, 7); leg(g, 42, 38, 44, 49, 44, 58, 7)
        leg(g, 29, 40, 31, 50, 32, 58, 6); leg(g, 48, 40, 46, 50, 45, 58, 6)
    poly(g, [(18, 26), (40, 22), (50, 26), (50, 38), (40, 42), (22, 38)], 'A')   # deep chest
    ellipse(g, 44, 30, 12, 11, 'A')
    ellipse(g, 24, 32, 10, 8, 'A')                             # tucked waist
    taper(g, 46, 28, 54, 20, 11, 8, 'A')                       # long neck
    ellipse(g, 55, 17, 8, 7, 'A')
    poly(g, [(58, 14), (63, 17), (63, 23), (57, 23)], 'A')     # long muzzle
    poly(g, [(48, 12), (55, 6), (58, 16)], 'A')                # folded ears
    poly(g, [(44, 14), (50, 7), (52, 17)], 'A')
    g = shadeform(g)
    disc(g, 63, 19, 2.6, 'C')
    eye(g, 57, 15, 2.2)
    return dump(paint(g, 0.10))

# --------------------------------------------------------------- 2 frog
def frog(step):
    g = blank()
    k = 0 if step else 3
    for s in (-1, 1):                                          # folded back legs
        poly(g, [(32 + s*16, 34), (32 + s*27, 22 - k), (32 + s*31, 34),
                 (32 + s*24, 44), (32 + s*15, 42)], 'A')
        taper(g, 32 + s*28, 36, 32 + s*30, 52, 8, 6, 'A')
        for i in range(3):
            taper(g, 32 + s*30, 52, 32 + s*(34 + i*4), 58 + i, 5, 2.5, 'A')
    ellipse(g, 32, 36, 22, 16, 'A')                            # body
    poly(g, [(16, 30), (48, 30), (50, 20), (14, 20)], 'A')     # brow
    for s in (-1, 1):                                          # front feet
        taper(g, 32 + s*10, 46, 32 + s*13, 57, 6, 5, 'A')
        for i in range(3):
            taper(g, 32 + s*13, 57, 32 + s*(10 + i*5), 62, 4, 2, 'A')
    for s in (-1, 1): disc(g, 32 + s*12, 18, 9, 'A')           # eye domes
    g = shadeform(g)
    ellipse(g, 32, 44, 14, 9, 'C')                             # pale belly
    for s in (-1, 1):
        if step: disc(g, 32 + s*12, 18, 4.5, 'o')              # blink
        else: eye(g, 32 + s*12, 17, 4.5)
    poly(g, [(14, 30), (50, 30), (50, 33), (14, 33)], 'c')     # wide mouth
    return dump(paint(g, 0.10))

# --------------------------------------------------------------- 3 toad
def toad(step):
    g = blank()
    k = 0 if step else 2
    for s in (-1, 1):
        poly(g, [(32 + s*18, 36), (32 + s*29, 26 - k), (32 + s*32, 38),
                 (32 + s*26, 48), (32 + s*17, 46)], 'A')
        taper(g, 32 + s*29, 42, 32 + s*31, 56, 9, 7, 'A')
        for i in range(3):
            taper(g, 32 + s*31, 56, 32 + s*(35 + i*4), 61 + (i & 1), 5, 2.5, 'A')
    ellipse(g, 32, 40, 26, 17, 'A')
    poly(g, [(12, 34), (52, 34), (54, 22), (10, 22)], 'A')
    for s in (-1, 1):
        taper(g, 32 + s*11, 50, 32 + s*15, 59, 7, 6, 'A')
        for i in range(3):
            taper(g, 32 + s*15, 59, 32 + s*(11 + i*6), 63, 4, 2, 'A')
    for s in (-1, 1): disc(g, 32 + s*13, 20, 10, 'A')
    g = shadeform(g)
    for (wx, wy) in ((20, 38), (28, 44), (38, 40), (46, 46), (24, 50), (42, 52),
                     (16, 44), (34, 34), (48, 36)):
        disc(g, wx, wy, 2.4, 'd'); put(g, wx - 1, wy - 1, 'A')
    for s in (-1, 1):
        if step: disc(g, 32 + s*13, 20, 5.0, 'o')
        else: eye(g, 32 + s*13, 19, 5.0)
    poly(g, [(10, 34), (54, 34), (54, 38), (10, 38)], 'c')
    return dump(paint(g, 0.10))

# ----------------------------------------------------------- 4 songbird
def songbird(step):
    g = blank()
    poly(g, [(18, 30), (4, 44), (2, 54), (16, 46), (22, 38)], 'A')   # fanned tail
    for i in range(3):
        line_on(g, 16, 36 + i*4, 3, 46 + i*3, 'd', 'A')
    ellipse(g, 32, 34, 18, 15, 'A')                            # body
    ellipse(g, 47, 20, 11, 10, 'A')                            # head
    poly(g, [(54, 17), (63, 21), (54, 25)], 'C')               # beak
    if step:
        poly(g, [(24, 26), (18, 10), (34, 18), (40, 32), (28, 36)], 'A')   # wing up
    else:
        poly(g, [(24, 28), (26, 40), (40, 44), (44, 32), (34, 24)], 'A')   # folded
    g = shadeform(g)
    if not step:
        for i in range(3):
            line_on(g, 26 + i*2, 32 + i*3, 42, 36 + i*2, 'd', 'A')
    for lx in (28, 38):                                        # legs and toes
        taper(g, lx, 46, lx + 2, 56, 4, 3, 'C')
        for i in range(3): taper(g, lx + 2, 56, lx + 6 - i*5, 61, 3, 1.5, 'C')
    eye(g, 50, 18, 3.0)
    return dump(paint(g, 0.10))

SHAPES = []
for fn in (dog_small, dog_large, frog, toad, songbird):
    SHAPES += [fn(False), fn(True)]
