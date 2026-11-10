# -*- coding: utf-8 -*-
"""The eight things that bar the trail.

   Silhouette rules, taken from the hand blocked bosses in the main game
   and worth repeating here because they are what makes a boss read as a
   boss and not as a large pet:

     * shoulders span the frame, head sits LOW and SMALL
     * torso tapers hard to a narrow waist
     * arms hang past the knee and end in something heavy
     * legs are short
     * asymmetry everywhere, never mirror the two sides
     * light from the upper left

   Five stand on the ground and three are in the air. The flying ones
   break the shoulder rule on purpose: their span is wing, and the body
   is the small dense thing in the middle.
"""
from pixlib import *
import math

# ------------------------------------------------------------- helpers
def boulder(g, cx, cy, r, ch='A', facets=3):
    """A rock, not a ball. One disc knocked about by a few flat faces."""
    disc(g, cx, cy, r, ch)
    for i in range(facets):
        a = 1.1 + i * 2.3
        x = cx + math.cos(a) * r * 0.78
        y = cy + math.sin(a) * r * 0.78
        poly(g, [(x - r*0.5, y - r*0.42), (x + r*0.55, y - r*0.30),
                 (x + r*0.40, y + r*0.46), (x - r*0.44, y + r*0.34)], ch)

def glow_eye(g, x, y, r=2.4, hot='Z', cool='C'):
    disc(g, x, y, r + 1.3, 'q')
    disc(g, x, y, r, cool)
    disc(g, x, y, r * 0.52, hot)

def maw(g, cx, cy, w, h, teeth=5, lip='q', inside='n'):
    """A mouth that reads at 96 pixels: a dark hole with a hard rim and
       teeth that cross it, top and bottom, out of step with each other."""
    ellipse(g, cx, cy, w, h, lip)
    ellipse(g, cx, cy, w - 1.6, h - 1.4, inside)
    for i in range(teeth):
        t = (i + 0.5) / teeth
        x = cx - w + t * w * 2
        d = h * (0.55 + 0.38 * math.sin(t * 9.1 + cx))
        poly(g, [(x - 1.5, cy - h + 0.6), (x + 1.5, cy - h + 0.6), (x, cy - h + d)], 'W')
    for i in range(teeth - 1):
        t = (i + 1.0) / teeth
        x = cx - w + t * w * 2
        d = h * (0.50 + 0.34 * math.cos(t * 7.3 + cy))
        poly(g, [(x - 1.4, cy + h - 0.6), (x + 1.4, cy + h - 0.6), (x, cy + h - d)], 'W')

def claw_hand(g, cx, cy, r, k=1, n=4, L=7.0):
    """A fist with the fingers splayed off the low side of it."""
    boulder(g, cx, cy, r, 'A', 2)
    for i in range(n):
        a = (-0.35 + i * 0.42) * k + 1.25
        x1 = cx + math.cos(a) * (r + L); y1 = cy + math.sin(a) * (r + L)
        taper(g, cx + math.cos(a) * r * 0.6, cy + math.sin(a) * r * 0.6,
              x1, y1, 3.4, 1.3, 'C')
        disc(g, x1, y1, 1.1, 'x')

def vine(g, x0, y0, x1, y1, n=7, amp=3.2, ch='G', leaf='C'):
    px, py = x0, y0
    for i in range(1, n + 1):
        t = i / n
        x = x0 + (x1 - x0) * t + math.sin(t * 5.4 + x0 * 0.3) * amp
        y = y0 + (y1 - y0) * t
        line(g, px, py, x, y, ch, 2 if t < 0.6 else 1)
        if i % 2 == 0:
            disc(g, x + (2.2 if i % 4 else -2.2), y, 1.8, leaf)
        px, py = x, y

def crystal(g, cx, base, h, w, ch='B', tip='V'):
    poly(g, [(cx - w, base), (cx - w * 0.45, base - h), (cx + w * 0.30, base - h * 0.92),
             (cx + w, base)], ch)
    poly(g, [(cx - w * 0.45, base - h), (cx + w * 0.30, base - h * 0.92),
             (cx + w * 0.05, base - h * 0.52)], tip)

