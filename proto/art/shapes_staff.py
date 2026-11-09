# -*- coding: utf-8 -*-
"""Six staves. The shaft leans slightly so the sprite is not a column,
   and every head sits in the top third where the eye lands first."""
from pixlib import *
import math

BOT = (26, 62); TOP = (36, 20)

def shaft(g, top=TOP, w=6, knots=()):
    haft(g, BOT[0], BOT[1], top[0], top[1], w)
    for t in knots:
        c = (BOT[0] + (top[0]-BOT[0])*t, BOT[1] + (top[1]-BOT[1])*t)
        disc(g, c[0], c[1], w*0.75, 'G')
        line_on(g, c[0]-w*0.7, c[1]-1, c[0]+w*0.7, c[1]-1, 'H', 'G')
        line_on(g, c[0]-w*0.7, c[1]+2, c[0]+w*0.7, c[1]+2, 'g', 'G')

def ferrule(g, t=0.80, w=7.5, h=4):
    c = (BOT[0] + (TOP[0]-BOT[0])*t, BOT[1] + (TOP[1]-BOT[1])*t)
    poly(g, [(c[0]-w/2, c[1]-h), (c[0]+w/2, c[1]-h), (c[0]+w/2, c[1]+h), (c[0]-w/2, c[1]+h)], 'C')
    line_on(g, c[0]-w/2, c[1]-h+1, c[0]+w/2, c[1]-h+1, 'W', 'C')
    line_on(g, c[0]-w/2, c[1]+h-1, c[0]+w/2, c[1]+h-1, 'c', 'C')
    return c

def st_orb():
    g = blank(); shaft(g); ferrule(g, 0.86)
    for a in (-1.0, -0.35, 0.35, 1.0):                   # four brass prongs
        poly(g, [(36, 20), (36 + 13*a, 7), (36 + 10*a, 16)], 'C')
    disc(g, 36, 12, 10, 'C')                             # orb
    disc(g, 36, 12, 8, 'A'); disc(g, 36, 12, 8, 'A')
    g = shadeform(g, 'A', 'd', 'B')
    disc(g, 33, 9, 2.4, 'W')
    ring(g, 36, 12, 10, 1.6, 'c')
    return g

def st_crystal():
    g = blank(); shaft(g); ferrule(g, 0.84)
    poly(g, [(36, 20), (45, 14), (40, 2), (33, 1), (27, 13)], 'C')
    line_on(g, 36, 2, 36, 20, 'c', 'C')                  # facet lines
    line_on(g, 29, 12, 40, 7, 'c', 'C')
    line_on(g, 33, 1, 44, 14, 'c', 'C')
    poly(g, [(34, 4), (38, 5), (37, 11), (33, 10)], 'W')
    return g

def st_crescent():
    g = blank(); shaft(g); ferrule(g, 0.84)
    ring(g, 36, 20, 16, 5.5, 'C')
    rect(g, 0, 21, 63, 63, '.')                          # keep only the top arc
    shaft(g); ferrule(g, 0.84)
    for k in (-1, 1):                                    # horns tipping up
        poly(g, [(36 + k*16, 20), (36 + k*22, 8), (36 + k*12, 14)], 'C')
    disc(g, 36, 16, 3.2, 'W')
    return g

def st_lantern():
    g = blank(); shaft(g, (34, 26)); ferrule(g, 0.72)
    poly(g, [(23, 24), (47, 24), (44, 20), (26, 20)], 'C')      # cap
    rect(g, 24, 4, 46, 22, 'C')
    rect(g, 28, 8, 42, 20, 'A')
    g = shadeform(g, 'A', 'd', 'B')
    rect(g, 30, 10, 36, 16, 'W')
    for x in (28, 35, 42): line_on(g, x, 6, x, 21, 'c', 'A')    # bars
    poly(g, [(26, 4), (44, 4), (41, 1), (29, 1)], 'C')
    return g

def st_branch():
    g = blank()
    pts = [(26, 62), (29, 50), (26, 40), (31, 30), (28, 20), (33, 10)]
    for i in range(len(pts)-1):
        haft(g, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], 6.5 - i*0.4)
    for (bx, by, tx, ty) in ((27, 45, 17, 38), (30, 27, 41, 22), (28, 36, 38, 34)):
        haft(g, bx, by, tx, ty, 3.4)
    for (kx, ky) in ((28, 54), (28, 34), (31, 16)):
        disc(g, kx, ky, 4.0, 'G'); disc(g, kx, ky, 1.6, 'g')
    disc(g, 33, 8, 6.5, 'A')                                    # lashed stone
    g = shadeform(g, 'A', 'd', 'B')
    for k in (-2, 2): line_on(g, 26, 8+k, 40, 8+k, 'C', 'A')
    return g

def st_totem():
    g = blank(); shaft(g, (34, 24)); ferrule(g, 0.74)
    ellipse(g, 33, 14, 10, 10, 'A')
    poly(g, [(25, 18), (41, 18), (39, 26), (27, 26)], 'A')      # jaw
    g = shadeform(g, 'A', 'd', 'B')
    for ex in (29, 37): disc(g, ex, 12, 2.8, 'o')
    for ex in (29, 37): put(g, ex-1, 11, 'c')
    for jx in (28, 31, 34, 37): line_on(g, jx, 19, jx, 25, 'o', 'A')
    for k in (-1, 1):                                           # hanging rings
        ring(g, 33 + k*13, 30, 4.5, 1.8, 'C')
        line(g, 33 + k*9, 24, 33 + k*13, 27, 'C', 1)
    poly(g, [(27, 5), (33, 0), (39, 5), (33, 8)], 'C')          # crest
    return g

SHAPES = [dump(outline(despeckle(f()))) for f in
          (st_orb, st_crystal, st_crescent, st_lantern, st_branch, st_totem)]
