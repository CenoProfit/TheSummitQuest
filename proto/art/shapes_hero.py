# -*- coding: utf-8 -*-
"""The climber, seen from behind, and every layer that goes on him.

   SHAPES order:
     0,1,2   body, three walk frames
     3       the wizard hat, worn when the head slot is empty
     4-10    head layers,  helm shapes 0-6
     11-15   body layers,  chest shapes 0-4
     16-19   feet layers,  boot shapes 0-3
     20      a plain walking stick, carried when the hand is empty
     21      his hands, drawn over the gear so he grips it

   Proportions: he stands 58 of the 64 rows and is 30 wide at the
   shoulder. The first attempt made him as wide as he was tall and he
   read as a barrel with a bucket on it.
"""
import pixlib as P
from pixlib import *

P.setsize(64)
CX = 32
HEAD_Y = 12; HEAD_R = 9.6
SH_Y   = 25                 # shoulder line
WAIST  = 41
HEM    = 47
GROUND = 61

def legs(step):
    g = blank()
    lift = ((0, 0), (0, 2), (2, 0))[step]
    for i, k in enumerate((-1, 1)):
        lx = CX + k * 5.5
        taper(g, lx, HEM - 1, lx, GROUND - lift[i], 8, 7, 'G')
    return g

def arms(g):
    for k in (-1, 1):
        taper(g, CX + k * 10, SH_Y + 1, CX + k * 13, WAIST, 7, 6, 'A')
        disc(g, CX + k * 13, WAIST + 2, 3.4, 'm')

def shell(g, ch='A', sh=11, wa=9, hm=14):
    """the torso silhouette every chest layer shares"""
    poly(g, [(CX - sh, SH_Y), (CX + sh, SH_Y), (CX + wa, WAIST),
             (CX + hm, HEM), (CX - hm, HEM), (CX - wa, WAIST)], ch)

def body(step):
    g = legs(step)
    shell(g)
    arms(g)
    # Neck: about half the width of the skull, and mostly hidden under
    # the jaw. Six pixels was a stalk; twelve was a tree trunk.
    poly(g, [(CX - 4.6, HEAD_Y + 4), (CX + 4.6, HEAD_Y + 4),
             (CX + 5.0, SH_Y + 1), (CX - 5.0, SH_Y + 1)], 'm')
    # Skull, then a squared jaw under it. A plain disc narrows to a point
    # where it meets the neck, which is what made the head look pinched.
    ellipse(g, CX, HEAD_Y - 1, HEAD_R, HEAD_R * 0.80, 'm')
    poly(g, [(CX - HEAD_R * 0.94, HEAD_Y - 3), (CX + HEAD_R * 0.94, HEAD_Y - 3),
             (CX + HEAD_R * 0.78, HEAD_Y + 7), (CX - HEAD_R * 0.78, HEAD_Y + 7)], 'm')
    poly(g, [(CX - 10, HEAD_Y - 7), (CX + 10, HEAD_Y - 7), (CX + 10.4, HEAD_Y + 3),
             (CX + 6, HEAD_Y - 1), (CX - 6, HEAD_Y - 1), (CX - 10.4, HEAD_Y + 3)], 'G')
    g = model(g)
    poly(g, [(CX - 11, WAIST - 3), (CX + 11, WAIST - 3), (CX + 11, WAIST), (CX - 11, WAIST)], 'C')
    stud(g, CX, WAIST - 1.5, 2.2)
    poly(g, [(CX - 14, HEM - 3), (CX + 14, HEM - 3), (CX + 14, HEM), (CX - 14, HEM)], 'C')
    g = ao(g); g = rim(g); g = dither(g); g = despeckle(g)
    return dump(softline(outline(g)))

def fin(g):
    g = ao(g); g = rim(g); g = dither(g); g = despeckle(g)
    return dump(softline(outline(g)))