def wing_membrane(g, sx, sy, k, span, drop, ribs=4):
    """A bat/wyrm wing: one big sheet, ribs across it, scalloped trailing
       edge bitten out afterwards so the sheet does not read as a flag."""
    tip = (sx + k * span, sy - drop)
    poly(g, [(sx, sy), tip, (sx + k * span * 0.86, sy + drop * 0.95),
             (sx + k * span * 0.34, sy + drop * 1.25)], 'A')
    for i in range(ribs):
        t = (i + 1) / (ribs + 1)
        ex = sx + k * span * (0.30 + 0.64 * t)
        ey = sy + drop * (1.18 * t - 0.30 * (1 - t))
        line(g, sx, sy, ex, ey, 'd', 2)
    for i in range(ribs):
        t = (i + 0.5) / ribs
        ex = sx + k * span * (0.36 + 0.56 * t)
        ey = sy + drop * (1.12 * t - 0.16)
        disc(g, ex + k * 3.0, ey + 3.4, 3.6, '.')
    line(g, sx, sy, tip[0], tip[1], 'C', 3)

def rubble(g, pts, r=2.4, ch='A'):
    for (x, y) in pts:
        boulder(g, x, y, r, ch, 2)


# ============================================================ 0  WARDEN
def b_warden():
    """THE BLOOD MOUNTAIN WARDEN. The CCC shelter got up and walked.
       Cut granite blocks, mortar gone, moss in the seams."""
    g = blank()
    # shoulders span the frame, two stacked cairns, deliberately uneven
    boulder(g, 11, 23, 11, 'A', 4); boulder(g, 7, 33, 8, 'A', 3)
    boulder(g, 54, 21, 10, 'A', 4); boulder(g, 59, 30, 7.5, 'A', 3)
    # torso: squared blocks, wide at the chest, hard taper to the waist
    poly(g, [(17, 24), (48, 22), (45, 40), (21, 41)], 'A')
    poly(g, [(21, 40), (45, 39), (40, 50), (26, 50)], 'A')
    for y in (29, 35, 44):                       # courses of masonry
        line(g, 19, y, 46, y - 1, 'q', 1)
    for x in (27, 36):
        line(g, x, 23, x - 1, 40, 'q', 1)
    # head sits low and small, down between the shoulders
    poly(g, [(28, 13), (40, 12), (42, 23), (26, 24)], 'A')
    poly(g, [(27, 11), (41, 10), (41, 14), (27, 15)], 'C')   # lintel brow
    glow_eye(g, 31, 19, 2.3); glow_eye(g, 38, 18.4, 2.0)
    maw(g, 34, 24, 6.5, 2.6, 4)
    # arms past the knees, the left one heavier
    taper(g, 10, 34, 6, 48, 9, 8, 'A'); boulder(g, 5, 55, 9, 'A', 3)
    claw_hand(g, 5, 60, 6.5, 1, 4, 8)
    taper(g, 58, 32, 62, 45, 7.5, 6.5, 'A'); boulder(g, 62, 52, 7, 'A', 3)
    claw_hand(g, 62, 57, 5.5, -1, 3, 7)
    # short legs, planted
    poly(g, [(24, 49), (33, 49), (32, 61), (23, 61)], 'A')
    poly(g, [(36, 49), (45, 49), (46, 60), (37, 60)], 'A')
    rect(g, 20, 60, 34, 63, 'A'); rect(g, 35, 59, 49, 63, 'A')
    # moss in the seams, on the lit side. The accent ramp is the glow in
    # its chest, so the moss rides the grip ramp instead.
    for (x, y) in [(20, 30), (24, 44), (38, 33), (44, 27), (12, 28), (30, 52),
                   (44, 46), (9, 44), (57, 26), (27, 36)]:
        disc(g, x, y, 2.3, 'G'); put(g, x - 1, y - 1, 'H')
    rubble(g, [(16, 62), (52, 62), (9, 63)], 2.6)
    return dump(paint(g, 0.22))


