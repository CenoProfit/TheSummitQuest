# -*- coding: utf-8 -*-
"""Seven head pieces. Every face opening is filled with 'd' shadow; left
   transparent it reads as a hole punched through the head."""
from pixlib import *
CX = 32

def hm_hood():
    g = blank()
    poly(g, [(14, 22), (22, 8), (42, 8), (50, 22), (52, 44), (46, 56), (18, 56), (12, 44)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    ellipse(g, CX, 31, 12, 14, 'd')                      # the face, in shadow
    for k in (-1, 1):                                    # folds falling at the sides
        poly(g, [(CX + k*14, 24), (CX + k*20, 34), (CX + k*18, 52), (CX + k*12, 48)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    poly(g, [(18, 50), (46, 50), (44, 58), (20, 58)], 'C')   # throat band
    return g

def hm_horned():
    g = blank()
    for k in (-1, 1):                                    # horns, behind the dome
        poly(g, [(CX + k*16, 26), (CX + k*30, 10), (CX + k*26, 2),
                 (CX + k*34, 6), (CX + k*32, 20), (CX + k*20, 32)], 'C')
    ellipse(g, CX, 30, 18, 20, 'A')
    rect(g, 10, 44, 54, 56, 'A')
    g = shadeform(g, 'A', 'd', 'B')
    rect(g, 14, 32, 50, 42, 'd')                         # eye slot
    rect(g, 29, 32, 35, 52, 'A')                         # nose guard
    rect(g, 12, 24, 52, 30, 'C')                         # brow band
    line_on(g, 12, 25, 52, 25, 'W', 'C')
    for sx in (18, 26, 38, 46): stud(g, sx, 27, 1.8)
    return g

def hm_great():
    g = blank()
    poly(g, [(13, 6), (51, 6), (54, 18), (54, 48), (46, 60), (18, 60), (10, 48), (10, 18)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    rect(g, 13, 26, 51, 33, 'd')                         # eye slit
    rect(g, 29, 22, 35, 37, 'A')                         # centre bar
    for y in (18, 40):                                   # riveted bands
        rect(g, 11, y, 53, y+4, 'C')
        line_on(g, 11, y+1, 53, y+1, 'W', 'C')
    for sx in (16, 26, 38, 48):
        stud(g, sx, 20, 1.6); stud(g, sx, 42, 1.6)
    for bx in (22, 28, 34, 40):                          # breath holes
        for by in (47, 52): disc(g, bx, by, 1.6, 'd')
    return g

def hm_crown():
    g = blank()
    pts = [(10, 44), (14, 16), (21, 34), (26, 10), (32, 30), (38, 10), (43, 34), (50, 16), (54, 44)]
    poly(g, pts + [(54, 52), (10, 52)], 'C')
    g = shadeform(g, 'C', 'c', 'C')
    rect(g, 10, 42, 54, 50, 'C')
    line_on(g, 10, 43, 54, 43, 'W', 'C')
    line_on(g, 10, 49, 54, 49, 'c', 'C')
    for (px, py) in ((14, 18), (26, 12), (38, 12), (50, 18)): stud(g, px, py, 2.2, 'A', 'W')
    disc(g, CX, 46, 5.5, 'A'); disc(g, CX, 45, 3.2, 'W')   # the stone in front
    return g

def hm_brim():
    g = blank()
    poly(g, [(22, 30), (28, 4), (38, 4), (44, 30)], 'A')     # crown
    ellipse(g, CX, 36, 30, 9, 'A')                           # brim
    g = shadeform(g, 'A', 'd', 'B')
    poly(g, [(22, 28), (44, 28), (45, 34), (21, 34)], 'C')   # band
    line_on(g, 21, 29, 45, 29, 'W', 'C')
    ellipse(g, CX, 41, 26, 4, 'd')                           # under the brim
    return g

def hm_barbute():
    g = blank()
    poly(g, [(14, 10), (50, 10), (54, 26), (52, 50), (44, 60), (20, 60), (12, 50), (10, 26)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    poly(g, [(24, 22), (28, 22), (30, 38), (34, 38), (36, 22), (40, 22),
             (40, 52), (24, 52)], 'd')                       # the Y opening
    poly(g, [(28, 5), (36, 5), (34, 22), (30, 22)], 'C')     # crest
    rect(g, 12, 14, 52, 19, 'C')
    line_on(g, 12, 15, 52, 15, 'W', 'C')
    for sx in (16, 24, 40, 48): stud(g, sx, 16, 1.6)
    return g

def hm_cap():
    g = blank()
    ellipse(g, CX, 30, 20, 16, 'A')
    rect(g, 12, 30, 52, 34, 'A')
    g = shadeform(g, 'A', 'd', 'B')
    rect(g, 12, 32, 52, 38, 'C')                             # band
    line_on(g, 12, 33, 52, 33, 'W', 'C')
    for k in (-1, 1):                                        # cheek flaps
        poly(g, [(CX + k*13, 38), (CX + k*22, 38), (CX + k*20, 56), (CX + k*11, 52)], 'G')
    for sx in (18, 26, 38, 46): stud(g, sx, 35, 1.7)
    return g

SHAPES = [dump(paint(f())) for f in
          (hm_hood, hm_horned, hm_great, hm_crown, hm_brim, hm_barbute, hm_cap)]
