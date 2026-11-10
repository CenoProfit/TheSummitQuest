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
     24      his left arm, closed on the shield
     25,26   his bare arms, right then left, hanging
     27,28   the same arms in a chest piece's material
     29,30   and in the robe's longer sleeve

   Proportions: he stands 58 of the 64 rows and is 30 wide at the
   shoulder. The first attempt made him as wide as he was tall and he
   read as a barrel with a bucket on it.
"""
import pixlib as P
from pixlib import *

P.setsize(64)
CX = 32
# The head sits one row higher than it used to: with the shoulder line
# raised, a helm whose neckguard reached HEAD_Y+13 ended up buried in
# the pauldrons and head and torso read as one mass.
HEAD_Y = 13; HEAD_R = 9.6
# The torso used to be 22 rows tall and 32 wide: wider than it was
# high, which no amount of detail on it could rescue. Raising the
# shoulder and dropping the hem buys the room the layers need.
SH_Y   = 24                 # shoulder line
WAIST  = 41
HEM    = 49
GROUND = 62

def legs(step):
    g = blank()
    lift = ((0, 0), (0, 2), (2, 0))[step]
    for i, k in enumerate((-1, 1)):
        lx = CX + k * 5.5
        taper(g, lx, HEM - 1, lx, GROUND - lift[i], 8, 7, 'G')
    return g

def arm(k, ch='A', to=None, w0=6.6, w1=5.8, cuff=None):
    """ONE hanging arm, as its own layer. It used to be part of the
       body, which meant that the moment he picked something up the body
       went on hanging that arm straight down while the gripping arm
       reached out over the top of it, and he had two right arms. Drawn
       per side now, and the side that is holding something is simply
       not drawn."""
    g = blank()
    to = WAIST if to is None else to
    taper(g, CX + k * 9.4, SH_Y + 0.5, CX + k * 12.2, to, w0, w1, ch)
    g = model(g)
    if cuff:
        poly(g, [(CX + k * 12.2 - w1 * 0.55, to - 2.2), (CX + k * 12.2 + w1 * 0.55, to - 2.2),
                 (CX + k * 12.2 + w1 * 0.50, to), (CX + k * 12.2 - w1 * 0.50, to)], cuff)
    disc(g, CX + k * 12.2, to + 2, 3.3, 'm')
    return fin(g)

def shell(g, ch='A', sh=10, wa=8, hm=11):
    """The torso silhouette every chest layer shares. The sides bow in
       at the waist rather than running straight from shoulder to hem:
       a trapezoid that only widens on the way down reads as a slab
       hung off his neck, which is exactly what the armour looked like."""
    pts = []
    rows = [(SH_Y, sh), (SH_Y + 4, sh * 0.99), (WAIST - 4, wa * 1.06),
            (WAIST, wa), (WAIST + 3, wa * 1.09), (HEM, hm)]
    for (y, w) in rows:  pts.append((CX + w, y))
    for (y, w) in reversed(rows): pts.append((CX - w, y))
    poly(g, pts, ch)

# --------------------------------------------------------- body helpers
# These three are what give a worn piece layers. Before them every chest
# was one filled silhouette with a texture stamped across it, which is
# why they all read as the same slab in different colours.
def plackart(g, top=None, w=10.0, drop=9.0, ch='B', trim='C'):
    """The upper chest plate, a separate piece lapped over the torso
       with its own lit top edge and a shadow where the one below tucks
       under it."""
    t = SH_Y + 1 if top is None else top
    edgelight(g, CX - w, t + 0.6, CX + w, t + 0.6, 1.1, 2)
    cut(g, CX - w * 0.93, t + drop * 0.74, CX, t + drop + 0.2, 1.2)
    cut(g, CX + w * 0.93, t + drop * 0.74, CX, t + drop + 0.2, 1.2)
    if trim:
        for k in (-1, 1): stud(g, CX + k * (w - 1.6), t + 2.0, 1.2, trim)

def belt(g, y=None, h=3.2, w=9.6, ch='G', buckle='C'):
    """A waist. Without one the torso and the skirt are one mass and he
       has no middle."""
    y = WAIST if y is None else y
    poly(g, [(CX - w, y), (CX + w, y), (CX + w, y + h), (CX - w, y + h)], ch)
    line_on(g, CX - w, y + 0.6, CX + w, y + 0.6, 'H', ch, 0.9)
    line_on(g, CX - w, y + h - 0.6, CX + w, y + h - 0.6, 'j', ch, 0.9)
    if buckle:
        rect(g, CX - 2.6, y + 0.3, CX + 2.6, y + h - 0.3, buckle)
        rect(g, CX - 1.1, y + 1.0, CX + 1.1, y + h - 1.0, 'c')

def shoulder(g, k, w=6.2, h=11.5, plates=3, ch='A', trim='C'):
    """A shoulder cap that comes DOWN over the arm. pixlib's pauldron
       lays its plates out almost horizontally, which on a figure seen
       from behind turns into a shelf either side of his neck and makes
       the whole silhouette a letter T."""
    ox = CX + k * 8.6
    for i in range(plates):
        f = 1.0 - i * 0.17
        y0 = SH_Y - 3.0 + i * 2.1
        poly(g, [(ox - k * 4.5, y0),
                 (ox + k * w * f, y0 + h * 0.30),
                 (ox + k * w * f * 0.86, y0 + h * f),
                 (ox - k * 4.5, y0 + h * f * 0.78)], ch)
        line_on(g, ox - k * 4.5, y0 + 0.7, ox + k * w * f, y0 + h * 0.30 + 0.7, 'W', ch, 0.9)
        line_on(g, ox - k * 4.5, y0 + h * f * 0.78, ox + k * w * f * 0.86, y0 + h * f, 'q', ch, 1.2)
    if trim:
        poly(g, [(ox - k * 4.5, SH_Y - 3.0), (ox + k * w, SH_Y - 3.0 + h * 0.30),
                 (ox + k * w, SH_Y - 1.2 + h * 0.30), (ox - k * 4.5, SH_Y - 1.2)], trim)
        stud(g, ox + k * (w - 2.0), SH_Y - 1.4 + h * 0.30, 1.2, trim)

def sleeve(k, ch='A', to=None, w0=7.0, w1=5.8, cuff='C'):
    """ONE arm clothed in the chest piece's own material, as its own
       layer. The body hangs bare arms either side of the torso, and a
       steel cuirass worn over them left two skin coloured lumps at the
       shoulders belonging to no piece of armour at all. Per side,
       because the side that is holding something is not drawn."""
    g = blank()
    to = WAIST - 0.5 if to is None else to
    if True:
        taper(g, CX + k * 9.4, SH_Y + 0.5, CX + k * 12.2, to, w0, w1, ch)
        g = model(g)
        line_on(g, CX + k * 9.4 - 2.2, SH_Y + 1.5, CX + k * 12.2 - 2.2, to - 1, 'W', ch, 0.9)
        line_on(g, CX + k * 9.4 + 2.4, SH_Y + 1.5, CX + k * 12.2 + 2.4, to - 1, 'q', ch, 0.9)
        if cuff:
            poly(g, [(CX + k * 12.2 - w1 * 0.55, to - 2.2), (CX + k * 12.2 + w1 * 0.55, to - 2.2),
                     (CX + k * 12.2 + w1 * 0.50, to), (CX + k * 12.2 - w1 * 0.50, to)], cuff)
    disc(g, CX + k * 12.2, to + 2.4, 3.3, 'm')
    return fin(g)

def seam(g, sh=10.4, wa=8.2, hm=11.4, ch='q'):
    """A dark line down the torso edge. Pauldrons, sleeves and swept
       plates are drawn in the same body tone as the shell, so without
       this they melt into one mass and the whole piece reads as a slab
       the width of his shoulders. Call it before model(), which only
       rewrites mid tones and so leaves the line alone."""
    for k in (-1, 1):
        line_on(g, CX + k * sh, SH_Y - 1, CX + k * wa, WAIST, ch, 'A', 1.3)
        line_on(g, CX + k * wa, WAIST, CX + k * hm, HEM, ch, 'A', 1.3)
    line_on(g, CX - sh, SH_Y - 0.4, CX + sh, SH_Y - 0.4, ch, 'A', 1.1)

def fauld(g, n=3, top=None, w=10.6, ch='A', trim='C'):
    """The skirt, narrower than the torso and cut into tassets, so the
       bottom edge is a shape instead of a straight line."""
    t = (WAIST + 3.4) if top is None else top
    span = HEM - t
    for i in range(n):
        y0 = t + span * i / float(n)
        y1 = t + span * (i + 1) / float(n) + 0.9
        f = 1.0 + 0.10 * i
        poly(g, [(CX - w * f, y0), (CX + w * f, y0),
                 (CX + w * f * 0.95, y1), (CX - w * f * 0.95, y1)], ch)
        edgelight(g, CX - w * f, y0 + 0.6, CX + w * f, y0 + 0.6, 1.0, 2)
        shift_line(g, CX - w * f * 0.95, y1 - 0.5, CX + w * f * 0.95, y1 - 0.5, -2, 1.1)
    # cut a notch out of the bottom edge either side of centre, so the
    # skirt ends in tassets rather than a ruler line
    for k in (-1, 1):
        poly(g, [(CX + k * 2.2, HEM - 2.2), (CX + k * 4.4, HEM - 2.2),
                 (CX + k * 4.4, HEM + 2), (CX + k * 2.2, HEM + 2)], '.')
    if trim:
        line_on(g, CX - w * 1.18, HEM - 1.3, CX + w * 1.18, HEM - 1.3, trim, ch, 1.2)

def body(step):
    g = legs(step)
    shell(g)
    # Neck: about half the width of the skull, and mostly hidden under
    # the jaw. Six pixels was a stalk; twelve was a tree trunk.
    poly(g, [(CX - 4.6, HEAD_Y + 4), (CX + 4.6, HEAD_Y + 4),
             (CX + 5.0, SH_Y + 1), (CX - 5.0, SH_Y + 1)], 'm')
    # Skull, then a squared jaw under it. A plain disc narrows to a point
    # where it meets the neck, which is what made the head look pinched.
    ellipse(g, CX, HEAD_Y - 1, HEAD_R, HEAD_R * 0.80, 'm')
    poly(g, [(CX - HEAD_R * 0.94, HEAD_Y - 3), (CX + HEAD_R * 0.94, HEAD_Y - 3),
             (CX + HEAD_R * 0.80, HEAD_Y + 6), (CX + HEAD_R * 0.62, HEAD_Y + 9),
             (CX - HEAD_R * 0.62, HEAD_Y + 9), (CX - HEAD_R * 0.80, HEAD_Y + 6)], 'm')
    # Hair. He is seen from behind, so the back of his head is most of
    # what you ever see of him, and bare it read as a bald egg: a crown
    # worn over it looked as though it were floating on a neck.
    ellipse(g, CX, HEAD_Y - 1.6, HEAD_R * 0.98, HEAD_R * 0.80, 'G')
    poly(g, [(CX - HEAD_R * 0.92, HEAD_Y - 2), (CX + HEAD_R * 0.92, HEAD_Y - 2),
             (CX + HEAD_R * 0.78, HEAD_Y + 5.5), (CX - HEAD_R * 0.78, HEAD_Y + 5.5)], 'G')
    for i in range(5):                   # locks at the nape, uneven
        x = CX - 7.2 + i * 3.6
        poly(g, [(x - 1.7, HEAD_Y + 3), (x + 1.7, HEAD_Y + 3),
                 (x + 1.3, HEAD_Y + 7.4 + (1.6 if i % 2 else 0)),
                 (x - 1.3, HEAD_Y + 6.6 + (1.6 if i % 2 else 0))], 'G')
    for i in range(6):                   # strand shadow and sheen
        x = CX - 7.6 + i * 3.1
        line_on(g, x, HEAD_Y - 8, x + 0.9, HEAD_Y + 6, 'g', 'G', 1.0)
        line_on(g, x - 1.3, HEAD_Y - 8, x - 0.4, HEAD_Y + 6, 'H', 'G', 0.9)
    poly(g, [(CX - 10, HEAD_Y - 7), (CX + 10, HEAD_Y - 7), (CX + 10.4, HEAD_Y + 3),
             (CX + 6, HEAD_Y - 1), (CX - 6, HEAD_Y - 1), (CX - 10.4, HEAD_Y + 3)], 'G')
    g = model(g)
    # His own clothes: a plain tunic. What was here before was two solid
    # slabs of accent colour wider than the torso they sat on, one at
    # the hips and one at the hem, and they read as planks nailed across
    # him rather than as a belt and a hem.
    for i in range(4):                   # cloth, so it hangs in folds
        x = CX - 6.6 + i * 4.4
        cut(g, x, SH_Y + 3, x + (1.1 if i % 2 else -1.1), WAIST - 4, 1.0, 2, -2, 1.1)
    belt(g, WAIST - 3.2, 3.0, 8.4, 'G', 'C')
    # and the hem, which follows the body instead of squaring it off
    for i in range(5):
        x = CX - 8.0 + i * 4.0
        cut(g, x, WAIST + 1, x + (1.3 if i % 2 else -1.3), HEM - 2, 1.0, 2, -2, 1.1)
    shift_line(g, CX - 9.8, HEM - 2.6, CX + 9.8, HEM - 2.6, 2, 1.0)
    line_on(g, CX - 9.8, HEM - 1.6, CX + 9.8, HEM - 1.6, 'C', 'A', 1.0)
    shift_line(g, CX - 9.9, HEM - 0.5, CX + 9.9, HEM - 0.5, -2, 1.1)
    g = ao(g); g = rim(g); g = dither(g); g = despeckle(g)
    return dump(softline(outline(g)))

def H_crown_grand():
    """The legendary crown, worn. Its points are taller, wider apart and
       each carries a lit edge to hold it off its neighbour, because at
       this size a crown is its gaps and five short points close
       together just merge into a lump under the modelling pass.

       Like the plain circlet it used to sit six rows too low, with its
       band down at the ears."""
    g = blank()
    BT, BB = HEAD_Y - 5, HEAD_Y + 1
    TOPS = ((-11, -7), (-5.5, -10), (0, -12), (5.5, -10), (11, -7))
    VAL = BT + 1
    pts = [(CX - 12.5, BT)]
    for (dx, dy) in TOPS:
        pts += [(CX + dx - 2.0, VAL), (CX + dx, HEAD_Y + dy), (CX + dx + 2.0, VAL)]
    pts.append((CX + 12.5, BT))
    poly(g, pts, 'C')
    poly(g, [(CX - 12.5, BT), (CX + 12.5, BT),
             (CX + 12.5, BB), (CX - 12.5, BB)], 'C')
    g = model(g)
    for (dx, dy) in TOPS:
        line_on(g, CX + dx - 0.9, HEAD_Y + dy + 1, CX + dx - 0.9, BT + 1.5, 'Z', 'C', 1.0)
        line_on(g, CX + dx + 1.1, HEAD_Y + dy + 2, CX + dx + 1.1, BT + 1.5, 'x', 'C', 1.0)
        disc(g, CX + dx, HEAD_Y + dy + 0.6, 1.5, 'A')
        put(g, CX + dx, HEAD_Y + dy, 'W')
    line_on(g, CX - 12.5, BT + 1, CX + 12.5, BT + 1, 'Z', 'C', 1.1)
    line_on(g, CX - 12.5, BB - 1, CX + 12.5, BB - 1, 'x', 'C', 1.1)
    for gx in (-7, 0, 7):
        disc(g, CX + gx, (BT + BB) * 0.5, 2.0, 'A')
        put(g, CX + gx - 1, (BT + BB) * 0.5 - 1, 'W')
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

def gripArmL():
    """His left forearm, come across and closed on the shield's strap.
       Drawn over the shield and under the body, the same way the right
       arm is drawn over whatever he carries. The body layer hangs this
       arm straight down, and a straight arm beside a shield reads as a
       shield floating at his side rather than one he is holding.

       Reach and build mirror the right arm exactly, lifted a little so
       the fist lands near the middle of the shield's back rather than
       down on its rim."""
    g = blank()
    taper(g, CX - 10, SH_Y + 1, CX - 16, WAIST - 2, 8, 7, 'A')
    g = model(g)
    disc(g, CX - 16.5, WAIST + 0.5, 4.0, 'm')
    # knuckles, closed across the strap
    poly(g, [(CX - 19.0, WAIST - 3.0), (CX - 15.0, WAIST - 1.6),
             (CX - 14.6, WAIST + 1.2), (CX - 18.6, WAIST - 0.2)], 'm')
    line_on(g, CX - 19.6, WAIST - 0.6, CX - 13.2, WAIST - 0.6, 'u', 'm', 0.9)
    line_on(g, CX - 19.4, WAIST + 1.8, CX - 13.4, WAIST + 1.8, 'u', 'm', 0.9)
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

def hatcrown(g, apex_y, base_y=None, bw=10.2, ch='A'):
    """The crown of a hat, shaped to the head under it. Drawn as a plain
       cone from the brim to the point, the skull was wider than the hat
       for the first several rows above the brim and its corners stuck
       out either side of it."""
    base_y = HEAD_Y + 1.0 if base_y is None else base_y
    side = []
    for (y, f) in ((base_y, 1.00), (HEAD_Y - 2.5, 0.97), (HEAD_Y - 6.0, 0.84),
                   (HEAD_Y - 9.5, 0.58), (apex_y + 1.4, 0.20)):
        side.append((y, bw * f))
    pts  = [(CX + w, y) for (y, w) in side]
    pts += [(CX + 1.1, apex_y), (CX - 1.1, apex_y)]
    pts += [(CX - w, y) for (y, w) in reversed(side)]
    poly(g, pts, ch)

def hat():
    g = blank()
    hatcrown(g, HEAD_Y - 13.0, HEAD_Y + 1.0, 10.4)
    ellipse(g, CX, HEAD_Y + 2.0, 14.6, 4.0, 'A')
    g = model(g)
    cut(g, CX + 3.6, HEAD_Y - 9.0, CX + 6.4, HEAD_Y + 0.4, 1.1)
    edgelight(g, CX - 2.6, HEAD_Y - 10.0, CX - 6.2, HEAD_Y + 0.4, 1.3, 2)
    poly(g, [(CX - 9.8, HEAD_Y - 3.4), (CX + 9.8, HEAD_Y - 3.4),
             (CX + 10.4, HEAD_Y + 0.6), (CX - 10.4, HEAD_Y + 0.6)], 'C')
    line_on(g, CX - 10.0, HEAD_Y - 2.7, CX + 10.0, HEAD_Y - 2.7, 'Z', 'C', 0.9)
    stud(g, CX + 6, HEAD_Y - 1.4, 1.9)
    edgelight(g, CX - 15.6, HEAD_Y + 1.0, CX + 15.6, HEAD_Y + 1.0, 1.1, 2)
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
    g = blank(); dome(g, HEAD_R + 2.0)
    poly(g, [(CX - 11, HEAD_Y), (CX + 11, HEAD_Y),
             (CX + 13, SH_Y + 2), (CX - 13, SH_Y + 2)], 'A')
    g = model(g)
    for i in range(4):
        x = CX - 8.4 + i * 5.6
        cut(g, x, HEAD_Y - 6, x + (1.4 if i % 2 else -1.4), SH_Y + 1, 1.1)
    poly(g, [(CX - 12.4, SH_Y - 1), (CX + 12.4, SH_Y - 1),
             (CX + 12.4, SH_Y + 2.6), (CX - 12.4, SH_Y + 2.6)], 'C')
    line_on(g, CX - 12.4, SH_Y - 0.2, CX + 12.4, SH_Y - 0.2, 'Z', 'C', 0.9)
    for sx in (-8, 0, 8): stud(g, CX + sx, SH_Y + 1, 1.3, 'A', 'W')
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
    """A great helm: a tapered barrel with a rounded crown, not the flat
       slab it was, which with its two bands read as three plates
       stacked on his shoulders rather than one helmet."""
    g = blank()
    poly(g, [(CX - 8.4, HEAD_Y - 9.4), (CX + 8.4, HEAD_Y - 9.4),
             (CX + 10.6, HEAD_Y - 5), (CX + 10.8, HEAD_Y + 5),
             (CX + 9.0, HEAD_Y + 12), (CX - 9.0, HEAD_Y + 12),
             (CX - 10.8, HEAD_Y + 5), (CX - 10.6, HEAD_Y - 5)], 'A')
    ellipse(g, CX, HEAD_Y - 8.6, 8.6, 4.4, 'A')
    g = model(g)
    comb(g, HEAD_Y - 12.4, HEAD_Y - 5.6, 2.6)
    # a reinforce down the spine of the helm, and the brow band
    cut(g, CX - 3.0, HEAD_Y - 7, CX - 3.0, HEAD_Y + 11, 1.1)
    cut(g, CX + 3.6, HEAD_Y - 7, CX + 3.6, HEAD_Y + 11, 1.1)
    edgelight(g, CX, HEAD_Y - 7, CX, HEAD_Y + 11, 1.2, 2)
    band(g, HEAD_Y - 6.4, 2.8, 10.6, 4)
    cut(g, CX - 9.4, HEAD_Y + 8.4, CX + 9.4, HEAD_Y + 8.4, 1.2)
    for bx in (-5, -1.6, 1.6, 5):
        disc(g, CX + bx, HEAD_Y + 10.2, 0.9, 'q')
    for sx in (-8.6, 8.6):
        for sy in (-1, 2.4, 5.8): stud(g, CX + sx, HEAD_Y + sy, 1.1)
    return fin(g)

def H_crown():
    """A circlet sits on the upper half of the skull. This one had its
       band down at the ears, six rows lower, which read as a crown that
       had slipped. Raising it leaves less room above for the points, so
       they are shorter as well as higher."""
    g = blank()
    BT, BB = HEAD_Y - 5, HEAD_Y + 1          # band top and bottom
    pts = [(CX - 11, BT), (CX - 10, HEAD_Y - 8), (CX - 5, HEAD_Y - 3),
           (CX, HEAD_Y - 11), (CX + 5, HEAD_Y - 3), (CX + 10, HEAD_Y - 8),
           (CX + 11, BT)]
    poly(g, pts + [(CX + 11, BB), (CX - 11, BB)], 'C')
    poly(g, [(CX - 11, BT), (CX + 11, BT), (CX + 11, BB), (CX - 11, BB)], 'C')
    g = model(g)
    for (px, top) in ((CX - 10, HEAD_Y - 8), (CX, HEAD_Y - 11), (CX + 10, HEAD_Y - 8)):
        line_on(g, px - 0.8, top + 1, px - 0.8, BT + 1.5, 'Z', 'C', 1.0)
        line_on(g, px + 1.2, top + 2, px + 1.2, BT + 1.5, 'x', 'C', 1.0)
        stud(g, px, top + 0.6, 1.5, 'A', 'W')
    line_on(g, CX - 11, BT + 1, CX + 11, BT + 1, 'Z', 'C', 1.0)
    line_on(g, CX - 11, BB - 1, CX + 11, BB - 1, 'x', 'C', 1.0)
    for gx in (-6, 0, 6): gem(g, CX + gx, (BT + BB) * 0.5, 2.0, 'A', 5)
    return fin(g)

def H_brim():
    """A travelling hat: a real cone with volume in it, over a brim that
       no longer spans half the sprite."""
    g = blank()
    hatcrown(g, HEAD_Y - 12.6, HEAD_Y + 0.8, 10.2)
    ellipse(g, CX, HEAD_Y + 2.4, 12.6, 3.4, 'A')
    g = model(g)
    # the cone's lit side and the crease down its shaded side
    edgelight(g, CX - 2.2, HEAD_Y - 10.4, CX - 6.4, HEAD_Y - 0.5, 1.3, 2)
    cut(g, CX + 3.4, HEAD_Y - 9.4, CX + 6.8, HEAD_Y - 0.5, 1.1)
    # a band with a buckle, and the brim's own lit edge
    poly(g, [(CX - 9.6, HEAD_Y - 3.6), (CX + 9.6, HEAD_Y - 3.6),
             (CX + 10.2, HEAD_Y + 0.4), (CX - 10.2, HEAD_Y + 0.4)], 'C')
    line_on(g, CX - 9.8, HEAD_Y - 2.9, CX + 9.8, HEAD_Y - 2.9, 'Z', 'C', 0.9)
    line_on(g, CX - 10.1, HEAD_Y - 0.2, CX + 10.1, HEAD_Y - 0.2, 'x', 'C', 0.9)
    poly(g, [(CX + 3.4, HEAD_Y - 4.6), (CX + 6.6, HEAD_Y - 4.6),
             (CX + 6.6, HEAD_Y + 1.2), (CX + 3.4, HEAD_Y + 1.2)], 'G')
    put(g, CX + 5, HEAD_Y - 1.8, 'x')
    edgelight(g, CX - 12.0, HEAD_Y + 1.4, CX + 12.0, HEAD_Y + 1.4, 1.1, 2)
    shift_line(g, CX - 11.6, HEAD_Y + 4.0, CX + 11.6, HEAD_Y + 4.0, -2, 1.3)
    return fin(g)

def H_barbute():
    """Rounded crown, a raised comb, and cheeks that come down past the
       jaw. It was a flat topped box with a band across it."""
    g = blank()
    ellipse(g, CX, HEAD_Y - 5.0, 10.6, 8.0, 'A')
    poly(g, [(CX - 10.6, HEAD_Y - 5), (CX + 10.6, HEAD_Y - 5),
             (CX + 11.4, HEAD_Y + 4), (CX + 7.6, HEAD_Y + 12),
             (CX - 7.6, HEAD_Y + 12), (CX - 11.4, HEAD_Y + 4)], 'A')
    g = model(g)
    comb(g, HEAD_Y - 13, HEAD_Y - 4, 2.8)
    band(g, HEAD_Y - 5.6, 2.6, 11.0, 4)
    # the two cheek plates, cut away from the crown so they read as
    # separate pieces hinged on
    for k in (-1, 1):
        cut(g, CX + k * 7.2, HEAD_Y - 2, CX + k * 5.6, HEAD_Y + 11.4, 1.1)
    cut(g, CX - 9.6, HEAD_Y + 4.4, CX + 9.6, HEAD_Y + 4.4, 1.2)
    for sx in (-7.6, -2.6, 2.6, 7.6): stud(g, CX + sx, HEAD_Y + 10.4, 1.1)
    return fin(g)

def H_wolf():
    """The wolf pelt hood, worn. From behind what tells you it is a wolf
       and not a cowl is the ears, so they stand clear of the dome, and
       the pelt below is shaggy rather than smooth, with the scruff of
       the neck across his shoulders."""
    g = blank()
    # the pelt falling over his shoulders
    poly(g, [(CX - 10.5, HEAD_Y - 2), (CX + 10.5, HEAD_Y - 2),
             (CX + 13.5, SH_Y - 1), (CX + 12.0, SH_Y + 2.5),
             (CX - 12.0, SH_Y + 2.5), (CX - 13.5, SH_Y - 1)], 'A')
    # The ears have to clear the dome SIDEWAYS. There is no room above
    # it inside the sprite, so an ear drawn straight up sat inside the
    # hood's own silhouette and all you saw was a brown box.
    for k in (-1, 1):
        poly(g, [(CX + k*6.5, HEAD_Y - 3.5), (CX + k*11.5, HEAD_Y - 12),
                 (CX + k*15.5, HEAD_Y - 5.0), (CX + k*11.0, HEAD_Y + 1.5)], 'A')
    dome(g, HEAD_R + 1.6)
    g = model(g)
    for k in (-1, 1):                     # the inside of each ear
        poly(g, [(CX + k*8.6, HEAD_Y - 2.6), (CX + k*11.4, HEAD_Y - 10.2),
                 (CX + k*14.0, HEAD_Y - 4.6)], 'd')
        poly(g, [(CX + k*9.8, HEAD_Y - 2.8), (CX + k*11.4, HEAD_Y - 8.4),
                 (CX + k*12.8, HEAD_Y - 4.6)], 'q')
    # fur, falling in uneven hanks. Shallow marks vanished into the
    # pelt and left a smooth brown dome, which is the thing a wolf skin
    # is not.
    for i in range(8):
        x = CX - 9.8 + i * 2.8
        cut(g, x, HEAD_Y - 7, x + (1.7 if i % 2 else -1.7), SH_Y + 1.5, 1.2, 2, -3, 1.3)
    for i in range(4):
        x = CX - 7.5 + i * 5.0
        cut(g, x, HEAD_Y - 9.5, x - 1.2, HEAD_Y - 2, 1.0, 1, -2, 1.1)
    # the scruff of the neck, across the shoulders
    furtrim(g, [(CX - 13.4, SH_Y - 1), (CX - 9, SH_Y + 2), (CX - 3, SH_Y + 3)], 2.6, 'A', 'B')
    furtrim(g, [(CX + 13.4, SH_Y - 1), (CX + 9, SH_Y + 2), (CX + 3, SH_Y + 3)], 2.6, 'A', 'B')
    # the thong that holds it on, and a claw strung on it
    strap(g, CX - 11, SH_Y - 1, CX + 11, SH_Y - 1, 2.4)
    poly(g, [(CX - 1.3, SH_Y + 0.5), (CX + 1.3, SH_Y + 0.5),
             (CX + 0.8, SH_Y + 5), (CX - 0.8, SH_Y + 5)], 'H')
    return fin(g)

def H_cap():
    g = blank(); dome(g, HEAD_R + 0.8, -1)
    g = model(g)
    comb(g, HEAD_Y - 9, HEAD_Y, 2.0)
    band(g, HEAD_Y + 1, 3.2, 10.0, 3)
    for k in (-1, 1):                                   # cheek flaps, laced
        poly(g, [(CX + k*9, HEAD_Y + 4), (CX + k*13, HEAD_Y + 4),
                 (CX + k*12, HEAD_Y + 12), (CX + k*8, HEAD_Y + 10)], 'G')
        line_on(g, CX + k*9, HEAD_Y + 6, CX + k*12, HEAD_Y + 6, 'K', 'G', 0.9)
        line_on(g, CX + k*9, HEAD_Y + 10, CX + k*12, HEAD_Y + 10, 'j', 'G', 0.9)
        stud(g, CX + k*11, HEAD_Y + 8, 1.2)
    return fin(g)

# --------------------------------------------------------------- bodies
# These are the same five pieces as the icons, worn. They are built
# with the same helpers so a fluted cuirass in the pack is a fluted
# cuirass on his back, not a differently shaped grey rectangle.
def B_cuirass():
    """Fluted plate: pauldrons that break the shoulder line, a plackart
       lapped over the breast, a belt, and a tasseted fauld."""
    g = blank()
    shoulder(g, -1, w=8.2, h=12.0, plates=3)
    shoulder(g,  1, w=7.0, h=10.5, plates=2)
    shell(g, 'A', 9.0, 7.0, 9.8)
    seam(g, 9.0, 7.0, 9.8)
    g = model(g)
    for t in (-1, 1):
        cut(g, CX + t * 4.6, SH_Y + 9, CX + t * 5.4, WAIST - 1, 1.1, 2, -2, 1.2)
    edgelight(g, CX, SH_Y + 8, CX, WAIST - 1, 1.1, 3)
    plackart(g, SH_Y + 1, 9.4, 8.4)
    belt(g)
    fauld(g, 3, w=9.0)
    gorget(g, CX, SH_Y - 3, 7.5, 3)
    for k in (-1, 1):
        stud(g, CX + k * 6.6, WAIST - 2.6, 1.2)
        cut(g, CX + k * 8.6, SH_Y + 2, CX + k * 7.2, WAIST - 2, 1.0)
    return fin(g)

def B_scale():
    """Mail: a scale field over a padded gambeson, with a collar, a
       sash, and a brass-edged hem."""
    g = blank()
    shoulder(g, -1, w=6.8, h=10.0, plates=2)
    shoulder(g,  1, w=7.4, h=11.0, plates=3)
    shell(g, 'A', 9.0, 7.2, 10.0)
    seam(g, 9.0, 7.2, 10.0)
    g = model(g)
    for row in range(10):
        y = SH_Y + 2.4 + row * 2.3
        if y > HEM - 1: break
        t = (y - SH_Y) / float(HEM - SH_Y)
        half = 10.2 - 2.4 * (1 - abs(t - 0.52) * 2.0)
        off = 1.2 if row % 2 else 0
        scales(g, CX - half + off, CX + half, y, y, step=2.5, r=1.4)
    gorget(g, CX, SH_Y - 2, 8.4, 3)
    belt(g, WAIST - 1, 2.8, 8.8)
    strap(g, CX - 9, SH_Y + 3, CX + 8, SH_Y + 13, 2.4)
    poly(g, [(CX - 9.8, HEM - 2.4), (CX + 9.8, HEM - 2.4),
             (CX + 9.6, HEM - 0.4), (CX - 9.6, HEM - 0.4)], 'C')
    line_on(g, CX - 9.8, HEM - 1.9, CX + 9.8, HEM - 1.9, 'Z', 'C', 0.9)
    return fin(g)

def B_robe():
    """Cloth: a narrow body under a long open overrobe, sleeves that
       flare at the cuff, a sash, and a trimmed stole down the front."""
    g = blank()
    for k, w, c in ((-1, 13.2, 5.5), (1, 12.4, 5.0)):
        poly(g, [(CX + k * 9.4, SH_Y - 1), (CX + k * w, SH_Y + 7),
                 (CX + k * (w - 2.0), WAIST), (CX + k * (w - 0.5), HEM - 1),
                 (CX + k * 9.4, HEM - 3)], 'A')
        # cuff, a step wider than the sleeve so the arm reads as ending
        poly(g, [(CX + k * (w - 0.5), HEM - 5.5), (CX + k * (w + 1.4), HEM - 5.0),
                 (CX + k * (w + 1.0), HEM - 1.2), (CX + k * (w - 1.8), HEM - 1.6)], 'C')
    shell(g, 'A', 8.8, 7.0, 9.8)
    seam(g, 8.8, 7.0, 9.8)
    g = model(g)
    folds(g, CX - 9, CX + 9, SH_Y + 3, HEM - 1, n=5)
    # the overrobe's front edges, lit on one lip and shadowed on the other
    for k in (-1, 1):
        cut(g, CX + k * 4.6, SH_Y + 2, CX + k * 5.8, HEM - 1, 1.2, 2, -3, 1.1)
    # stole: a trimmed band down the centre
    poly(g, [(CX - 2.6, SH_Y + 1), (CX + 2.6, SH_Y + 1),
             (CX + 2.2, HEM - 1), (CX - 2.2, HEM - 1)], 'C')
    line_on(g, CX - 2.6, SH_Y + 1.6, CX - 2.6, HEM - 1.4, 'Z', 'C', 0.9)
    line_on(g, CX + 2.2, SH_Y + 1.6, CX + 2.2, HEM - 1.4, 'c', 'C', 0.9)
    for i in range(4):
        y = SH_Y + 5 + i * 4.8
        shift_line(g, CX - 2.4, y, CX + 2.4, y, -2, 1.0)
        shift_line(g, CX - 2.4, y - 1.1, CX + 2.4, y - 1.1, 2, 0.9)
    belt(g, WAIST - 2, 3.0, 9.0, 'G', 'C')
    # a hood pooled at the back of the neck, which is what makes it a robe
    poly(g, [(CX - 7.5, SH_Y - 3), (CX + 7.5, SH_Y - 3),
             (CX + 6.2, SH_Y + 3.4), (CX - 6.2, SH_Y + 3.4)], 'd')
    edgelight(g, CX - 7.2, SH_Y - 2.4, CX + 7.2, SH_Y - 2.4, 1.0, 2)
    return fin(g)

def B_banded():
    """Lamellar: horizontal bands the whole way down, held by vertical
       leather, with shoulder caps and a studded belt."""
    g = blank()
    shoulder(g, -1, w=7.6, h=11.0, plates=3)
    shoulder(g,  1, w=7.6, h=11.0, plates=3)
    shell(g, 'A', 9.0, 7.0, 9.8)
    seam(g, 9.0, 7.0, 9.8)
    g = model(g)
    for i in range(4):
        y = SH_Y + 2 + (WAIST - 3 - SH_Y) * (i + 1) / 5.0
        cut(g, CX - 9.6, y, CX + 9.6, y, 1.2, 2, -3, 1.2)
        for k in (-1, 1): stud(g, CX + k * 8.2, y - 2.0, 1.1)
    gorget(g, CX, SH_Y - 3, 7.8, 3)
    belt(g, WAIST - 1, 3.2, 9.0)
    fauld(g, 2, WAIST + 2.6, 9.2)
    for k in (-1, 1):
        strap(g, CX + k * 6.4, SH_Y + 1, CX + k * 7.4, WAIST - 1, 2.2, False)
        for i in range(3):
            stud(g, CX + k * 6.8, SH_Y + 4 + i * 4.4, 1.1)
    return fin(g)

def B_carapace():
    """Legendary: a ridged spine, a high asymmetric collar, swept plates
       that run past the shoulders, and veins of accent light in the
       gaps between them."""
    g = blank()
    # swept back plates, longer on his left, which stops it reading as
    # a symmetrical machined thing
    for k, w, h in ((-1, 14.4, 10), (1, 12.8, 8)):
        poly(g, [(CX + k * 9, SH_Y - 3), (CX + k * w, SH_Y + h),
                 (CX + k * (w - 2.5), WAIST + 2), (CX + k * 9, HEM - 2)], 'A')
        line_on(g, CX + k * 9, SH_Y - 2.4, CX + k * w, SH_Y + h - 0.6, 'W', 'A', 1.1)
        line_on(g, CX + k * (w - 2.5), WAIST + 2, CX + k * 9, HEM - 2, 'q', 'A', 1.1)
    shell(g, 'A', 9.0, 7.2, 10.0)
    seam(g, 9.0, 7.2, 10.0)
    g = model(g)
    # the spine: chevrons stacked up the centre with an accent core
    for i in range(7):
        y = SH_Y + 1 + i * 3.1
        poly(g, [(CX, y), (CX + 3.6, y + 1.5), (CX, y + 3.1), (CX - 3.6, y + 1.5)], 'C')
        line_on(g, CX - 2.8, y + 1.5, CX + 2.8, y + 1.5, 'Z', 'C', 0.9)
        line_on(g, CX - 3.2, y + 2.4, CX + 3.2, y + 2.4, 'c', 'C', 0.9)
    # ribs sweeping out from the spine, each with a lit upper lip
    for k in (-1, 1):
        for i in range(5):
            y = SH_Y + 3 + i * 4.2
            cut(g, CX + k * 5, y, CX + k * 12, y + 1.8, 1.2, 3, -3, 1.2)
            if i % 2 == 0:
                line_on(g, CX + k * 6.4, y + 3.0, CX + k * 10.6, y + 4.2, 'Z', 'A', 0.9)
    # high collar, taller on one side
    poly(g, [(CX - 8.4, SH_Y - 2), (CX - 5.2, SH_Y - 8), (CX - 3.0, SH_Y - 2)], 'C')
    poly(g, [(CX + 3.0, SH_Y - 2), (CX + 5.6, SH_Y - 6), (CX + 8.4, SH_Y - 2)], 'C')
    gorget(g, CX, SH_Y - 2.6, 8.2, 3)
    belt(g, WAIST, 2.8, 9.0, 'G', 'C')
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
SHAPES += [stick(), hands(), H_crown_grand(), gripArm(), gripArmL()]
# 25-26 bare arms, 27-28 sleeved, 29-30 the robe's long sleeve
SHAPES += [arm(1), arm(-1)]
SHAPES += [sleeve(1), sleeve(-1)]
SHAPES += [sleeve(1, 'A', HEM - 6, 8.4, 7.2, None), sleeve(-1, 'A', HEM - 6, 8.4, 7.2, None)]
SHAPES += [H_wolf()]                                  # 31, the wolf pelt hood
P.setsize(96)