# ======================================================== 1  LAUREL HELL
def b_laurel():
    """THE LAUREL HELL. A rhododendron thicket that closed over the trail
       and did not open again. No face, just the hollow where one goes.

       The first version drew the branches darker than the mass they sat
       on and they vanished into it. The mass is the dark thing now and
       the sticks are lit, which is what a thicket looks like."""
    g = blank()
    for (x, y, r) in [(18, 26, 14), (46, 24, 13), (32, 31, 16), (11, 38, 10),
                      (54, 37, 10), (30, 47, 13), (20, 54, 9), (44, 53, 9)]:
        disc(g, x, y, r, 'q')
    for (x, y, r) in [(24, 24, 7), (44, 22, 6), (34, 28, 7), (16, 36, 5)]:
        disc(g, x, y, r, 'd')
    # the sticks, lit, crossing the dark mass in every direction
    for i in range(34):
        a = i * 0.72
        r0 = 5 + (i % 5) * 2.6
        r1 = 20 + (i % 8) * 3.4
        x0 = 32 + math.cos(a) * r0;        y0 = 35 + math.sin(a) * r0 * 0.9
        x1 = 32 + math.cos(a * 1.06) * r1; y1 = 33 + math.sin(a * 1.06) * r1 * 0.9
        line(g, x0, y0, x1, y1, 'A' if i % 3 else 'B', 2 if i % 3 else 1)
        a2 = a * 2.0
        line(g, x1, y1, x1 + math.cos(a2) * 8, y1 + math.sin(a2) * 8,
             'A', 1)
        if i % 4 == 0:
            line(g, x1, y1, x1 - math.cos(a2) * 6, y1 + math.sin(a2) * 5, 'B', 1)
    # leaves, long and leathery, clumped at the ends on the lit side
    for i in range(34):
        a = 2.2 + i * 0.40
        x = 30 + math.cos(a) * (15 + (i % 6) * 3.2)
        y = 32 + math.sin(a) * (13 + (i % 5) * 3.0)
        if x > 38 and y > 40: continue
        ellipse(g, x, y, 3.6, 1.6, 'C')
        put(g, x - 1, y - 1, 'Z')
    # the hollow, low and small
    disc(g, 32, 34, 10, 'n')
    disc(g, 32, 34, 7.4, 'o')
    glow_eye(g, 29, 33, 2.4, 'Z', 'C'); glow_eye(g, 36, 35, 2.0, 'Z', 'C')
    for i in range(7):
        a = 0.3 + i * 0.84
        line(g, 32 + math.cos(a) * 7, 34 + math.sin(a) * 7,
             32 + math.cos(a) * 11, 34 + math.sin(a) * 11, 'A', 1)
    # runners along the ground, filling the bottom corners
    for (x0, x1) in [(5, 20), (18, 34), (30, 48), (44, 61)]:
        vine(g, x0, 57, x1, 62, 5, 2.4, 'G', 'C')
    for i in range(8):
        line(g, 7 + i * 8, 63, 12 + i * 7, 52, 'A', 2)
        line(g, 11 + i * 8, 63, 15 + i * 7, 56, 'q', 1)
    return dump(paint(g, 0.20))


