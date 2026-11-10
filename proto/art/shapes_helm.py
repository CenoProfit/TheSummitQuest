# -*- coding: utf-8 -*-
"""Seven head pieces. Every face opening is filled with 'd' shadow; left
   transparent it reads as a hole punched through the head."""
from pixlib import *
CX = 32

def comb(g, cx, y0, y1, w=3.0, ch='C'):
    """the raised crest down the centre line of a helm"""
    poly(g, [(cx - w, y0 + 2), (cx, y0), (cx + w, y0 + 2), (cx + w * 0.7, y1), (cx - w * 0.7, y1)], ch)
    line_on(g, cx, y0, cx, y1, 'Z', ch, 0.9)
    line_on(g, cx + w * 0.55, y0 + 2, cx + w * 0.45, y1, 'x', ch, 0.9)

def rivets(g, x0, x1, y, n=5, r=1.5):
    for i in range(n):
        stud(g, x0 + (x1 - x0) * i / float(n - 1), y, r)

def slit(g, x0, x1, y, h=5):
    """a cut through the plate, with the lip of the metal above it"""
    rect(g, x0, y, x1, y + h, 'q')
    line_on(g, x0, y - 1, x1, y - 1, 'W', 'A', 0.9)
    line_on(g, x0, y + h + 1, x1, y + h + 1, 'd', 'A', 0.9)

def hm_hood():
    g = blank()
    poly(g, [(14, 22), (22, 8), (42, 8), (50, 22), (52, 44), (46, 56), (18, 56), (12, 44)], 'A')
    g = model(g)
    ellipse(g, CX, 31, 12, 14, 'd')
    ellipse(g, CX, 31, 10, 12, 'q')
    for k in (-1, 1):
        poly(g, [(CX + k*14, 24), (CX + k*20, 34), (CX + k*18, 52), (CX + k*12, 48)], 'A')
    folds(g, 14, 50, 10, 54, n=5)
    poly(g, [(18, 50), (46, 50), (44, 58), (20, 58)], 'C')
    line_on(g, 19, 51, 45, 51, 'Z', 'C', 0.9)
    for k in (-1, 1): stud(g, CX + k*9, 54, 1.8)
    strap(g, 20, 20, 44, 20, 2.6)
    return g

def hm_horned():
    g = blank()
    for k in (-1, 1):
        poly(g, [(CX + k*16, 26), (CX + k*30, 10), (CX + k*26, 2),
                 (CX + k*34, 6), (CX + k*32, 20), (CX + k*20, 32)], 'C')
        line_on(g, CX + k*18, 25, CX + k*31, 8, 'Z', 'C', 0.9)
        line_on(g, CX + k*20, 30, CX + k*31, 17, 'x', 'C', 0.9)
    ellipse(g, CX, 30, 18, 20, 'A')
    rect(g, 10, 44, 54, 56, 'A')
    g = model(g)
    slit(g, 14, 50, 33, 6)
    rect(g, 29, 32, 35, 54, 'A')
    line_on(g, 30, 32, 30, 54, 'W', 'A', 0.9)
    rect(g, 12, 24, 52, 30, 'C')
    line_on(g, 12, 25, 52, 25, 'Z', 'C', 0.9)
    line_on(g, 12, 29, 52, 29, 'x', 'C', 0.9)
    rivets(g, 16, 48, 27, 5, 1.7)
    comb(g, CX, 8, 24, 2.6)
    return g

def hm_great():
    g = blank()
    poly(g, [(13, 6), (51, 6), (54, 18), (54, 48), (46, 60), (18, 60), (10, 48), (10, 18)], 'A')
    g = model(g)
    slit(g, 13, 51, 27, 6)
    rect(g, 29, 22, 35, 37, 'A')
    line_on(g, 30, 22, 30, 37, 'W', 'A', 0.9)
    for y in (18, 40):
        rect(g, 11, y, 53, y + 4, 'C')
        line_on(g, 11, y + 1, 53, y + 1, 'Z', 'C', 0.9)
        line_on(g, 11, y + 3, 53, y + 3, 'x', 'C', 0.9)
        rivets(g, 15, 49, y + 2, 5, 1.5)
    for bx in (22, 28, 34, 40):
        for by in (47, 52): disc(g, bx, by, 1.7, 'q')
    comb(g, CX, 3, 18, 3.0)
    return g

def hm_crown():
    g = blank()
    pts = [(10, 44), (14, 16), (21, 34), (26, 10), (32, 30), (38, 10), (43, 34), (50, 16), (54, 44)]
    poly(g, pts + [(54, 52), (10, 52)], 'C')
    rect(g, 10, 42, 54, 50, 'C')
    g = model(g)
    line_on(g, 10, 43, 54, 43, 'Z', 'C', 1.0)
    line_on(g, 10, 49, 54, 49, 'x', 'C', 1.0)
    for (px, py) in ((14, 18), (26, 12), (38, 12), (50, 18)):
        stud(g, px, py, 2.4, 'A', 'W')
    for fx in (18, 30, 42):                     # filigree between the points
        poly(g, [(fx, 36), (fx + 3, 32), (fx + 6, 36), (fx + 3, 40)], 'Y')
        put(g, fx + 3, 36, 'x')
    disc(g, CX, 46, 5.5, 'A'); disc(g, CX - 1, 45, 3.0, 'W'); disc(g, CX, 44, 1.4, 'V')
    return g

