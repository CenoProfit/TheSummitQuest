# -*- coding: utf-8 -*-
"""Six shields, each filling the frame so the face has room for a device."""
from pixlib import *
import math
CX = 32

def rimstuds(g, pts, r=2.0):
    for (x, y) in pts: stud(g, x, y, r)

def damage(g, pts, body='A'):
    """nicks taken out of the rim and gouges across the face"""
    for i, (x, y, r) in enumerate(pts):
        if i % 2: disc(g, x, y, r, '.')
        else:
            disc(g, x, y, r, 'q'); put(g, x - 1, y - 1, 'd')

def planks(g, x0, x1, y0, y1, n=5, body='A'):
    for i in range(1, n):
        x = x0 + (x1 - x0) * i / float(n)
        line_on(g, x, y0, x, y1, 'q', body, 1.2)
        line_on(g, x + 1.3, y0, x + 1.3, y1, 'B', body, 0.9)

def sh_round():
    g = blank()
    disc(g, CX, 32, 28, 'C')                       # brass rim
    disc(g, CX, 32, 24.5, 'A')                     # planked face
    g = shadeform(g, 'A', 'd', 'B')
    for x in range(CX-22, CX+23, 7): line_on(g, x, 6, x, 58, 'd', 'A')
    for x in range(CX-21, CX+24, 7): line_on(g, x, 6, x, 58, 'B', 'A')
    disc(g, CX, 32, 10, 'c'); disc(g, CX, 32, 8.4, 'C')
    gem(g, CX, 32, 5.2, 'A', 6)
    nails(g, [(CX + 20*math.cos(a), 32 + 20*math.sin(a))
              for a in [i*math.pi/6 for i in range(12)]], 1.2)
    rimstuds(g, [(CX + 26*math.cos(a), 32 + 26*math.sin(a))
                 for a in [i*math.pi/4 for i in range(8)]])
    damage(g, [(50, 14, 2.6), (16, 46, 2.2), (44, 50, 1.8)])
    return g

def sh_kite():
    g = blank()
    poly(g, [(9, 10), (55, 10), (52, 34), (32, 60), (12, 34)], 'C')
    poly(g, [(13, 14), (51, 14), (48, 33), (32, 55), (16, 33)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    poly(g, [(29, 17), (35, 17), (35, 46), (29, 46)], 'C')      # cross
    poly(g, [(18, 26), (46, 26), (46, 32), (18, 32)], 'C')
    line_on(g, 30, 17, 30, 46, 'Z', 'C', 0.9)
    line_on(g, 18, 31, 46, 31, 'x', 'C', 0.9)
    gem(g, 32, 29, 4.0, 'A', 5)
    nails(g, [(16, 17), (48, 17), (16, 38), (48, 38), (32, 50)], 1.3)
    rimstuds(g, [(13, 13), (51, 13), (15, 32), (49, 32), (32, 56)])
    damage(g, [(50, 22, 2.4), (14, 24, 1.8)])
    return g

def sh_tower():
    """Three full-width bands made it read as a barrel. A tall shield
       needs a flat top, a vertical spine and corner plates instead."""
    g = blank()
    poly(g, [(11, 3), (53, 3), (56, 16), (54, 46), (32, 61), (10, 46), (8, 16)], 'C')
    poly(g, [(15, 8), (49, 8), (51, 18), (50, 44), (32, 56), (14, 44), (13, 18)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    planks(g, 15, 50, 8, 56, 6)
    poly(g, [(27, 6), (37, 6), (37, 50), (32, 58), (27, 50)], 'C')    # spine
    line_on(g, 28, 7, 28, 50, 'W', 'C')
    line_on(g, 36, 7, 36, 50, 'c', 'C')
    for sy in (14, 26, 38): stud(g, 32, sy, 2.6, 'A', 'W')
    gem(g, 32, 44, 4.2, 'A', 5)
    for (px, py) in ((14, 9), (50, 9), (12, 42), (52, 42)):           # corner plates
        poly(g, [(px-4, py-3), (px+4, py-3), (px+4, py+5), (px-4, py+5)], 'C')
        stud(g, px, py + 1, 1.8, 'A', 'W')
    return g

def sh_buckler():
    g = blank()
    disc(g, CX, 32, 23, 'C')
    disc(g, CX, 32, 19.5, 'A')
    g = shadeform(g, 'A', 'd', 'B')
    ring(g, CX, 32, 15, 2.0, 'c')
    disc(g, CX, 32, 11.5, 'c'); disc(g, CX, 32, 10, 'C')
    gem(g, CX, 32, 6.0, 'A', 6)
    for k in (-1, 1):                                # grip strap behind
        poly(g, [(CX + k*20, 26), (CX + k*27, 29), (CX + k*27, 36), (CX + k*20, 39)], 'G')
    rimstuds(g, [(CX + 21*math.cos(a), 32 + 21*math.sin(a))
                 for a in [i*math.pi/3 for i in range(6)]], 1.8)
    return g

def sh_heater():
    g = blank()
    poly(g, [(8, 6), (56, 6), (54, 30), (32, 59), (10, 30)], 'C')
    poly(g, [(13, 11), (51, 11), (49, 30), (32, 53), (15, 30)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    poly(g, [(23, 18), (41, 18), (38, 30), (32, 40), (26, 30)], 'C')   # device
    poly(g, [(27, 22), (37, 22), (35, 29), (32, 34), (29, 29)], 'A')
    line_on(g, 24, 19, 40, 19, 'Z', 'C', 0.9)
    gem(g, 32, 25, 3.4, 'A', 5)
    nails(g, [(17, 14), (47, 14), (17, 30), (47, 30)], 1.3)
    rimstuds(g, [(12, 9), (52, 9), (11, 28), (53, 28), (32, 55)])
    damage(g, [(46, 40, 2.4), (18, 20, 1.8), (36, 46, 2.0)])
    return g

def sh_spiked():
    g = blank()
    for i in range(6):                                # spikes first, behind
        a = -math.pi/2 + i*math.pi/3 + 0.26
        poly(g, [(CX + 22*math.cos(a-0.16), 32 + 22*math.sin(a-0.16)),
                 (CX + 31*math.cos(a),      32 + 31*math.sin(a)),
                 (CX + 22*math.cos(a+0.16), 32 + 22*math.sin(a+0.16))], 'C')
    disc(g, CX, 32, 23, 'C')
    disc(g, CX, 32, 20, 'A')
    g = shadeform(g, 'A', 'd', 'B')
    for (bx, by, br) in ((24, 24, 3.0), (40, 38, 2.6), (28, 42, 2.2)):
        disc(g, bx, by, br, 'd')                      # battered face
    disc(g, CX, 32, 9, 'c'); disc(g, CX, 32, 7.6, 'C')
    gem(g, CX, 32, 4.4, 'A', 6)
    for i in range(6):
        a = -math.pi/2 + i*math.pi/3 + 0.26
        hornridge(g, CX + 22*math.cos(a), 32 + 22*math.sin(a),
                     CX + 30*math.cos(a), 32 + 30*math.sin(a), 3)
    return g

SHAPES = [dump(paint(f())) for f in
          (sh_round, sh_kite, sh_tower, sh_buckler, sh_heater, sh_spiked)]
