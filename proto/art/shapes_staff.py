# -*- coding: utf-8 -*-
"""Six staves. The shaft leans slightly so the sprite is not a column,
   and every head sits in the top third where the eye lands first."""
from pixlib import *
import math

BOT = (26, 62); TOP = (36, 20)

def shaft(g, top=TOP, w=6, knots=(), binds=(0.22, 0.46)):
    haft(g, BOT[0], BOT[1], top[0], top[1], w)
    for t in binds:                       # leather bindings up the shaft
        c = (BOT[0] + (top[0]-BOT[0])*t, BOT[1] + (top[1]-BOT[1])*t)
        cordwrap(g, c[0]-1, c[1]+4, c[0]+1, c[1]-4, w, 3)
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
    disc(g, 36, 12, 10.5, 'c')
    gem(g, 36, 12, 9.2, 'A', 8)                          # a cut orb, not a ball
    for a in (-1.0, -0.42, 0.42, 1.0):                   # claw prongs over it
        poly(g, [(36 + 2.4*a, 22), (36 + 13*a, 5), (36 + 9.5*a, 7), (36 + 5*a, 20)], 'C')
        hornridge(g, 36 + 3*a, 20, 36 + 12*a, 6, 3)
    ring(g, 36, 12, 10.5, 1.4, 'x')
    return g

def st_crystal():
    g = blank(); shaft(g); ferrule(g, 0.84)
    poly(g, [(36, 20), (45, 14), (40, 2), (33, 1), (27, 13)], 'C')
    for (ax, ay, bx, by) in ((36,2,36,20),(29,12,40,7),(33,1,44,14),(31,6,41,18)):
        line_on(g, ax, ay, bx, by, 'x', 'C', 1.0)
        line_on(g, ax+1, ay, bx+1, by, 'Z', 'C', 0.8)
    poly(g, [(34, 4), (38, 5), (37, 11), (33, 10)], 'Z')
    for (sx, sy, sr) in ((30, 22, 3.0), (43, 19, 2.4)):  # shards floating off
        poly(g, [(sx, sy-sr), (sx+sr*0.7, sy), (sx, sy+sr), (sx-sr*0.7, sy)], 'C')
    return g

def st_crescent():
    g = blank(); shaft(g); ferrule(g, 0.84)
    ring(g, 36, 20, 16, 5.5, 'C')
    rect(g, 0, 21, 63, 63, '.')                          # keep only the top arc
    # up INTO the gem, not to the hollow inside the arc, where the shaft
    # ended a row short of anything and the crescent floated
    shaft(g, (36, 13)); ferrule(g, 0.84)
    for k in (-1, 1):                                    # horns tipping up
        poly(g, [(36 + k*16, 20), (36 + k*22, 8), (36 + k*12, 14)], 'C')
        hornridge(g, 36 + k*14, 18, 36 + k*21, 9, 4)
    # The gem is the mount: it has to reach from the shaft top to the
    # inner edge of the arc, or the crescent hangs in the air above a
    # staff that threads up through its hollow touching nothing.
    gem(g, 36, 10, 5.2, 'A', 6)
    return g

def st_lantern():
    g = blank(); shaft(g, (34, 22)); ferrule(g, 0.72)
    poly(g, [(23, 24), (47, 24), (44, 20), (26, 20)], 'C')      # cap
    rect(g, 24, 4, 46, 22, 'C')
    rect(g, 28, 8, 42, 20, 'A')
    g = shadeform(g, 'A', 'd', 'B')
    gem(g, 33, 13, 5.0, 'A', 6)
    for x in (28, 35, 42): line_on(g, x, 6, x, 21, 'x', 'A')    # bars
    nails(g, [(26, 6), (44, 6), (26, 21), (44, 21)], 1.2)
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
    disc(g, 33, 8, 7.0, 'A')                                    # lashed stone
    for k in (-2.4, 2.4):
        cordwrap(g, 26, 8+k, 41, 8+k, 3.2, 4)
        line_on(g, 26, 8+k, 41, 8+k, 'C', 'A', 1.1)
    for (kx, ky) in ((30, 6), (36, 10)): disc(g, kx, ky, 1.6, 'd')
    return g

def st_totem():
    g = blank(); shaft(g, (34, 20)); ferrule(g, 0.74)
    ellipse(g, 33, 14, 10, 10, 'A')
    poly(g, [(25, 18), (41, 18), (39, 26), (27, 26)], 'A')      # jaw
    g = shadeform(g, 'A', 'd', 'B')
    for ex in (29, 37):
        disc(g, ex, 12, 3.2, 'q'); disc(g, ex, 12, 1.6, 'x'); put(g, ex-1, 11, 'Z')
    for jx in (28, 31, 34, 37): line_on(g, jx, 19, jx, 26, 'q', 'A', 1.1)
    poly(g, [(31, 16), (35, 16), (34, 19), (32, 19)], 'q')      # nose hollow
    for k in (-1, 1):                                           # hanging charms
        # the hanger has to REACH the ring, and the ring the pendant;
        # ending inside the ring's hole left all three floating apart
        ring(g, 33 + k*13, 30, 4.5, 1.8, 'C')
        line(g, 33 + k*6, 22, 33 + k*13, 26, 'C', 2)
        poly(g, [(33 + k*13, 32.5), (33 + k*16, 44), (33 + k*11, 42)], 'G')
    gem(g, 33, 4, 4.0, 'C', 5)                                  # crest stone
    poly(g, [(27, 6), (33, 0), (39, 6), (33, 9)], 'C')
    return g

SHAPES = [dump(paint(f())) for f in
          (st_orb, st_crystal, st_crescent, st_lantern, st_branch, st_totem)]
