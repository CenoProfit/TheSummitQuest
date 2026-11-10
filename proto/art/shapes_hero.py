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
     22      the legendary crown, which has a shape of its own
     23      his right arm, reaching out and gripping what he carries

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

def H_crown_grand():
    """The legendary crown, worn. The first attempt put five short points
       close together and the modelling pass merged them into one lump;
       at this size a crown is its gaps, so the points are taller, wider
       apart, and each one carries a lit edge to hold it off its
       neighbour."""
    g = blank()
    TOPS = ((-11, -8), (-5.5, -13), (0, -16), (5.5, -13), (11, -8))
    VAL = HEAD_Y - 2
    pts = [(CX - 12.5, HEAD_Y + 3)]
    for (dx, dy) in TOPS:
        pts += [(CX + dx - 2.0, VAL), (CX + dx, HEAD_Y + dy), (CX + dx + 2.0, VAL)]
    pts.append((CX + 12.5, HEAD_Y + 3))
    poly(g, pts, 'C')
    poly(g, [(CX - 12.5, HEAD_Y + 1), (CX + 12.5, HEAD_Y + 1),
             (CX + 12.5, HEAD_Y + 7), (CX - 12.5, HEAD_Y + 7)], 'C')
    g = model(g)
    for (dx, dy) in TOPS:
        line_on(g, CX + dx - 0.9, HEAD_Y + dy + 1, CX + dx - 0.9, HEAD_Y + 2, 'Z', 'C', 1.0)
        line_on(g, CX + dx + 1.1, HEAD_Y + dy + 2, CX + dx + 1.1, HEAD_Y + 2, 'x', 'C', 1.0)
        disc(g, CX + dx, HEAD_Y + dy + 0.6, 1.5, 'A')
        put(g, CX + dx, HEAD_Y + dy, 'W')
    line_on(g, CX - 12.5, HEAD_Y + 2, CX + 12.5, HEAD_Y + 2, 'Z', 'C', 1.1)
    line_on(g, CX - 12.5, HEAD_Y + 6, CX + 12.5, HEAD_Y + 6, 'x', 'C', 1.1)
    for gx in (-7, 0, 7):
        disc(g, CX + gx, HEAD_Y + 4, 2.0, 'A')
        put(g, CX + gx - 1, HEAD_Y + 3, 'W')
    return fin(g)

def fin(g):
    g = ao(g); g = rim(g); g = dither(g); g = despeckle(g)
    return dump(softline(outline(g)))

def gripArm():
    """His right forearm, reaching out and closing on whatever he is
       carrying. The body layer hangs both arms straight down, which is
       right when his hands are empty and wrong the moment he picks
       something up: the staff stood beside an arm that was not holding
       it. Drawn over the carried piece, in the chest piece's own
       palette so the sleeve matches whatever he has on."""
    g = blank()
    taper(g, CX + 10, SH_Y + 1, CX + 16, WAIST - 1, 8, 7, 'A')
    g = model(g)
    disc(g, CX + 16.5, WAIST + 1.5, 4.0, 'm')
    poly(g, [(CX + 15.0, WAIST - 2.0), (CX + 19.0, WAIST - 0.6),
             (CX + 18.6, WAIST + 2.2), (CX + 14.6, WAIST + 1.0)], 'm')
    line_on(g, CX + 13.2, WAIST + 0.4, CX + 19.6, WAIST + 0.4, 'u', 'm', 0.9)
    line_on(g, CX + 13.4, WAIST + 2.8, CX + 19.4, WAIST + 2.8, 'u', 'm', 0.9)
    return fin(g)

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
    """His own walking staff, carried when the hand slot is empty. It
       used to start at his shoulder and end at his ear, which read as a
       pole stuck to his side; it stands the full height of him now, the
       way an equipped staff does, so the two swap cleanly."""
    g = blank()
    haft(g, 50, 7, 47, GROUND + 1, 3.8)
    cordwrap(g, 49.4, 20, 48.6, 30, 3.8, 4)
    poly(g, [(45.6, 36), (50.4, 36), (50.2, 40), (45.4, 40)], 'C')   # ferrule
    poly(g, [(45.0, GROUND - 3), (49.8, GROUND - 3),
             (49.6, GROUND + 1), (44.8, GROUND + 1)], 'C')           # shod heel
    disc(g, 50.4, 5.4, 4.6, 'c'); disc(g, 50.4, 5.4, 3.6, 'C')
    disc(g, 49.6, 4.4, 1.6, 'Z')
    for k in (-1, 1):                                                 # the claw
        poly(g, [(50.4 + k*1.4, 11), (50.4 + k*5.2, 3), (50.4 + k*3.0, 10)], 'C')
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
# Every one of these is seen from BEHIND, so none of them has a face
# opening, a visor or a nose guard to show. What a helmet gives you from
# the back is its crown, its banding, its rivets, whatever rises off the
# top of it, and how it finishes at the neck. That is what these are
# built out of, matching the same features on their icons.

