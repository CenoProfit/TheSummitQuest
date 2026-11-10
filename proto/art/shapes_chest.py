# -*- coding: utf-8 -*-
"""Five torso pieces. Each has a different shoulder line, because in a
   grid of a dozen armours the shoulders are what you tell apart."""
from pixlib import *
CX = 32

def torso(g, shoulder=16, waist=11, top=16, bot=56, ch='A'):
    poly(g, [(CX-shoulder, top), (CX+shoulder, top),
             (CX+waist, bot), (CX-waist, bot)], ch)

def ch_cuirass():
    g = blank()
    for k in (-1, 1):                                  # flared pauldrons
        poly(g, [(CX + k*12, 14), (CX + k*29, 18), (CX + k*27, 30), (CX + k*13, 28)], 'A')
    torso(g, 15, 12, 16, 54)
    poly(g, [(18, 52), (46, 52), (44, 60), (20, 60)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    line_on(g, CX, 17, CX, 58, 'B', 'A')               # centre ridge
    line_on(g, CX-1, 17, CX-1, 58, 'W', 'A')
    for k in (-1, 1):
        poly(g, [(CX + k*13, 15), (CX + k*29, 19), (CX + k*28, 23), (CX + k*13, 20)], 'C')
    poly(g, [(16, 54), (48, 54), (47, 59), (17, 59)], 'C')
    for sx in (22, 32, 42): stud(g, sx, 56, 1.7)
    return g

def ch_scale():
    g = blank()
    for k in (-1, 1):
        poly(g, [(CX + k*12, 15), (CX + k*25, 19), (CX + k*23, 28), (CX + k*13, 26)], 'A')
    torso(g, 15, 13, 15, 58)
    g = shadeform(g, 'A', 'd', 'B')
    for row in range(8):                               # real overlapping rows
        y = 22 + row*5
        off = 3 if row % 2 else 0
        for x in range(CX-16+off, CX+17, 6):
            disc(g, x, y, 2.6, 'A'); put(g, x-1, y-1, 'B'); put(g, x+1, y+2, 'd')
            disc(g, x, y+3, 0.1, 'o')
    poly(g, [(CX-14, 14), (CX+14, 14), (CX+13, 21), (CX-13, 21)], 'C')   # collar
    line_on(g, CX-14, 15, CX+14, 15, 'W', 'C')
    return g

def ch_robe():
    g = blank()
    for k in (-1, 1):                                  # wide sleeves
        poly(g, [(CX + k*11, 16), (CX + k*30, 24), (CX + k*28, 44), (CX + k*14, 36)], 'A')
    torso(g, 13, 16, 14, 60)
    g = shadeform(g, 'A', 'd', 'B')
    poly(g, [(CX-5, 14), (CX+5, 14), (CX+2, 34), (CX-2, 34)], 'd')       # the gap
    poly(g, [(CX-18, 40), (CX+18, 40), (CX+17, 47), (CX-17, 47)], 'C')   # sash
    line_on(g, CX-18, 41, CX+18, 41, 'W', 'C')
    disc(g, CX, 17, 4.0, 'C'); put(g, CX-1, 16, 'W')                     # brooch
    return g

def ch_banded():
    g = blank()
    for k in (-1, 1):
        poly(g, [(CX + k*12, 15), (CX + k*27, 20), (CX + k*25, 29), (CX + k*13, 27)], 'A')
    torso(g, 15, 13, 15, 58)
    g = shadeform(g, 'A', 'd', 'B')
    for i in range(6):                                 # lames with real gaps
        y = 22 + i*6
        rect(g, 14, y+4, 50, y+5, 'd')
        line_on(g, 14, y, 50, y, 'B', 'A')
        for sx in (18, 32, 46): stud(g, sx, y+2, 1.5)
    poly(g, [(CX-15, 14), (CX+15, 14), (CX+14, 20), (CX-14, 20)], 'C')
    return g

def ch_carapace():
    g = blank()
    for k in (-1, 1):                                  # curved side plates
        poly(g, [(CX + k*10, 14), (CX + k*28, 22), (CX + k*30, 40),
                 (CX + k*20, 56), (CX + k*12, 50)], 'A')
    torso(g, 12, 10, 12, 58)
    g = shadeform(g, 'A', 'd', 'B')
    for i in range(7):                                 # raised central spine
        y = 16 + i*6
        poly(g, [(CX, y), (CX+5, y+3), (CX, y+6), (CX-5, y+3)], 'C')
        put(g, CX-2, y+2, 'W')
    for k in (-1, 1):
        for i in range(4):
            line_on(g, CX + k*11, 22 + i*9, CX + k*27, 26 + i*9, 'd', 'A')
    return g

SHAPES = [dump(paint(f())) for f in
          (ch_cuirass, ch_scale, ch_robe, ch_banded, ch_carapace)]
