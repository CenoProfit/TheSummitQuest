# -*- coding: utf-8 -*-
"""Full colour gear, built with forge.py. One builder per piece.

Laid out the way the letter staffs are, so it sits in the hand the same
way: upright, head at the top of the frame, shaft to the bottom. GRIP
is the band of rows the hand closes on, which the page uses where it
would otherwise look for wood coloured pixels.
"""
import math
from forge import *


def staff_first_light(f=0):
    """The one legendary staff. A crook of black wood split by age, gold
       bound, holding a captive sun; prayer strips hang from the crown."""
    C = Canvas()
    wood = Mat('#3a2a2e', 8, tex=lambda c: tex_bark(c, 1.2, 3))
    gold = Mat('#d8a630', 8, spec=0.9, gloss=0.8, tex=lambda c: tex_metal(c, 0.6, 5))
    sun = Mat('#ffd060', 6, emit=True, glow=3,
              tones=[(200, 90, 20), (240, 140, 30), (255, 190, 60), (255, 222, 120), (255, 244, 200), (255, 255, 245)])
    cloth = Mat('#9a2a2a', 7, tex=lambda c: (np.sin(c.Y * 1.2) > 0.7) * -1.0)
    paper = Mat('#e6dcc0', 6)
    cx = 48
    # shaft, a little gnarled
    C.limb([(cx + 1, 93, 2.6), (cx - 1, 78, 3.0), (cx + 1, 60, 3.2), (cx - 1, 44, 3.4), (cx, 36, 3.8)], wood)
    # gold bands and the grip wrap
    for y in (40, 77, 90):
        C.ell(cx, y, 4.6, 1.8, 4, gold, z=4)
    for i in range(7):
        y = 57 + i * 2.6
        C.limb([(cx - 3.4, y, 1.1, 5), (cx + 3.4, y + 1.6, 1.1, 5)], Mat('#5a3a26', 6))
    # the crook: two arms of wood that curl round the sun
    C.limb([(cx, 36, 3.6), (cx - 7, 30, 3.2), (cx - 12, 20, 2.8), (cx - 10, 10, 2.4), (cx - 4, 5, 2.0), (cx + 2, 6, 1.6)], wood, z=2)
    C.limb([(cx, 36, 3.4), (cx + 8, 31, 3.0), (cx + 13, 22, 2.6), (cx + 12, 13, 2.0), (cx + 8, 9, 1.5)], wood, z=-2)
    # gold filigree over the wood
    C.limb([(cx - 7, 31, 1.0, 8), (cx - 12, 22, 1.0, 8), (cx - 10.5, 12, 0.9, 8)], gold)
    C.limb([(cx + 8, 32, 1.0, 6), (cx + 12.5, 23, 1.0, 6)], gold)
    C.ball(cx - 4, 5, 2.2, gold, z=10)
    # the sun, held in the middle
    C.ball(cx + 0.5, 20, 7.2, sun, z=4)
    for a in range(8):
        ang = a * math.pi / 4 + 0.3
        r0, r1 = 8.5, 11.5 if a % 2 == 0 else 10
        C.limb([(cx + 0.5 + math.cos(ang) * r0, 20 + math.sin(ang) * r0, 0.9, 1),
                (cx + 0.5 + math.cos(ang) * r1, 20 + math.sin(ang) * r1, 0.5, 1)], sun)
    C.dot(cx - 2, 17, (255, 255, 255)); C.dot(cx - 1, 17, (255, 255, 250))
    # prayer strips off the crown
    C.plate([(cx - 13, 24), (cx - 10, 24), (cx - 11, 42), (cx - 15, 41)], cloth, z=12, bevel=1.2)
    C.plate([(cx - 15, 41), (cx - 11, 42), (cx - 12, 46), (cx - 16, 45)], paper, z=13, bevel=1)
    C.plate([(cx + 12, 26), (cx + 14.5, 27), (cx + 15, 38), (cx + 12, 37)], cloth, z=10, bevel=1.2)
    return C


# [name, builder, frames, grip rows (or None)]
BUILD = [
    ('Staff of the First Light', staff_first_light, 1, (56, 73)),
]
