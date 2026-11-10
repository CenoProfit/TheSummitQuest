# -*- coding: utf-8 -*-
"""Six shields, each filling the frame so the face has room for a device."""
from pixlib import *
import math
CX = 32

def rimstuds(g, pts, r=2.0):
    for (x, y) in pts: stud(g, x, y, r)

def sh_round():
    g = blank()
    disc(g, CX, 32, 28, 'C')                       # brass rim
    disc(g, CX, 32, 24.5, 'A')                     # planked face
    g = shadeform(g, 'A', 'd', 'B')
    for x in range(CX-22, CX+23, 7): line_on(g, x, 6, x, 58, 'd', 'A')
    for x in range(CX-21, CX+24, 7): line_on(g, x, 6, x, 58, 'B', 'A')
    disc(g, CX, 32, 9, 'C'); disc(g, CX, 32, 6, 'W'); disc(g, CX, 32, 4, 'C')
    rimstuds(g, [(CX + 26*math.cos(a), 32 + 26*math.sin(a))
                 for a in [i*math.pi/4 for i in range(8)]])
    return g

def sh_kite():
    g = blank()
    poly(g, [(9, 10), (55, 10), (52, 34), (32, 60), (12, 34)], 'C')
    poly(g, [(13, 14), (51, 14), (48, 33), (32, 55), (16, 33)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    poly(g, [(29, 17), (35, 17), (35, 46), (29, 46)], 'C')      # cross
    poly(g, [(18, 26), (46, 26), (46, 32), (18, 32)], 'C')
    rimstuds(g, [(13, 13), (51, 13), (15, 32), (49, 32), (32, 56)])
    return g

def sh_tower():
    """Three full-width bands made it read as a barrel. A tall shield
       needs a flat top, a vertical spine and corner plates instead."""
    g = blank()
    poly(g, [(11, 3), (53, 3), (56, 16), (54, 46), (32, 61), (10, 46), (8, 16)], 'C')
    poly(g, [(15, 8), (49, 8), (51, 18), (50, 44), (32, 56), (14, 44), (13, 18)], 'A')
    g = shadeform(g, 'A', 'd', 'B')
    for x in range(17, 48, 6): line_on(g, x, 8, x, 56, 'd', 'A')      # planking
    for x in range(18, 49, 6): line_on(g, x, 8, x, 56, 'B', 'A')
    poly(g, [(27, 6), (37, 6), (37, 50), (32, 58), (27, 50)], 'C')    # spine
    line_on(g, 28, 7, 28, 50, 'W', 'C')
    line_on(g, 36, 7, 36, 50, 'c', 'C')
    for sy in (14, 26, 38): stud(g, 32, sy, 2.4, 'A', 'W')
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
    disc(g, CX, 32, 11, 'C'); disc(g, CX, 31, 7.5, 'W'); disc(g, CX, 32, 5, 'C')
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
    poly(g, [(27, 22), (37, 22), (35, 29), (32, 34), (29, 29)], 'W')
    rimstuds(g, [(12, 9), (52, 9), (11, 28), (53, 28), (32, 55)])
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
    disc(g, CX, 32, 8, 'C'); disc(g, CX, 31, 5, 'W')
    return g

SHAPES = [dump(paint(f())) for f in
          (sh_round, sh_kite, sh_tower, sh_buckler, sh_heater, sh_spiked)]