def dome(g, r=None, drop=0, ch='A'):
    r = r or (HEAD_R + 1.6)
    ellipse(g, CX, HEAD_Y + drop - 1, r, r * 0.86, ch)
    poly(g, [(CX - r * 0.96, HEAD_Y + drop - 1), (CX + r * 0.96, HEAD_Y + drop - 1),
             (CX + r * 0.82, HEAD_Y + drop + r * 0.86), (CX - r * 0.82, HEAD_Y + drop + r * 0.86)], ch)

def band(g, y, h=3.0, w=12.0, studs=3):
    poly(g, [(CX - w, y), (CX + w, y), (CX + w, y + h), (CX - w, y + h)], 'C')
    line_on(g, CX - w, y + 0.7, CX + w, y + 0.7, 'Z', 'C', 0.9)
    line_on(g, CX - w, y + h - 0.7, CX + w, y + h - 0.7, 'x', 'C', 0.9)
    if studs:
        for i in range(studs):
            sx = CX - w * 0.72 + (w * 1.44) * i / float(studs - 1)
            stud(g, sx, y + h * 0.5, 1.3, 'A', 'W')

def comb(g, y0, y1, w=2.6):
    """A raised ridge down the crown. It used to be drawn standing above
       the helm, which on a head this near the top of the sprite meant it
       was cut off at y=0 and the helm read as a plain box."""
    poly(g, [(CX - w, y0 + 2), (CX, y0), (CX + w, y0 + 2),
             (CX + w * 0.7, y1), (CX - w * 0.7, y1)], 'C')
    line_on(g, CX - 0.6, y0 + 1, CX - 0.6, y1, 'Z', 'C', 0.9)
    line_on(g, CX + w * 0.5, y0 + 2, CX + w * 0.45, y1, 'x', 'C', 0.9)

def neckguard(g, y, w=11.0, drop=5.0, ch='A'):
    """the lames at the back of a helm that cover the nape"""
    poly(g, [(CX - w, y), (CX + w, y), (CX + w * 0.86, y + drop), (CX - w * 0.86, y + drop)], ch)
    for i in range(2):
        yy = y + drop * (i + 1) / 3.0
        line_on(g, CX - w, yy, CX + w, yy, 'q', ch, 1.0)
        line_on(g, CX - w, yy - 1, CX + w, yy - 1, 'W', ch, 0.9)

def H_hood():
    g = blank(); dome(g, HEAD_R + 2.8)
    poly(g, [(CX - 12, HEAD_Y), (CX + 12, HEAD_Y),
             (CX + 15, SH_Y + 4), (CX - 15, SH_Y + 4)], 'A')
    g = model(g)
    folds(g, CX - 12, CX + 12, HEAD_Y - 7, SH_Y + 3, n=4)
    poly(g, [(CX - 14, SH_Y), (CX + 14, SH_Y),
             (CX + 14, SH_Y + 4), (CX - 14, SH_Y + 4)], 'C')
    line_on(g, CX - 14, SH_Y + 0.8, CX + 14, SH_Y + 0.8, 'Z', 'C', 0.9)
    for sx in (-9, 0, 9): stud(g, CX + sx, SH_Y + 2, 1.3, 'A', 'W')
    return fin(g)

