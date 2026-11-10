# -*- coding: utf-8 -*-
"""Five things you meet on the trail and can walk straight past.

   These are not bosses and must not read like them. A boss fills the
   frame and looks at you; an encounter is life-sized, side on, usually
   busy with something that is not you. Light from the upper left, same
   ramp, same outline pass.
"""
from pixlib import *
import math


def eye(g, x, y, r=1.9, iris='q'):
    """An animal's eye at this scale is a dark bead with one lit pixel.
       The first pass ringed it in outline and filled it bright, and a
       black bear came out looking like a lemur."""
    disc(g, x, y, r, 'n')
    disc(g, x - r*0.26, y - r*0.30, max(0.6, r*0.34), 'B')

def leg(g, x, top, bot, w=4.0, k=0, body='A'):
    taper(g, x, top, x + k, bot, w, w*0.72, body)
    taper(g, x + k, bot - 1, x + k - 1, bot + 3, w*0.8, w*0.9, 'q')

def fur(g, pts, r=2.0, ch='B'):
    for (x, y) in pts: disc(g, x, y, r, ch)

def grass(g, y0, n=16, h=6, ch='C'):
    for i in range(n):
        x = 1 + i * (62.0 / n) + (i % 3)
        hh = h * (0.5 + (i % 4) * 0.22)
        line(g, x, y0, x + (2.5 if i % 2 else -2.5), y0 - hh, ch, 1)


# ============================================================== 0  BEAR
def e_bear():
    """A black bear on the trail, side on, head turned to look at you.
       Shoulders high, rump low, the opposite of a dog."""
    g = blank()
    ellipse(g, 34, 36, 21, 13, 'A')                    # barrel body
    ellipse(g, 20, 31, 11, 10, 'A')                    # shoulder hump, high
    ellipse(g, 48, 36, 12, 10, 'A')                    # rump, lower
    leg(g, 17, 38, 56, 6.5, 1); leg(g, 26, 40, 57, 5.5, -1)
    leg(g, 45, 40, 56, 6.0, 1); leg(g, 53, 39, 56, 5.5, 0)
    for x in (16, 26, 45, 53):                          # paws and claws
        ellipse(g, x, 57, 5.0, 2.6, 'A')
        for k in range(3): disc(g, x - 3 + k*3, 59, 1.0, 'C')
    # Head low and forward, three quarters on. A bear's head is mostly
    # muzzle; the first pass made it a ball with two big eyes on it.
    ellipse(g, 14, 24, 11, 9.5, 'A')                        # heavy skull
    poly(g, [(1, 23), (14, 19), (16, 31), (3, 33)], 'A')    # thick muzzle
    poly(g, [(2, 24), (13, 20.5), (14, 25), (3, 28)], 'm')  # tan bridge
    ellipse(g, 2.6, 28.5, 3.2, 2.6, 'n')                    # nose pad
    disc(g, 1.8, 27.4, 1.0, 'q')
    # ears round, low and set BACK on the skull. Up on top they read as
    # horns and the whole animal turns into a goat.
    for (x, y) in [(13, 15.5), (21, 16.5)]:
        disc(g, x, y, 3.6, 'A'); disc(g, x, y, 1.9, 'n')
    eye(g, 9.5, 23, 1.2); eye(g, 16.5, 23.4, 1.1)
    line_on(g, 3, 31, 11, 29.5, 'q', 'A')                   # mouth line
    # the light catching the top of it
    fur(g, [(20, 24), (27, 25), (35, 25), (43, 27), (50, 29)], 2.4)
    for i in range(11):                                      # a shaggy back
        x = 16 + i * 3.6
        line(g, x, 25 + i*0.5, x + 2, 21 + i*0.7, 'B', 1)
    fur(g, [(24, 46), (34, 48), (44, 47)], 2.2, 'd')
    grass(g, 60, 18, 7, 'G')
    return dump(paint(g, 0.16))


