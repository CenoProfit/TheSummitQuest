# -*- coding: utf-8 -*-
"""Big scenery: four old trees.

   The waterfalls that used to live here were sprites and are gone. A
   billboard pasted onto a mountain reads as pasted however well it is
   drawn, because the mountain is terrain: shaded by its own normal,
   occluded by its own ridges, and the right size at every distance. A
   fall is painted into the ground now, the way the tarns are.

   These used to be drawn inline in trek.html with flat fillRect calls
   and they looked it, sitting in a world where everything else goes
   through model/ao/rim/dither/outline. They are sprites now, like the
   bosses, and the renderer tints them per biome.

   RAMP USE, which differs from gear and is what the runtime tint
   expects:
     tree   body = canopy      grip = trunk and bark   accent = vines
"""
from pixlib import *
import math


# ---------------------------------------------------------------- trees
def _buttress(g, cx, base, k, L, H, ch='G'):
    """A root flare: a wedge off the trunk that meets the ground."""
    poly(g, [(cx, base - H), (cx + k * L, base), (cx + k * L * 0.52, base),
             (cx, base)], ch)
    line(g, cx, base - H * 0.86, cx + k * L * 0.86, base - 1, 'j', 1)
    line(g, cx + k * 2, base - H * 0.5, cx + k * L * 0.6, base - 1, 'H', 1)

def _bark(g, x0, x1, y0, y1, n=9):
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n
        prev = None
        for y in range(int(y0), int(y1), 2):
            xx = x + math.sin((y + i * 7) * 0.22) * 0.9
            if prev: line(g, prev[0], prev[1], xx, y, 'j' if i % 2 else 'H', 1)
            prev = (xx, y)

def _clump(g, cx, cy, r, ch):
    disc(g, cx, cy, r, ch)
    disc(g, cx - r * 0.34, cy - r * 0.30, r * 0.62, ch)
    disc(g, cx + r * 0.40, cy + r * 0.18, r * 0.54, ch)

def _vine(g, x0, y0, L, sway, n=None, leaf=True):
    """A hanging vine is a THREAD. The first pass drew these two pixels
       wide with a leaf every five rows and ran them down the trunk, so
       the tree came out wearing four yellow ladders."""
    n = n or int(L)
    px, py = x0, y0
    for i in range(1, n + 1):
        t = i / n
        x = x0 + math.sin(t * 2.6 + sway) * sway * 1.6
        y = y0 + L * t
        # 1.4 wide, not 1. A one pixel vine is a run of isolated pixels
        # and despeckle() in the paint pass eats it, which left the
        # first attempt as a column of floating specks.
        line(g, px, py, x, y, 'C', 1.4)
        if i % 4 == 1: line(g, px, py, x, y, 'c', 0.9)
        if leaf and i % 9 == 4:
            ellipse(g, x + (2.0 if i % 18 else -2.0), y, 2.0, 1.1, 'C')
        px, py = x, y
    disc(g, px, py, 1.6, 'c')

def _tree(lean, crown, vines, seed):
    g = blank()
    CX = 32 + lean
    # roots first so the trunk sits into them
    for (k, L, H) in [(-1, 15, 13), (1, 14, 12), (-1, 8, 19), (1, 9, 17),
                      (-1, 21, 7), (1, 20, 6)]:
        _buttress(g, CX + k * 2, 62, k, L, H)
    # trunk, bowed, tapering
    poly(g, [(CX - 8, 24), (CX + 8, 24), (CX + 11, 44), (CX + 12, 60),
             (CX - 12, 60), (CX - 11, 44)], 'G')
    _bark(g, CX - 10, CX + 10, 25, 60, 9)
    # limbs forking up and out
    def limb(x0, y0, x1, y1, w, d=2):
        taper(g, x0, y0, x1, y1, w, max(1.8, w * 0.44), 'G')
        if d <= 0: return
        dx, dy = x1 - x0, y1 - y0
        for k in (-1, 1):
            limb(x1, y1, x1 + dx * 0.5 + k * dy * 0.58,
                 y1 + dy * 0.5 - k * dx * 0.26, w * 0.56, d - 1)
    limb(CX - 5, 26, CX - 20, 13, 9.0)
    limb(CX + 5, 26, CX + 21, 14, 9.0)
    limb(CX, 24, CX + 2, 8, 7.5)
    # the crown: a dark mass, then lit clumps on the upper left
    for i in range(crown):
        a = i * 0.83 + seed
        rr = 7 + (i * 5) % 6
        cx = CX + math.cos(a) * (12 + (i % 7) * 2.8)
        cy = 13 + math.sin(a) * (6 + (i % 5) * 1.9)
        _clump(g, cx, cy, rr, 'd')
    for i in range(crown - 2):
        a = 0.6 + i * 0.79 + seed
        rr = 5 + (i * 3) % 5
        cx = CX + math.cos(a) * (11 + (i % 6) * 2.6)
        cy = 12 + math.sin(a) * (5 + (i % 4) * 1.8)
        _clump(g, cx, cy, rr, 'A')
    for i in range(crown // 2):
        a = 2.6 + i * 0.64 + seed
        cx = CX + math.cos(a) * (10 + (i % 5) * 2.4) - 2
        cy = 10 + math.sin(a) * (4 + (i % 3) * 1.6) - 2
        _clump(g, cx, cy, 3 + (i % 3), 'B')
    for i in range(4):
        disc(g, CX - 14 + i * 4, 5 + (i % 2) * 2, 2.6, 'W')
    # No notches. Two passes were spent trying to punch gaps in the
    # outline to stop the crown reading as one lozenge, and both of
    # them read instead as holes bored through the canopy. The clumps
    # already give the edge its shape.
    # epiphytes in the first fork, and moss up the shaded side
    for (x, y) in [(CX - 7, 27), (CX + 8, 29), (CX - 3, 23)]:
        for k in range(5):
            line(g, x, y, x - 5 + k * 2.5, y - 5 - (k % 2) * 2, 'C', 1)
    for i in range(7):
        disc(g, CX + 7 + (i % 3), 34 + i * 3.4, 2.0, 'j')
    # the vines, which are the whole reason these read as old. They hang
    # off the OUTER limbs, well clear of the trunk, or they just look
    # like something growing up the bark.
    # They hang off the limbs INSIDE the crown's footprint and stop
    # above the buttress. Started at the crown's top edge they fell
    # through open sky beside the tree and read as litter.
    for i in range(vines):
        s2 = -1 if i % 2 else 1
        # kept inside the crown's own footprint. Any further out and the
        # vine hangs through open sky beside the tree, where despeckle
        # chews it into a column of yellow specks.
        out = 7 + (i % 4) * 4
        x = CX + s2 * out
        _vine(g, x, 18 + (i % 3) * 3, 16 + (i * 11) % 16, 0.8 + (i % 3) * 0.5)
    return dump(paint(g, 0.20))


SHAPES = [_tree(0, 15, 5, 0.0), _tree(-3, 17, 6, 1.3),
          _tree(3, 13, 4, 2.6), _tree(-1, 18, 6, 4.1)]