# ========================================================== 2  BLY OAK
def b_oak():
    """THE BLY GAP OAK. The most photographed tree on the trail, and it
       has had enough of it.

       The first version was a rectangle under a slab and read as a crate
       wearing a hat. The trunk tapers and bows now, the boughs fork
       instead of radiating, and the crown is clumps on those forks
       rather than one lid laid across the top."""
    g = blank()
    # root flare, a wide V, drawn first so the trunk sits into it
    for (x, k, L) in [(24, -1, 20), (40, 1, 20), (28, -1, 13), (37, 1, 14)]:
        taper(g, x, 44, x - k * L, 62, 10, 4.5, 'G')
        taper(g, x - k * L * 0.7, 57, x - k * (L + 6), 63, 4.0, 2.0, 'G')
    taper(g, 32, 42, 32, 63, 13, 22, 'G')
    # trunk: bowed, tapering, bark worked down it
    poly(g, [(23, 20), (42, 19), (45, 34), (46, 48), (19, 49), (20, 33)], 'G')
    for i in range(10):
        x = 21 + i * 2.7
        line(g, x + 1.2, 19, x, 49, 'g' if i % 2 else 'j', 1)
    for i in range(5):
        line(g, 21, 24 + i * 5.5, 44, 22 + i * 5.6, 'j', 1)
    # boughs, forking. Each one splits twice on its way out.
    def bough(x0, y0, x1, y1, w, depth=2, spread=0.55):
        taper(g, x0, y0, x1, y1, w, max(1.6, w * 0.45), 'G')
        if depth <= 0: return
        dx, dy = x1 - x0, y1 - y0
        for k in (-1, 1):
            nx = x1 + dx * 0.55 + k * dy * spread
            ny = y1 + dy * 0.55 - k * dx * spread * 0.45
            bough(x1, y1, nx, ny, w * 0.58, depth - 1, spread)
    bough(26, 21, 13, 11, 7.5)
    bough(29, 19, 25, 5, 6.0)
    bough(38, 19, 52, 10, 7.5)
    bough(36, 18, 41, 4, 6.0)
    bough(32, 20, 33, 6, 5.0)
    # crown: clumps hung on the forks, not a slab
    for (cx, cy, r) in [(9, 9, 9), (18, 5, 8), (27, 3, 8), (36, 3, 8),
                        (46, 5, 8), (55, 10, 8), (14, 16, 6), (50, 17, 6),
                        (32, 10, 9), (22, 12, 6), (42, 11, 6)]:
        disc(g, cx, cy, r, 'A')
    for i in range(44):                      # leaf texture, lit from the left
        a = i * 0.68
        x = 32 + math.cos(a) * (12 + (i % 8) * 3.0)
        y = 9 + math.sin(a) * (4 + (i % 6) * 1.6)
        disc(g, x, y, 2.4, 'A')
        if x < 33 or y < 7: disc(g, x - 0.8, y - 0.8, 1.4, 'B')
    # the burl face, low on the trunk and big enough to read
    ellipse(g, 32, 35, 11, 10, 'j')
    ellipse(g, 32, 35, 8.6, 7.6, 'g')
    glow_eye(g, 28, 33, 2.8); glow_eye(g, 37, 34, 2.3)
    maw(g, 32, 43, 8, 3.4, 5, 'j')
    # hanging vines off the boughs, the thing it is known for
    vine(g, 10, 14, 7, 36, 7, 3.0)
    vine(g, 19, 9, 22, 31, 6, 2.6)
    vine(g, 31, 12, 29, 26, 5, 2.0)
    vine(g, 49, 13, 54, 35, 7, 3.0)
    vine(g, 57, 15, 60, 32, 5, 2.2)
    return dump(paint(g, 0.18))


# ======================================================= 3  HOARFROST
def b_frost():
    """THE NANTAHALA HOARFROST. Rime that kept accreting until it stood
       up. Crystal crown, a body you can nearly see through."""
    g = blank()
    # shoulders: a shelf of ice, spikes growing off the top of it
    poly(g, [(6, 30), (26, 22), (40, 21), (58, 29), (52, 38), (12, 39)], 'A')
    for (x, h, w) in [(10, 15, 4), (17, 22, 5), (25, 13, 3.5), (44, 20, 5),
                      (51, 12, 3.5), (57, 17, 4)]:
        crystal(g, x, 31, h, w)
    # torso, narrowing hard
    poly(g, [(16, 36), (48, 35), (42, 49), (23, 50)], 'A')
    poly(g, [(23, 49), (42, 48), (38, 57), (27, 57)], 'A')
    for i in range(6):                               # facets down the chest
        line(g, 20 + i * 4.4, 36, 24 + i * 3.4, 56, 'B' if i % 2 else 'd', 1)
    # head, low, small, mostly crown
    poly(g, [(26, 16), (39, 15), (41, 27), (25, 28)], 'A')
    for (x, h, w) in [(27, 11, 3), (32, 15, 3.6), (38, 10, 3)]:
        crystal(g, x, 17, h, w, 'B', 'V')
    poly(g, [(25, 18), (41, 17), (41, 22), (25, 23)], 'q')   # brow in shadow
    glow_eye(g, 29, 22, 2.2, 'V', 'd'); glow_eye(g, 37, 21.4, 1.9, 'V', 'd')
    maw(g, 33, 27, 6, 2.4, 5, 'd', 'q')
    # arms, long, ending in a splay of icicles rather than a fist
    taper(g, 11, 36, 7, 50, 8, 6, 'A')
    for i in range(4):
        crystal(g, 4 + i * 2.6, 62 - i, 13 - i * 2, 2.6, 'B', 'V')
    taper(g, 53, 35, 58, 47, 7, 5.5, 'A')
    for i in range(3):
        crystal(g, 55 + i * 2.8, 58 - i, 11 - i * 2, 2.4, 'B', 'V')
    # short legs ending in a drift
    poly(g, [(25, 56), (32, 56), (31, 62), (23, 62)], 'A')
    poly(g, [(35, 56), (42, 56), (44, 62), (36, 62)], 'A')
    ellipse(g, 32, 62, 26, 5, 'B')
    for i in range(9):                               # rime along the drift
        crystal(g, 9 + i * 6, 62, 4 + (i % 3) * 2.4, 2.0, 'B', 'V')
    return dump(paint(g, 0.10))