def hands():
    """Just his hands, drawn OVER whatever he is carrying so his fingers
       close around the grip. Skin only, never the sleeve, because the
       sleeve belongs to whichever chest piece he has on and this layer
       has to sit correctly under all of them."""
    g = blank()
    for k in (-1, 1):
        cx = CX + k * 13
        disc(g, cx, WAIST + 2.5, 4.2, 'm')
        poly(g, [(cx - k*1.0, WAIST - 1.0), (cx + k*3.6, WAIST + 0.6),
                 (cx + k*3.2, WAIST + 3.2), (cx - k*1.4, WAIST + 2.0)], 'm')
    g = model(g)
    for k in (-1, 1):
        cx = CX + k * 13
        line_on(g, cx - 3.4, WAIST + 1.0, cx + 3.4, WAIST + 1.0, 'u', 'm', 0.9)
        line_on(g, cx - 3.0, WAIST + 3.4, cx + 3.0, WAIST + 3.4, 'u', 'm', 0.9)
    return fin(g)

def stick():
    g = blank()
    haft(g, 47, SH_Y - 7, 45, GROUND, 3.6)
    disc(g, 47.5, SH_Y - 10, 4.4, 'C'); disc(g, 46.5, SH_Y - 11, 2.0, 'Z')
    return fin(model(g))

def hat():
    g = blank()
    poly(g, [(CX, 0), (CX + 10, HEAD_Y - 1), (CX - 10, HEAD_Y - 1)], 'A')
    ellipse(g, CX, HEAD_Y + 1, 16, 4.4, 'A')
    g = model(g)
    poly(g, [(CX - 9, HEAD_Y - 5), (CX + 9, HEAD_Y - 5), (CX + 10, HEAD_Y - 1), (CX - 10, HEAD_Y - 1)], 'C')
    stud(g, CX + 6, HEAD_Y - 3, 1.9)
    return fin(g)

# ---------------------------------------------------------------- heads
def dome(g, r=None, drop=0, ch='A'):
    r = r or (HEAD_R + 1.6)
    ellipse(g, CX, HEAD_Y + drop - 1, r, r * 0.86, ch)
    poly(g, [(CX - r * 0.96, HEAD_Y + drop - 1), (CX + r * 0.96, HEAD_Y + drop - 1),
             (CX + r * 0.82, HEAD_Y + drop + r * 0.86), (CX - r * 0.82, HEAD_Y + drop + r * 0.86)], ch)

def H_hood():
    g = blank(); dome(g, HEAD_R + 2.6)
    poly(g, [(CX - 12, HEAD_Y), (CX + 12, HEAD_Y), (CX + 14, SH_Y + 3), (CX - 14, SH_Y + 3)], 'A')
    g = model(g)
    poly(g, [(CX - 12, SH_Y), (CX + 12, SH_Y), (CX + 12, SH_Y + 3), (CX - 12, SH_Y + 3)], 'C')
    return fin(g)

def H_horned():
    g = blank()
    for k in (-1, 1):
        poly(g, [(CX + k*8, HEAD_Y - 3), (CX + k*22, HEAD_Y - 12), (CX + k*18, HEAD_Y - 4),
                 (CX + k*24, HEAD_Y - 6), (CX + k*12, HEAD_Y + 4)], 'C')
    dome(g)
    g = model(g)
    poly(g, [(CX - 10, HEAD_Y - 1), (CX + 10, HEAD_Y - 1), (CX + 10, HEAD_Y + 3), (CX - 10, HEAD_Y + 3)], 'C')
    for sx in (-6, 0, 6): stud(g, CX + sx, HEAD_Y + 1, 1.7)
    return fin(g)

def H_great():
    g = blank()
    poly(g, [(CX - 10, HEAD_Y - 11), (CX + 10, HEAD_Y - 11), (CX + 12, HEAD_Y - 5),
             (CX + 12, HEAD_Y + 8), (CX + 9, HEAD_Y + 12), (CX - 9, HEAD_Y + 12),
             (CX - 12, HEAD_Y + 8), (CX - 12, HEAD_Y - 5)], 'A')
    g = model(g)
    rect(g, CX - 10, HEAD_Y - 1, CX + 10, HEAD_Y + 1, 'q')
    for y in (-7, 5): rect(g, CX - 11, HEAD_Y + y, CX + 11, HEAD_Y + y + 1, 'C')
    for sx in (-7, 0, 7): stud(g, CX + sx, HEAD_Y - 6, 1.4); stud(g, CX + sx, HEAD_Y + 6, 1.4)
    return fin(g)