# ============================================================== 1  DOE
def e_doe():
    """A whitetail doe, head up, already looking at you. Thin legs, deep
       chest, the tail up and white because she is about to go."""
    g = blank()
    ellipse(g, 32, 32, 17, 10, 'A')                    # body
    ellipse(g, 22, 31, 10, 9, 'A')                     # chest
    for (x, k, w) in [(20, -1, 3.2), (26, 1, 3.0), (41, -1, 3.0), (46, 1, 2.8)]:
        taper(g, x, 38, x + k * 2, 58, w, w * 0.55, 'A')
        taper(g, x + k*2, 54, x + k*2.5, 59, w*0.6, w*0.8, 'q')
        disc(g, x + k*2.5, 59.5, 1.6, 'q')
    # neck up and head high
    taper(g, 20, 30, 13, 14, 8, 5.5, 'A')
    ellipse(g, 11, 11, 7, 5, 'A')
    poly(g, [(3, 10), (12, 8), (13, 14), (4, 15)], 'A')     # muzzle
    disc(g, 3.6, 12.6, 2.0, 'q')
    for (x, y, k) in [(9, 5, -1), (15, 6, 1)]:              # big ears, out
        poly(g, [(x, y + 3), (x + k*7, y - 5), (x + k*8, y + 2), (x + k*2, y + 5)], 'A')
        poly(g, [(x + k*1.5, y + 2.5), (x + k*6, y - 3), (x + k*6.5, y + 1)], 'q')
    eye(g, 10, 10, 1.4)
    # the tail, up and white, which is the whole picture
    poly(g, [(47, 26), (52, 16), (56, 19), (52, 30)], 'V')
    poly(g, [(48, 26), (52, 18), (54, 20)], 'W')
    # white throat and belly, the only light on her
    poly(g, [(14, 15), (19, 16), (18, 22), (13, 20)], 'V')
    poly(g, [(23, 38), (42, 39), (40, 42), (24, 41)], 'V')
    for (x, y) in [(26, 25), (34, 25), (41, 27)]: disc(g, x, y, 2.2, 'B')
    grass(g, 61, 20, 8, 'G')
    return dump(paint(g, 0.12))


# ============================================================ 2  SOBO
def e_sobo():
    """A southbounder coming the other way: pack over the head, poles,
       beard, and the shuffle of someone two thousand miles in."""
    g = blank()
    # the pack first, it is most of the silhouette
    poly(g, [(22, 12), (44, 10), (47, 40), (20, 42)], 'C')
    for i in range(4):
        line(g, 21, 17 + i*6.5, 46, 15 + i*6.5, 'c', 2)     # compression straps
    poly(g, [(26, 4), (42, 3), (44, 12), (24, 13)], 'C')    # lid, overstuffed
    poly(g, [(44, 16), (54, 20), (52, 32), (45, 30)], 'c')  # side pocket
    disc(g, 50, 24, 3.4, 'Y')                               # a bottle in it
    poly(g, [(18, 14), (23, 13), (24, 34), (19, 35)], 'c')  # sleeping pad
    # body, small under it
    poly(g, [(28, 38), (42, 37), (41, 52), (29, 53)], 'A')
    taper(g, 31, 52, 29, 62, 5.5, 4.5, 'A')
    taper(g, 39, 52, 41, 62, 5.5, 4.5, 'A')
    for x in (28, 42): ellipse(g, x, 62, 5.0, 2.4, 'G')     # boots
    # arms out to the poles
    taper(g, 29, 41, 20, 50, 4.0, 3.2, 'A')
    taper(g, 41, 41, 50, 49, 4.0, 3.2, 'A')
    line(g, 19, 44, 16, 63, 'G', 2); line(g, 51, 43, 55, 63, 'G', 2)
    disc(g, 19, 44, 2.2, 'q'); disc(g, 51, 43, 2.2, 'q')
    # head, beard, sun hat
    ellipse(g, 35, 31, 6, 5.5, 'm')
    poly(g, [(30, 33), (40, 33), (38, 41), (32, 41)], 'G')  # beard
    ellipse(g, 35, 26, 11, 3.2, 'G')                        # brim
    ellipse(g, 35, 23, 6, 3.4, 'G')
    disc(g, 32, 30, 1.2, 'q'); disc(g, 38, 30, 1.2, 'q')
    grass(g, 62, 14, 5, 'G')
    return dump(paint(g, 0.24))