# ======================================================= 4  LEVIATHAN
def b_leviathan():
    """THE GORGE LEVIATHAN. What is under the water at Three Forks when
       the water is high.

       The first version drew three separate rings and a small head and
       read as hoops. One continuous S now, thickest where it leaves the
       water, with the head big and forward at the top of it."""
    g = blank()
    # two coils BEHIND, in shadow, so they read as more of the same animal
    for (cx, cy, r, t) in [(50, 16, 14, 10), (14, 22, 11, 9)]:
        ring(g, cx, cy, r, t, 'q')
        ring(g, cx - 1, cy - 1, r, t * 0.45, 'd')
    # the near body: one S curve, bottom left to top middle
    spine = [(3, 63), (10, 56), (18, 50), (27, 45), (34, 38), (38, 30)]
    for i in range(len(spine) - 1):
        w0 = 15 - i * 1.4; w1 = 14 - i * 1.4
        taper(g, spine[i][0], spine[i][1], spine[i+1][0], spine[i+1][1], w0, w1, 'A')
    # belly plates on the lower right of the curve, where the light is not
    for i in range(9):
        t = i / 8.0
        x = 9 + t * 30; y = 60 - t * 27
        ellipse(g, x + 6, y + 3, 5.5, 2.4, 'd')
    scales(g, 4, 42, 34, 62, 3.4, 1.9)
    # the dorsal sail: low triangles along the upper left edge of the
    # body, in shadow with a lit spine. Two earlier passes drew this
    # bright and large and it read first as cut paper, then as a second
    # animal lying across the first one.
    sail = [(7, 52), (14, 45), (22, 40), (30, 34), (36, 27)]
    for i in range(len(sail) - 1):
        h = 4.5 + i * 1.4
        poly(g, [sail[i], (sail[i][0] - 1, sail[i][1] - h),
                 (sail[i+1][0] - 1, sail[i+1][1] - h - 1), sail[i+1]], 'd')
        line(g, sail[i][0] - 1, sail[i][1] - h, sail[i+1][0] - 1,
             sail[i+1][1] - h - 1, 'C', 1)
    # the head, big, low and forward, jaw open to the left
    ellipse(g, 36, 22, 16, 11, 'A')
    poly(g, [(16, 18), (34, 13), (38, 25), (20, 28)], 'A')       # upper jaw
    poly(g, [(15, 25), (33, 23), (34, 33), (19, 32)], 'A')       # lower jaw
    line(g, 17, 19, 35, 15, 'B', 2)
    maw(g, 25, 26, 11, 3.8, 7)
    hornridge(g, 40, 13, 54, 6, 5)
    for (x, y, h, k) in [(40, 12, 10, 1), (46, 9, 13, 1), (52, 9, 9, 1),
                         (34, 11, 8, -1)]:
        poly(g, [(x, y + 2), (x + k * 3, y - h), (x + k * 7, y + 2)], 'C')
    glow_eye(g, 29, 18, 3.0); glow_eye(g, 38, 20, 2.3)
    # gill frills and barbels
    for i in range(3):
        poly(g, [(42, 24 + i * 4), (52, 21 + i * 5), (43, 29 + i * 4)], 'C')
    vine(g, 19, 30, 9, 42, 5, 2.6, 'C', 'Y')
    vine(g, 24, 33, 23, 46, 5, 2.2, 'C', 'Y')
    # the water it is coming out of
    for i in range(11):
        ellipse(g, 2 + i * 6.2, 60 + (i % 3) * 2, 7 - (i % 3), 2.2, 'B')
        ellipse(g, 5 + i * 6.2, 63 - (i % 2), 5, 1.6, 'V')
    return dump(paint(g, 0.14))