def H_horned():
    g = blank()
    for k in (-1, 1):                                   # horns, behind the dome
        poly(g, [(CX + k*8, HEAD_Y - 3), (CX + k*23, HEAD_Y - 13),
                 (CX + k*19, HEAD_Y - 4), (CX + k*25, HEAD_Y - 7),
                 (CX + k*12, HEAD_Y + 4)], 'C')
        hornridge(g, CX + k*10, HEAD_Y, CX + k*22, HEAD_Y - 11, 4)
    dome(g)
    neckguard(g, HEAD_Y + 8, 10.0, 5.0)
    g = model(g)
    comb(g, HEAD_Y - 9, HEAD_Y - 1, 2.2)
    band(g, HEAD_Y - 1.5, 3.2, 11.0, 3)
    return fin(g)

def H_great():
    g = blank()
    poly(g, [(CX - 7, HEAD_Y - 13), (CX + 7, HEAD_Y - 13), (CX + 11, HEAD_Y - 7),
             (CX + 12, HEAD_Y + 6), (CX + 14, HEAD_Y + 12), (CX - 14, HEAD_Y + 12),
             (CX - 12, HEAD_Y + 6), (CX - 11, HEAD_Y - 7)], 'A')
    ellipse(g, CX, HEAD_Y - 10, 8.0, 3.4, 'A')
    g = model(g)
    comb(g, HEAD_Y - 10, HEAD_Y - 7, 2.8)
    band(g, HEAD_Y - 7, 2.8, 12.0, 4)
    band(g, HEAD_Y + 5, 2.8, 12.0, 4)
    for bx in (-6, -2, 2, 6):                           # breath holes round the back
        disc(g, CX + bx, HEAD_Y + 10, 1.0, 'q')
    for sx in (-10, 10):
        for sy in (-2, 1, 4): stud(g, CX + sx, HEAD_Y + sy, 1.2)
    return fin(g)

def H_crown():
    g = blank()
    pts = [(CX - 11, HEAD_Y + 4), (CX - 10, HEAD_Y - 8), (CX - 5, HEAD_Y - 2),
           (CX, HEAD_Y - 11), (CX + 5, HEAD_Y - 2), (CX + 10, HEAD_Y - 8), (CX + 11, HEAD_Y + 4)]
    poly(g, pts + [(CX + 11, HEAD_Y + 7), (CX - 11, HEAD_Y + 7)], 'C')
    poly(g, [(CX - 11, HEAD_Y + 1), (CX + 11, HEAD_Y + 1),
             (CX + 11, HEAD_Y + 7), (CX - 11, HEAD_Y + 7)], 'C')
    g = model(g)
    for (px, top) in ((CX - 10, HEAD_Y - 8), (CX, HEAD_Y - 11), (CX + 10, HEAD_Y - 8)):
        line_on(g, px - 0.8, top + 1, px - 0.8, HEAD_Y + 2, 'Z', 'C', 1.0)
        line_on(g, px + 1.2, top + 2, px + 1.2, HEAD_Y + 2, 'x', 'C', 1.0)
        stud(g, px, top + 0.6, 1.5, 'A', 'W')
    line_on(g, CX - 11, HEAD_Y + 2, CX + 11, HEAD_Y + 2, 'Z', 'C', 1.0)
    line_on(g, CX - 11, HEAD_Y + 6, CX + 11, HEAD_Y + 6, 'x', 'C', 1.0)
    for gx in (-6, 0, 6): gem(g, CX + gx, HEAD_Y + 4, 2.0, 'A', 5)
    return fin(g)

def H_brim():
    g = blank()
    poly(g, [(CX, HEAD_Y - 14), (CX + 9, HEAD_Y), (CX - 9, HEAD_Y)], 'A')
    ellipse(g, CX, HEAD_Y + 2, 17, 4.4, 'A')
    g = model(g)
    folds(g, CX - 7, CX + 7, HEAD_Y - 12, HEAD_Y - 1, n=3)
    poly(g, [(CX - 9, HEAD_Y - 4), (CX + 9, HEAD_Y - 4),
             (CX + 10, HEAD_Y), (CX - 10, HEAD_Y)], 'C')
    line_on(g, CX - 9, HEAD_Y - 3.2, CX + 9, HEAD_Y - 3.2, 'Z', 'C', 0.9)
    poly(g, [(CX + 4, HEAD_Y - 5), (CX + 8, HEAD_Y - 5),
             (CX + 8, HEAD_Y + 1), (CX + 4, HEAD_Y + 1)], 'G')
    put(g, CX + 6, HEAD_Y - 2, 'x')
    ellipse(g, CX, HEAD_Y + 4, 14, 2.4, 'd')            # under the brim
    return fin(g)