def hm_brim():
    g = blank()
    poly(g, [(22, 30), (28, 4), (38, 4), (44, 30)], 'A')
    ellipse(g, CX, 36, 30, 9, 'A')
    g = model(g)
    folds(g, 24, 42, 6, 29, n=3)
    poly(g, [(22, 28), (44, 28), (45, 34), (21, 34)], 'C')
    line_on(g, 21, 29, 45, 29, 'Z', 'C', 0.9)
    line_on(g, 21, 33, 45, 33, 'x', 'C', 0.9)
    rect(g, 38, 27, 44, 35, 'G'); rect(g, 39.5, 29.5, 42.5, 32.5, 'x')
    ellipse(g, CX, 41, 26, 4, 'd')
    ring(g, CX, 36, 30, 2.0, 'd')
    return g

def hm_barbute():
    g = blank()
    poly(g, [(14, 10), (50, 10), (54, 26), (52, 50), (44, 60), (20, 60), (12, 50), (10, 26)], 'A')
    g = model(g)
    poly(g, [(24, 22), (28, 22), (30, 38), (34, 38), (36, 22), (40, 22),
             (40, 52), (24, 52)], 'q')
    for (lx, ly) in ((24, 22), (40, 22)): line_on(g, lx, ly - 1, lx + 4, ly - 1, 'W', 'A', 0.9)
    comb(g, CX, 5, 22, 3.2)
    rect(g, 12, 14, 52, 19, 'C')
    line_on(g, 12, 15, 52, 15, 'Z', 'C', 0.9)
    line_on(g, 12, 18, 52, 18, 'x', 'C', 0.9)
    rivets(g, 16, 48, 16, 5, 1.5)
    rivets(g, 16, 48, 56, 5, 1.4)
    return g

def hm_cap():
    g = blank()
    ellipse(g, CX, 30, 20, 16, 'A')
    rect(g, 12, 30, 52, 34, 'A')
    g = model(g)
    comb(g, CX, 14, 31, 2.4)
    rect(g, 12, 32, 52, 38, 'C')
    line_on(g, 12, 33, 52, 33, 'Z', 'C', 0.9)
    line_on(g, 12, 37, 52, 37, 'x', 'C', 0.9)
    for k in (-1, 1):
        poly(g, [(CX + k*13, 38), (CX + k*22, 38), (CX + k*20, 56), (CX + k*11, 52)], 'G')
        line_on(g, CX + k*14, 40, CX + k*20, 40, 'H', 'G', 0.9)
        line_on(g, CX + k*14, 50, CX + k*19, 50, 'j', 'G', 0.9)
        stud(g, CX + k*17, 46, 1.8)
    rivets(g, 16, 48, 35, 5, 1.5)
    return g

def hm_crown_grand():
    """The one legendary helm. Same classic open circlet as the rare
       crowns, but a king's version of it: five tall points instead of
       four, a pearl on every tip, three cut stones set in the band and
       studs between them."""
    g = blank()
    pts = [(7, 42), (12, 16), (17, 32), (22, 8), (27, 28), (32, 1),
           (37, 28), (42, 8), (47, 32), (52, 16), (57, 42)]
    poly(g, pts + [(57, 54), (7, 54)], 'C')
    poly(g, [(7, 38), (57, 38), (57, 54), (7, 54)], 'C')
    g = model(g)
    for (px, top) in ((12, 16), (22, 8), (32, 1), (42, 8), (52, 16)):
        line_on(g, px - 1, top + 3, px - 1, 38, 'Z', 'C', 1.0)   # lit edge
        line_on(g, px + 2, top + 4, px + 2, 38, 'x', 'C', 1.0)   # shaded edge
        stud(g, px, top + 1.5, 2.6, 'A', 'W')                    # pearl
    line_on(g, 7, 39, 57, 39, 'Z', 'C', 1.1)
    line_on(g, 7, 53, 57, 53, 'x', 'C', 1.1)
    line_on(g, 7, 48, 57, 48, 'x', 'C', 0.9)
    for gx in (18, 32, 46): gem(g, gx, 45, 4.6, 'A', 6)
    for nx in (11, 25, 39, 53): stud(g, nx, 45, 2.2, 'A', 'W')
    for nx in (14, 22, 28, 36, 42, 50): stud(g, nx, 51, 1.3)
    return g

SHAPES = [dump(paint(f())) for f in
          (hm_hood, hm_horned, hm_great, hm_crown, hm_brim, hm_barbute, hm_cap,
           hm_crown_grand)]