# =========================================================== 5  STORM
def b_storm():
    """THE STORM OVER TRAY. Sky. A thunderhead with something looking out
       of it. The body is cloud, so the silhouette is mass, not limbs.

       The first version was one flat value with squiggles under it. The
       anvil is banded now, bright on top and heavy underneath, and the
       bolts start inside the cloud instead of floating below it."""
    g = blank()
    # the anvil, built bottom up so the lit tops stay on top
    for (x, y, rx, ry) in [(32, 36, 23, 13), (14, 31, 15, 11), (50, 32, 15, 11),
                           (24, 24, 17, 12), (45, 25, 16, 12), (34, 15, 21, 12),
                           (16, 17, 13, 10), (52, 18, 12, 9)]:
        ellipse(g, x, y, rx, ry, 'd')
    for (x, y, rx, ry) in [(26, 20, 14, 9), (46, 21, 13, 8), (34, 12, 18, 9),
                           (15, 15, 10, 7), (53, 16, 9, 6)]:
        ellipse(g, x, y, rx, ry, 'A')
    for (x, y, rx, ry) in [(28, 14, 11, 6), (46, 16, 9, 5), (33, 7, 14, 6),
                           (15, 11, 8, 4)]:
        ellipse(g, x, y, rx, ry, 'B')
    for (x, y, rx, ry) in [(30, 7, 8, 3.4), (47, 12, 6, 2.8), (16, 8, 6, 2.6)]:
        ellipse(g, x, y, rx, ry, 'W')
    # the squall, ragged curtains hanging off the base
    for i in range(13):
        x = 2 + i * 5.0
        h = 10 + (i * 11 % 16)
        poly(g, [(x - 3, 42), (x + 3, 42), (x + 1, 42 + h), (x - 2, 42 + h * 0.65)],
             'q' if i % 2 else 'n')
    # the face: brow first so the eyes sit under something
    ellipse(g, 33, 30, 14, 10, 'q')
    poly(g, [(20, 24), (46, 22), (47, 29), (19, 30)], 'n')
    glow_eye(g, 27, 30, 3.4, 'Z', 'C'); glow_eye(g, 39, 31, 2.8, 'Z', 'C')
    maw(g, 33, 38, 9, 3.4, 6, 'n')
    # lightning. Three strikes, thin, hanging off the base of the cloud
    # rather than drawn across it: the first pass put four fat ones over
    # the face and the whole thing read as a white lattice.
    def bolt(x0, y0, x1, y1, n):
        px, py = x0, y0
        for i in range(1, n + 1):
            t = i / n
            x = x0 + (x1 - x0) * t + (5.0 if i % 2 else -4.0) * (1 - t * 0.4)
            y = y0 + (y1 - y0) * t
            line(g, px, py, x, y, 'C', 2)
            line(g, px, py, x, y, 'Z', 1)
            px, py = x, y
    bolt(22, 44, 15, 62, 4)
    bolt(48, 42, 55, 60, 4)
    bolt(35, 48, 38, 63, 3)
    for (x, y) in [(20, 54), (44, 56), (52, 50), (30, 58)]:
        disc(g, x, y, 1.4, 'Y')
    return dump(paint(g, 0.0))