def H_barbute():
    g = blank()
    poly(g, [(CX - 10, HEAD_Y - 12), (CX + 10, HEAD_Y - 12), (CX + 13, HEAD_Y - 4),
             (CX + 12, HEAD_Y + 9), (CX + 7, HEAD_Y + 13), (CX - 7, HEAD_Y + 13),
             (CX - 12, HEAD_Y + 9), (CX - 13, HEAD_Y - 4)], 'A')
    g = model(g)
    comb(g, HEAD_Y - 11, HEAD_Y - 3, 3.0)
    band(g, HEAD_Y - 7, 2.6, 12.5, 4)
    for sx in (-9, -3, 3, 9): stud(g, CX + sx, HEAD_Y + 11, 1.2)
    line_on(g, CX - 12, HEAD_Y + 4, CX + 12, HEAD_Y + 4, 'q', 'A', 1.0)
    line_on(g, CX - 12, HEAD_Y + 3, CX + 12, HEAD_Y + 3, 'W', 'A', 0.9)
    return fin(g)

def H_cap():
    g = blank(); dome(g, HEAD_R + 0.8, -1)
    g = model(g)
    comb(g, HEAD_Y - 9, HEAD_Y, 2.0)
    band(g, HEAD_Y + 1, 3.2, 10.0, 3)
    for k in (-1, 1):                                   # cheek flaps, laced
        poly(g, [(CX + k*9, HEAD_Y + 4), (CX + k*13, HEAD_Y + 4),
                 (CX + k*12, HEAD_Y + 13), (CX + k*8, HEAD_Y + 11)], 'G')
        line_on(g, CX + k*9, HEAD_Y + 6, CX + k*12, HEAD_Y + 6, 'K', 'G', 0.9)
        line_on(g, CX + k*9, HEAD_Y + 10, CX + k*12, HEAD_Y + 10, 'j', 'G', 0.9)
        stud(g, CX + k*11, HEAD_Y + 8, 1.2)
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
# These were four plain rectangles with a strip of brass across the toe,
# which is why they looked nothing like their icons. Each one is built
# from the same parts its icon is: a cuff, eyelets and laces, a knee
# cop, straps, fur, and a sole with tread cut into it.

def boot_shell(g, k, top, w=4.6):
    lx = CX + k * 5.5
    poly(g, [(lx - w, top), (lx + w, top), (lx + w, GROUND - 2), (lx - w, GROUND - 2)], 'A')
    return lx

def boot_sole(g, lx, w=5.6):
    poly(g, [(lx - w, GROUND - 3), (lx + w, GROUND - 3),
             (lx + w, GROUND), (lx - w, GROUND)], 'C')
    line_on(g, lx - w, GROUND - 2.4, lx + w, GROUND - 2.4, 'Z', 'C', 0.9)
    for i in (-3.2, -1.0, 1.2, 3.4):
        line_on(g, lx + i, GROUND - 1.6, lx + i, GROUND, 'x', 'C', 0.9)

def F_trail():
    g = blank()
    for k in (-1, 1): boot_shell(g, k, HEM - 2)
    g = model(g)
    for k in (-1, 1):
        lx = CX + k * 5.5
        poly(g, [(lx - 5.4, HEM - 4), (lx + 5.4, HEM - 4),
                 (lx + 5.0, HEM + 1), (lx - 5.0, HEM + 1)], 'G')     # turned cuff
        line_on(g, lx - 5.4, HEM - 3, lx + 5.4, HEM - 3, 'K', 'G', 0.9)
        line_on(g, lx - 5.0, HEM, lx + 5.0, HEM, 'j', 'G', 0.9)
        for y in (HEM + 4, HEM + 8):                                  # eyelets
            put(g, lx - 2.8, y, 'C'); put(g, lx + 2.8, y, 'C')
        line(g, lx - 2.8, HEM + 4, lx + 2.8, HEM + 8, 'H', 1)         # crossed laces
        line(g, lx + 2.8, HEM + 4, lx - 2.8, HEM + 8, 'H', 1)
        boot_sole(g, lx)
    return fin(g)