# =========================================================== 3  MAGIC
def e_magic():
    """Trail magic at a road crossing: a cooler, a sharpie sign, and
       whatever is left in it by the time you get there."""
    g = blank()
    # the cooler, three quarter on
    poly(g, [(12, 30), (48, 27), (52, 33), (52, 54), (12, 57)], 'A')
    poly(g, [(12, 30), (48, 27), (52, 33), (16, 36)], 'B')      # lit top face
    poly(g, [(10, 26), (50, 23), (54, 30), (14, 33)], 'C')      # open lid
    poly(g, [(10, 26), (50, 23), (52, 26), (12, 29)], 'Y')
    rect(g, 20, 42, 44, 45, 'd')                                 # moulded line
    poly(g, [(16, 38), (24, 37), (24, 41), (16, 42)], 'C')       # latch
    # cans in it
    for (x, y) in [(20, 31), (27, 30), (34, 29), (41, 28)]:
        ellipse(g, x, y, 3.0, 1.6, 'Z'); rect(g, x-3, y, x+3, y+3, 'C')
    # the sign, on a stake, leaning
    line(g, 56, 36, 59, 62, 'G', 3)
    poly(g, [(44, 8), (63, 5), (63, 22), (45, 25)], 'V')
    for i in range(4):                                           # sharpie
        line(g, 47, 11 + i*4, 60 - (i % 2) * 5, 10 + i*4, 'q', 1)
    # a camp chair, folded against it
    line(g, 4, 30, 9, 58, 'C', 3); line(g, 10, 31, 5, 58, 'C', 3)
    poly(g, [(2, 28), (12, 26), (12, 31), (3, 33)], 'c')
    grass(g, 62, 16, 6, 'G')
    return dump(paint(g, 0.26))


# ========================================================== 4  RATTLER
def e_rattler():
    """A timber rattlesnake across a warm rock. Coiled, head up off the
       coil, and the rattle lifted. The reason you look where you step."""
    g = blank()
    # the rock it is on, filling the lower frame
    poly(g, [(2, 44), (20, 34), (46, 33), (62, 45), (62, 63), (2, 63)], 'G')
    poly(g, [(4, 45), (21, 36), (44, 35), (56, 44), (30, 48)], 'H')
    for (x0, y0, x1, y1) in [(12, 52, 34, 50), (36, 56, 58, 52), (8, 59, 28, 58)]:
        line(g, x0, y0, x1, y1, 'g', 1)
    # the coil: three loops, drawn large to small
    for (cx, cy, r, t) in [(30, 44, 17, 7), (31, 43, 11, 6), (32, 42, 6, 5)]:
        ring(g, cx, cy, r, t, 'A')
    # the banding, dark chevrons across the loops
    for i in range(14):
        a = i * 0.45
        for (r, w) in [(17, 7), (11, 6)]:
            x = 30 + math.cos(a) * r; y = 44 + math.sin(a) * r * 0.86
            ellipse(g, x, y, w*0.34, w*0.46, 'q')
    # the head, up off the coil and turned at you
    taper(g, 33, 38, 22, 22, 6.5, 6.0, 'A')
    ellipse(g, 19, 18, 8, 6, 'A')
    poly(g, [(11, 17), (20, 15), (21, 21), (12, 22)], 'A')      # blunt snout
    poly(g, [(12, 14), (22, 12), (23, 17), (13, 18)], 'q')      # dark crown
    eye(g, 15, 18, 1.7, 'C')
    line(g, 11, 20, 4, 23, 'C', 1); line(g, 4, 23, 7, 21, 'C', 1)   # tongue
    line(g, 4, 23, 7, 25, 'C', 1)
    # the rattle, lifted clear
    for i in range(5):
        ellipse(g, 50 + i*2.6, 30 - i*3.4, 3.4 - i*0.4, 2.6 - i*0.3, 'V')
    taper(g, 44, 36, 50, 31, 5.0, 3.6, 'A')
    return dump(paint(g, 0.14))


SHAPES = [e_bear(), e_doe(), e_sobo(), e_magic(), e_rattler()]