def H_crown():
    g = blank()
    pts = [(CX - 11, HEAD_Y + 4), (CX - 10, HEAD_Y - 8), (CX - 5, HEAD_Y - 2),
           (CX, HEAD_Y - 11), (CX + 5, HEAD_Y - 2), (CX + 10, HEAD_Y - 8), (CX + 11, HEAD_Y + 4)]
    poly(g, pts, 'C')
    rect(g, CX - 11, HEAD_Y + 1, CX + 11, HEAD_Y + 4, 'C')
    g = model(g)
    for (px, py) in ((-9, -7), (0, -10), (9, -7)): stud(g, CX + px, HEAD_Y + py, 1.6, 'A', 'W')
    stud(g, CX, HEAD_Y + 1.5, 2.4, 'A', 'W')
    return fin(g)

def H_brim():
    g = blank()
    poly(g, [(CX, HEAD_Y - 13), (CX + 9, HEAD_Y), (CX - 9, HEAD_Y)], 'A')
    ellipse(g, CX, HEAD_Y + 2, 17, 4.2, 'A')
    g = model(g)
    poly(g, [(CX - 8, HEAD_Y - 4), (CX + 8, HEAD_Y - 4), (CX + 9, HEAD_Y), (CX - 9, HEAD_Y)], 'C')
    return fin(g)

def H_barbute():
    g = blank()
    poly(g, [(CX - 10, HEAD_Y - 12), (CX + 10, HEAD_Y - 12), (CX + 13, HEAD_Y - 4),
             (CX + 12, HEAD_Y + 9), (CX + 7, HEAD_Y + 13), (CX - 7, HEAD_Y + 13),
             (CX - 12, HEAD_Y + 9), (CX - 13, HEAD_Y - 4)], 'A')
    g = model(g)
    poly(g, [(CX - 2, HEAD_Y - 13), (CX + 2, HEAD_Y - 13), (CX + 1, HEAD_Y - 3), (CX - 1, HEAD_Y - 3)], 'C')
    rect(g, CX - 12, HEAD_Y - 7, CX + 12, HEAD_Y - 6, 'C')
    for sx in (-8, 0, 8): stud(g, CX + sx, HEAD_Y - 6.5, 1.4)
    return fin(g)

def H_cap():
    g = blank(); dome(g, HEAD_R + 0.8, -1)
    g = model(g)
    rect(g, CX - 9, HEAD_Y + 1, CX + 9, HEAD_Y + 4, 'C')
    for k in (-1, 1):
        poly(g, [(CX + k*8, HEAD_Y + 4), (CX + k*12, HEAD_Y + 4),
                 (CX + k*11, HEAD_Y + 13), (CX + k*7, HEAD_Y + 11)], 'G')
    for sx in (-6, 0, 6): stud(g, CX + sx, HEAD_Y + 2.5, 1.4)
    return fin(g)

# --------------------------------------------------------------- bodies
# These are the same five pieces as the icons, worn. They are built
# with the same helpers so a fluted cuirass in the pack is a fluted
# cuirass on his back, not a differently shaped grey rectangle.
def B_cuirass():
    g = blank()
    pauldron(g, CX - 8, SH_Y - 2, -1, w=13, h=8, plates=3)
    pauldron(g, CX + 8, SH_Y - 1, 1, w=11, h=7, plates=2)
    shell(g)
    g = model(g)
    flute(g, CX, SH_Y + 2, CX, HEM - 4, n=3, spread=5, bow=0.8)
    line_on(g, CX, SH_Y + 1, CX, HEM - 3, 'V', 'B', 0.9)
    lames(g, CX - 13, CX + 13, HEM - 7, HEM, n=2)
    gorget(g, CX, SH_Y - 2, 8, 3)
    strap(g, CX - 11, SH_Y + 7, CX + 11, SH_Y + 11, 2.6)
    return fin(g)

def B_scale():
    g = blank()
    pauldron(g, CX - 8, SH_Y - 1, -1, w=11, h=7, plates=2)
    pauldron(g, CX + 8, SH_Y, 1, w=12, h=8, plates=3)
    shell(g); g = model(g)
    for row in range(8):
        y = SH_Y + 3 + row * 2.6
        t = (y - SH_Y) / float(HEM - SH_Y)
        half = 11 - 2.0 * t
        off = 1.3 if row % 2 else 0
        scales(g, CX - half + off, CX + half, y, y, step=2.7, r=1.5)
    gorget(g, CX, SH_Y - 2, 9, 3)
    strap(g, CX - 10, SH_Y + 2, CX + 9, SH_Y + 12, 2.6)
    return fin(g)

