# -*- coding: utf-8 -*-
"""Five torso pieces.

   Each hangs as a torso with two shoulders and no head, and each has a
   deliberately different shoulder line, because in a grid of a dozen
   armours the shoulders are what you tell apart at a glance. The
   pauldrons are not mirrored: a matched pair of perfect arcs is the
   thing that reads as machine made."""
from pixlib import *
CX = 32
TOP, WAIST, HEM = 15, 38, 58

def torso(g, shoulder=15, waist=12, bot=HEM, ch='A'):
    poly(g, [(CX - shoulder, TOP), (CX + shoulder, TOP),
             (CX + waist, WAIST), (CX + waist + 2, bot), (CX - waist - 2, bot),
             (CX - waist, WAIST)], ch)

def ch_cuirass():
    """Plate. Fluted centre, a gorget at the throat, layered pauldrons
       and a fauld of lames hanging off the waist."""
    g = blank()
    pauldron(g, CX - 10, TOP - 1, -1, w=19, h=12, plates=3)
    pauldron(g, CX + 10, TOP + 1, 1, w=16, h=10, plates=2)
    torso(g, 15, 12, 50)
    poly(g, [(CX - 15, 48), (CX + 15, 48), (CX + 17, 60), (CX - 17, 60)], 'A')
    g = model(g)
    flute(g, CX, TOP + 4, CX, 47, n=3, spread=7, bow=1.2)
    line_on(g, CX, TOP + 2, CX, 48, 'V', 'B', 0.9)
    lames(g, CX - 15, CX + 15, 48, 60, n=3)
    gorget(g, CX, TOP - 1, 11, 4)
    strap(g, CX - 14, 26, CX + 14, 32, 3.2)
    for sx in (-13, 13): stud(g, CX + sx, WAIST, 1.5)
    return g

def ch_scale():
    """Mail. Real overlapping rows that narrow with the waist, a brass
       collar and a leather shoulder strap over the top."""
    g = blank()
    pauldron(g, CX - 10, TOP, -1, w=15, h=9, plates=2)
    pauldron(g, CX + 10, TOP + 2, 1, w=17, h=10, plates=3)
    torso(g, 15, 12)
    g = model(g)
    for row in range(13):
        y = TOP + 4 + row * 3.3
        t = (y - TOP) / float(HEM - TOP)
        half = 14 - 2.4 * t
        off = 1.7 if row % 2 else 0
        scales(g, CX - half + off, CX + half, y, y, step=3.4, r=1.9)
    gorget(g, CX, TOP - 1, 12, 4)
    strap(g, CX - 13, 22, CX + 12, 36, 3.4)
    return g

def ch_robe():
    """Cloth. Wide sleeves, drapery down the front, a sash with the
       ends hanging, and a brooch at the throat."""
    g = blank()
    for k, w, drop in ((-1, 26, 46), (1, 24, 42)):
        poly(g, [(CX + k * 10, TOP + 1), (CX + k * w, TOP + 10),
                 (CX + k * (w - 3), drop), (CX + k * 11, drop - 6)], 'A')
    torso(g, 13, 14, 62)
    g = model(g)
    folds(g, CX - 12, CX + 12, TOP + 6, 60, n=6)
    poly(g, [(CX - 3, TOP), (CX + 3, TOP), (CX + 1, 34), (CX - 1, 34)], 'd')
    for k in (-1, 1):
        folds(g, CX + k * 14, CX + k * 26, TOP + 12, 42, n=3)
    poly(g, [(CX - 16, 38), (CX + 16, 38), (CX + 15, 45), (CX - 15, 45)], 'C')
    line_on(g, CX - 16, 39, CX + 16, 39, 'Z', 'C', 0.9)
    poly(g, [(CX + 6, 44), (CX + 11, 44), (CX + 9, 58), (CX + 5, 56)], 'C')   # sash tail
    disc(g, CX, TOP + 2, 3.2, 'C'); disc(g, CX - 1, TOP + 1, 1.4, 'Z')
    return g

def ch_banded():
    """Lames over leather. The gaps between the bands are the point."""
    g = blank()
    pauldron(g, CX - 10, TOP, -1, w=16, h=8, plates=3)
    pauldron(g, CX + 10, TOP, 1, w=16, h=8, plates=3)
    torso(g, 15, 12)
    g = model(g)
    lames(g, CX - 14, CX + 14, TOP + 3, HEM - 2, n=7)
    gorget(g, CX, TOP - 1, 11, 4)
    for k in (-1, 1): strap(g, CX + k * 9, TOP + 2, CX + k * 11, HEM - 3, 2.6, False)
    return g

def ch_carapace():
    """Chitin. A raised segmented spine with curved side plates that
       overlap it, and no brass anywhere: this one did not come from a
       forge."""
    g = blank()
    for k, w, h in ((-1, 20, 13), (1, 18, 11)):
        poly(g, [(CX + k * 7, TOP), (CX + k * w, TOP + h),
                 (CX + k * (w - 2), 48), (CX + k * 8, 52)], 'A')
    torso(g, 12, 11, 56)
    g = model(g)
    for i in range(8):
        y = TOP + 1 + i * 5.2
        poly(g, [(CX, y), (CX + 5.5, y + 2.4), (CX, y + 5.2), (CX - 5.5, y + 2.4)], 'C')
        line_on(g, CX - 4, y + 2.4, CX + 4, y + 2.4, 'Z', 'C', 0.9)
        line_on(g, CX - 5, y + 4.0, CX + 5, y + 4.0, 'x', 'C', 0.9)
    for k in (-1, 1):
        for i in range(5):
            y = TOP + 6 + i * 8
            line_on(g, CX + k * 8, y, CX + k * 19, y + 3, 'q', 'A', 1.1)
            line_on(g, CX + k * 8, y - 1.2, CX + k * 19, y + 1.8, 'W', 'A', 0.9)
    return g

SHAPES = [dump(paint(f())) for f in
          (ch_cuirass, ch_scale, ch_robe, ch_banded, ch_carapace)]