def F_greaves():
    g = blank()
    for k in (-1, 1): boot_shell(g, k, HEM - 6)
    g = model(g)
    for k in (-1, 1):
        lx = CX + k * 5.5
        disc(g, lx, HEM - 1, 4.6, 'A')                                # knee cop
        ring(g, lx, HEM - 1, 4.6, 1.5, 'C')
        disc(g, lx, HEM - 1, 1.8, 'C'); put(g, lx - 1, HEM - 2, 'Z')
        for y in (HEM + 4, HEM + 8):                                  # shin lames
            line_on(g, lx - 4.6, y, lx + 4.6, y, 'q', 'A', 1.0)
            line_on(g, lx - 4.6, y - 1, lx + 4.6, y - 1, 'W', 'A', 0.9)
            put(g, lx - 3.4, y - 1, 'C'); put(g, lx + 3.4, y - 1, 'C')
        boot_sole(g, lx)
    return fin(g)

def F_sandals():
    g = blank()
    for k in (-1, 1):
        lx = CX + k * 5.5
        poly(g, [(lx - 4.4, GROUND - 7), (lx + 4.4, GROUND - 7),
                 (lx + 4.4, GROUND - 2), (lx - 4.4, GROUND - 2)], 'A')
    g = model(g)
    for k in (-1, 1):
        lx = CX + k * 5.5
        for (ax, bx) in ((-4.2, 4.2), (4.2, -4.2)):                   # crossed straps
            line(g, lx + ax, GROUND - 7, lx + bx, GROUND - 13, 'G', 2)
            line(g, lx + ax, GROUND - 8, lx + bx, GROUND - 14, 'K', 1)
        poly(g, [(lx - 4.6, GROUND - 14), (lx + 4.6, GROUND - 14),
                 (lx + 4.6, GROUND - 12), (lx - 4.6, GROUND - 12)], 'G')
        put(g, lx + 2, GROUND - 13, 'C')
        boot_sole(g, lx, 5.2)
    return fin(g)

def F_cuffed():
    g = blank()
    for k in (-1, 1): boot_shell(g, k, HEM - 1)
    g = model(g)
    for k in (-1, 1):
        lx = CX + k * 5.5
        ellipse(g, lx, HEM - 1, 6.2, 3.2, 'G')                        # fleece cuff
        for fx in (-4.4, -1.6, 1.6, 4.4):
            disc(g, lx + fx, HEM - 1.6, 1.7, 'H'); put(g, lx + fx - 1, HEM - 2.4, 'K')
        poly(g, [(lx - 5.0, HEM + 5), (lx + 5.0, HEM + 5),
                 (lx + 5.0, HEM + 8), (lx - 5.0, HEM + 8)], 'G')      # buckle band
        line_on(g, lx - 5.0, HEM + 5.6, lx + 5.0, HEM + 5.6, 'K', 'G', 0.9)
        poly(g, [(lx + 1.4, HEM + 4.6), (lx + 4.0, HEM + 4.6),
                 (lx + 4.0, HEM + 8.4), (lx + 1.4, HEM + 8.4)], 'C')
        put(g, lx + 2.6, HEM + 6.5, 'x')
        boot_sole(g, lx)
    return fin(g)

SHAPES = [body(0), body(1), body(2), hat()]
SHAPES += [f() for f in (H_hood, H_horned, H_great, H_crown, H_brim, H_barbute, H_cap)]
SHAPES += [f() for f in (B_cuirass, B_scale, B_robe, B_banded, B_carapace)]
SHAPES += [F_trail(), F_greaves(), F_sandals(), F_cuffed()]
SHAPES += [stick(), hands(), H_crown_grand(), gripArm()]
P.setsize(96)