def B_robe():
    g = blank()
    for k, w in ((-1, 18), (1, 17)):
        poly(g, [(CX + k*9, SH_Y), (CX + k*w, SH_Y + 5),
                 (CX + k*(w-1), HEM - 3), (CX + k*9, HEM - 5)], 'A')
    shell(g, 'A', 11, 10, 15)
    g = model(g)
    folds(g, CX - 10, CX + 10, SH_Y + 3, HEM - 1, n=5)
    poly(g, [(CX - 2, SH_Y - 2), (CX + 2, SH_Y - 2), (CX + 1, WAIST), (CX - 1, WAIST)], 'd')
    poly(g, [(CX - 13, WAIST - 3), (CX + 13, WAIST - 3), (CX + 12, WAIST + 1), (CX - 12, WAIST + 1)], 'C')
    poly(g, [(CX + 5, WAIST + 1), (CX + 9, WAIST + 1), (CX + 8, HEM - 2), (CX + 5, HEM - 3)], 'C')
    disc(g, CX, SH_Y + 1, 2.4, 'C'); put(g, CX - 1, SH_Y, 'Z')
    return fin(g)

def B_banded():
    g = blank()
    pauldron(g, CX - 8, SH_Y - 1, -1, w=12, h=6, plates=3)
    pauldron(g, CX + 8, SH_Y - 1, 1, w=12, h=6, plates=3)
    shell(g); g = model(g)
    lames(g, CX - 12, CX + 12, SH_Y + 2, HEM - 2, n=5)
    gorget(g, CX, SH_Y - 2, 8, 3)
    for k in (-1, 1): strap(g, CX + k*7, SH_Y + 1, CX + k*9, HEM - 3, 2.2, False)
    return fin(g)

def B_carapace():
    g = blank()
    for k, w, h in ((-1, 16, 9), (1, 14, 8)):
        poly(g, [(CX + k*6, SH_Y), (CX + k*w, SH_Y + h),
                 (CX + k*(w-1), HEM - 4), (CX + k*7, HEM - 2)], 'A')
    shell(g, 'A', 10, 9, 13)
    g = model(g)
    for i in range(7):
        y = SH_Y + i * 3.4
        poly(g, [(CX, y), (CX + 4, y + 1.6), (CX, y + 3.4), (CX - 4, y + 1.6)], 'C')
        line_on(g, CX - 3, y + 1.6, CX + 3, y + 1.6, 'Z', 'C', 0.9)
    for k in (-1, 1):
        for i in range(4):
            y = SH_Y + 4 + i * 5
            line_on(g, CX + k*7, y, CX + k*15, y + 2, 'q', 'A', 1.0)
            line_on(g, CX + k*7, y - 1.1, CX + k*15, y + 0.9, 'W', 'A', 0.8)
    return fin(g)

# ----------------------------------------------------------------- feet
def foot(g, k, top, cuff=None, knee=False):
    lx = CX + k * 5.5
    poly(g, [(lx - 4.5, top), (lx + 4.5, top), (lx + 4.5, GROUND - 1), (lx - 4.5, GROUND - 1)], 'A')
    if knee: disc(g, lx, top + 3, 4.6, 'A')
    if cuff: ellipse(g, lx, top, 6.2, 3.0, 'G')
    poly(g, [(lx - 5.5, GROUND - 3), (lx + 5.5, GROUND - 3), (lx + 5.5, GROUND), (lx - 5.5, GROUND)], 'C')

def F(top, cuff=False, knee=False):
    def build():
        g = blank()
        for k in (-1, 1): foot(g, k, top, cuff, knee)
        return fin(model(g))
    return build

SHAPES = [body(0), body(1), body(2), hat()]
SHAPES += [f() for f in (H_hood, H_horned, H_great, H_crown, H_brim, H_barbute, H_cap)]
SHAPES += [f() for f in (B_cuirass, B_scale, B_robe, B_banded, B_carapace)]
SHAPES += [F(HEM - 1)(), F(HEM - 4, knee=True)(), F(GROUND - 7)(), F(HEM - 1, cuff=True)()]
SHAPES += [stick(), hands()]
P.setsize(96)