# ============================================================ 6  WYRM
def b_wyrm():
    """THE RIDGE WYRM. Sky. Wings take the whole frame; the body is the
       small dense thing they hang from."""
    g = blank()
    wing_membrane(g, 26, 26, -1, 25, 20, 4)
    wing_membrane(g, 38, 24, 1, 26, 22, 4)
    # body, short and heavy, head low and forward
    ellipse(g, 32, 34, 9, 13, 'A')
    scales(g, 25, 39, 24, 46, 3.4, 1.9)
    poly(g, [(28, 20), (38, 19), (40, 30), (26, 31)], 'A')     # neck
    ellipse(g, 33, 17, 10, 7, 'A')                              # skull
    poly(g, [(24, 15), (33, 13), (34, 21), (25, 22)], 'A')     # snout
    maw(g, 27, 19, 7, 2.6, 5)
    for (x, y, k) in [(38, 11, 1), (43, 13, 1), (28, 10, -1)]:
        poly(g, [(x, y + 4), (x + k * 4, y - 7), (x + k * 7, y + 3)], 'C')
    glow_eye(g, 31, 15, 2.4); glow_eye(g, 37, 16, 1.9)
    # tail, long, down and to the left, ending in a blade
    pts = [(32, 46), (28, 54), (18, 59), (8, 60)]
    for i in range(len(pts) - 1):
        taper(g, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1],
              8 - i * 2, 6 - i * 2, 'A')
    poly(g, [(9, 57), (1, 61), (9, 63)], 'C')
    # legs tucked, claws out
    claw_hand(g, 25, 50, 4.5, -1, 3, 6)
    claw_hand(g, 40, 48, 4.0, 1, 3, 6)
    return dump(paint(g, 0.16))


# ========================================================== 7  CARRION
def b_carrion():
    """THE CARRION CROWN. Sky. A vulture that has been on this ridge long
       enough to be owed something, wearing what it took."""
    g = blank()
    # wings, spread and fingered, filling both sides
    for k in (-1, 1):
        sx = 32 + k * 7
        poly(g, [(sx, 24), (32 + k * 33, 12), (32 + k * 33, 26),
                 (32 + k * 12, 36)], 'A')
        for i in range(6):                       # separated primaries
            t = 0.12 + i * 0.16
            x0 = 32 + k * (12 + 21 * t); y0 = 26 + t * 5
            poly(g, [(x0, y0), (x0 + k * 10, y0 + 13), (x0 + k * 5, y0 + 16),
                     (x0 - k * 2, y0 + 7)], 'A')
        featherrows(g, 32 + k * 12, 24, 32 + k * 30, 17, 3, 6)
    # body, hunched, head LOW and small, neck bare
    ellipse(g, 32, 38, 12, 15, 'A')
    for r in range(5):                           # ruff of feathers
        for i in range(5):
            disc(g, 24 + i * 4 + (2 if r % 2 else 0), 28 + r * 3, 2.2, 'A')
            put(g, 23 + i * 4 + (2 if r % 2 else 0), 27 + r * 3, 'B')
    taper(g, 31, 29, 33, 18, 7, 5, 'u')          # bare neck, wrinkled
    for i in range(4):
        line(g, 28 + i * 0.6, 26 - i * 2, 36 - i * 0.4, 25 - i * 2, 'q', 1)
    ellipse(g, 33, 14, 6.5, 5.5, 'u')            # small skull
    poly(g, [(36, 11), (47, 15), (46, 19), (38, 18)], 'C')     # bill, hooked
    poly(g, [(44, 17), (48, 16), (45, 22)], 'c')               # the hook itself
    poly(g, [(37, 12), (45, 15), (42, 17)], 'Y')               # lit top
    disc(g, 31, 13, 2.4, 'q'); disc(g, 31, 13, 1.5, 'Z')       # eye
    # the crown it took, sitting crooked and too big for it
    poly(g, [(25, 10), (42, 7), (41, 2), (37, 6), (33, 0), (29, 6), (26, 3)], 'C')
    rect(g, 25, 9, 42, 11, 'c')
    for x in (28, 33, 39):
        disc(g, x, 6, 1.4, 'Z')
    # legs and talons hanging, and the bones it is carrying
    for (x, k) in [(27, -1), (38, 1)]:
        taper(g, x, 50, x + k * 2, 58, 4.5, 3.4, 'C')
        for i in range(3):
            taper(g, x + k * 2, 58, x + k * (2 + (i - 1) * 5), 63,
                  2.8, 1.2, 'C')
    for (x0, y0, x1, y1) in [(12, 52, 22, 58), (44, 55, 55, 50)]:
        taper(g, x0, y0, x1, y1, 2.6, 2.6, 'M')
        disc(g, x0, y0, 2.6, 'M'); disc(g, x1, y1, 2.4, 'M')
    return dump(paint(g, 0.18))


SHAPES = [b_warden(), b_laurel(), b_oak(), b_frost(),
          b_leviathan(), b_storm(), b_wyrm(), b_carrion()]
