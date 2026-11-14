# -*- coding: utf-8 -*-
"""The fifteen companions, in full colour, two frames each.

Built with forge.py. Each builder takes the frame (0 or 1: the legs, or
the wings, at the two ends of a stride) and returns a Canvas. Side view,
facing right, standing on the bottom of a 96 pixel frame, so they sit
in the pack grid and walk the trail the way the old letter sprites did.

Direction, from the brief: the bosses' finish, and the creatures of the
games that do this best. Weight and wear rather than cute: scars, worn
claws, moss in the cracks, eyes that catch the light.
"""
import math
from forge import *

GROUND = 91


# ------------------------------------------------------------- helpers
def leg(C, hip, knee, paw, r0, r1, fur, claw, z=0.0, toes=3):
    C.limb([(hip[0], hip[1], r0, z), (knee[0], knee[1], r1 * 1.15, z + 1),
            (paw[0], paw[1] - 1.5, r1, z + 2)], fur)
    C.ell(paw[0] + 1.6, paw[1] - 1.2, r1 + 1.6, r1 * 0.75, r1, fur, z=z + 2)
    for i in range(toes):
        tx = paw[0] + 2.5 + i * 1.6
        C.ell(tx + 1.4, paw[1] - 0.3, 1.2, 0.8, 1, claw, z=z + 4)


def eye(C, x, y, r, iris, glint=(255, 255, 240), pupil=(12, 8, 10), slit=False):
    C.ball(x, y, r, iris, z=30)
    if slit:
        for dy in range(-int(r), int(r) + 1):
            C.dot(x, y + dy, pupil)
    else:
        C.dot(x + 0.3, y + 0.2, pupil)
    C.dot(x - r * 0.45, y - r * 0.5, glint)


def stride(f, a=1.0):
    """two poses: legs reaching (0) and legs passing (1)"""
    return a if f == 0 else -a


# ============================================================== hounds
def hound(f, coat, belly, dark, eyec, collar=None, spikes=None, scar=True, pup=False,
          brindle=False, seed=1):
    C = Canvas()
    furA = Mat(coat, 8, tex=lambda c: tex_strands(c, 160, 1.3, seed))
    furB = Mat(belly, 7, tex=lambda c: tex_strands(c, 110, 1.0, seed + 1))
    furD = Mat(dark, 7, tex=lambda c: tex_strands(c, 160, 1.2, seed + 2))
    if brindle:
        base_tex = furA.tex
        furA.tex = lambda c: base_tex(c) + ((np.sin(c.X * 0.8 + vnoise(c.X, c.Y, 0.2, 9) * 7) > 0.5) * -2.0)
    claw = Mat('#d8cfb5', 5, dark=0.6)
    eyem = Mat(eyec, 5, emit=True, glow=2.5)
    nose = Mat('#2a2226', 5, spec=0.6)
    s = stride(f)
    if pup:
        bx, by = 42, 64
        leg(C, (bx + 12, by + 4), (bx + 13 - 2 * s, by + 14), (bx + 12 - 4 * s, GROUND), 5, 3.6, furD, claw, z=-10)
        leg(C, (bx - 10, by + 3), (bx - 14 + 2 * s, by + 14), (bx - 11 + 4 * s, GROUND), 6, 3.6, furD, claw, z=-10)
        C.limb([(bx - 15, by - 2, 3.6), (bx - 22, by - 8, 3.0), (bx - 24, by - 16 - 2 * s, 2.2)], furA, z=-4)
        C.tufts([(bx - 18, by - 5), (bx - 24, by - 15)], furA, z=-3, n=3, length=3, width=3, out=(-1, -0.2), seed=seed)
        C.ell(bx - 4, by, 15, 12, 12, furA)
        C.ell(bx + 8, by - 2, 12, 12, 12, furA)
        C.ell(bx + 4, by + 7, 12, 5, 8, furB, z=4)
        C.tufts([(bx - 12, by + 10), (bx + 12, by + 10)], furB, z=6, n=6, length=3, width=3, out=(0, 1), seed=seed)
        hx, hy = bx + 22, by - 17
        C.limb([(bx + 10, by - 6, 9), (hx - 4, hy + 6, 8)], furA, z=4)
        C.ell(hx, hy, 13, 11.5, 12, furA, z=8)
        C.tufts([(hx - 10, hy - 6), (hx + 2, hy - 11)], furA, z=9, n=4, length=3, width=3.4, out=(-0.3, -1), seed=seed)
        C.ell(hx + 10, hy + 4, 6.5, 5, 6, furB, z=14, rot=0.1)
        C.ball(hx + 15.5, hy + 2.4, 2.6, nose, z=22)
        C.plate([(hx - 8, hy - 7), (hx - 2, hy - 9), (hx - 2, hy + 7), (hx - 10, hy + 5)], furD, z=16, tilt=(-0.4, 0.2))
        eye(C, hx + 5, hy - 1, 2.8, eyem)
        if collar:
            cm = Mat(collar, 6, spec=0.2)
            C.limb([(bx + 13, by - 12, 3), (bx + 18, by - 5, 3)], cm, z=24)
            tag = Mat('#e8c25a', 5, spec=0.8, gloss=0.8)
            C.ball(bx + 19, by - 2, 2, tag, z=28)
        leg(C, (bx + 12, by + 4), (bx + 11 + 2 * s, by + 14), (bx + 13 + 4 * s, GROUND), 6, 4.2, furA, claw, z=14)
        leg(C, (bx - 8, by + 3), (bx - 12 - 2 * s, by + 14), (bx - 8 - 4 * s, GROUND), 7, 4.2, furA, claw, z=14)
        return C

    bx, by = 44, 58
    # far legs first, behind the body
    leg(C, (bx + 18, by + 6), (bx + 20 - 3 * s, by + 20), (bx + 18 - 6 * s, GROUND), 6, 3.4, furD, claw, z=-10)
    C.limb([(bx - 14, by + 2, 5.5, -10), (bx - 20 + 2 * s, by + 18, 3.6, -9), (bx - 16 + 6 * s, GROUND - 2, 3.2, -8)], furD)
    C.ell(bx - 14 + 6 * s, GROUND - 1.2, 4.6, 2.4, 3, furD, z=-7)
    # tail, low and brushy
    tail = [(bx - 19, by - 6, 4.4), (bx - 29, by - 8, 4.2), (bx - 38, by - 14 - 2 * s, 3.4), (bx - 40, by - 22 - 3 * s, 2.0)]
    C.limb(tail, furA, z=-4)
    C.tufts([(bx - 30, by - 4), (bx - 39, by - 18 - 3 * s)], furD, z=-3, n=4, length=4, width=3.6, out=(-1, 0.3), seed=seed)
    # body: haunch, barrel, deep chest, shoulder hump
    C.ell(bx - 13, by - 1, 10, 10.5, 10, furA)
    C.ell(bx + 1, by + 1, 17, 10, 11, furA, rot=-0.08)
    C.ell(bx + 1, by + 8, 13, 4.5, 9, furB, z=4)
    C.ell(bx + 16, by - 3, 14, 15, 14, furA)
    C.ell(bx + 18, by + 5, 9, 9, 10, furB, z=6)
    C.ell(bx + 12, by - 13, 10, 6, 8, furD, z=4)
    # the mane: a ridge of tufts down the back, a ruff under the throat
    C.tufts([(bx + 6, by + 11), (bx + 24, by + 12)], furB, z=10, n=5, length=4, width=3.6, out=(-0.2, 1), seed=seed + 2)
    # neck and head
    hx, hy = bx + 32, by - 21
    C.limb([(bx + 18, by - 6, 10), (hx - 5, hy + 6, 8)], furA, z=4)
    C.tufts([(bx + 22, by + 4), (hx - 6, hy + 12)], furB, z=12, n=5, length=5, width=4, out=(-0.6, 0.8), seed=seed + 5)
    C.ell(hx, hy, 10.5, 9, 10, furA, z=8)
    C.ell(hx + 9, hy + 4, 9, 5.0, 6, furA, z=12, rot=0.14)
    C.ell(hx + 8, hy + 7.5, 7, 2.6, 5, furB, z=13)
    C.ball(hx + 17, hy + 3.2, 2.5, nose, z=20)
    # lip line and a tooth showing
    for x in range(int(hx + 4), int(hx + 15)):
        C.dot(x, hy + 6.5 + (x - hx - 4) * 0.08, (30, 20, 20))
    C.dot(hx + 12, hy + 7.6, (236, 228, 206)); C.dot(hx + 12, hy + 8.6, (200, 190, 170))
    # ears
    C.plate([(hx - 8, hy - 5), (hx - 7, hy - 19), (hx + 0, hy - 7)], furD, z=6, tilt=(0.2, -0.4))
    C.plate([(hx - 3, hy - 6), (hx + 0, hy - 20), (hx + 6, hy - 6)], furA, z=16, tilt=(-0.5, -0.4))
    C.plate([(hx - 1, hy - 8), (hx + 0.6, hy - 16), (hx + 4, hy - 8)], furB, z=17, tilt=(-0.3, -0.2))
    C.tufts([(hx - 8, hy - 2), (hx - 4, hy + 8)], furA, z=9, n=3, length=4, width=3.4, out=(-1, 0.2), seed=seed + 7)
    C.ell(hx + 3, hy - 3.6, 5.5, 2, 3, furD, z=16, rot=-0.25)
    eye(C, hx + 4, hy - 1, 1.9, eyem)
    if scar:
        for i in range(5):
            C.dot(hx - 2 + i, hy - 6 + i * 1.7, (204, 160, 146))
    if collar:
        cm = Mat(collar, 6, spec=0.2)
        C.limb([(bx + 22, by - 14, 3.2), (bx + 27, by - 6, 3.2)], cm, z=24)
        if spikes:
            sm = Mat(spikes, 6, spec=0.8, gloss=0.7)
            for i in range(3):
                x = bx + 22 + i * 2.6; y = by - 15 + i * 3.6
                C.plate([(x, y - 1.6), (x + 5, y - 3.2), (x + 0.8, y + 1.6)], sm, z=28, bevel=1)
    # near legs, in front
    leg(C, (bx + 18, by + 6), (bx + 18 + 3 * s, by + 20), (bx + 20 + 6 * s, GROUND), 7, 3.9, furA, claw, z=14)
    C.limb([(bx - 12, by + 1, 6.2, 14), (bx - 18 - 2 * s, by + 18, 3.8, 15), (bx - 13 - 6 * s, GROUND - 2, 3.6, 16)], furA)
    C.ell(bx - 11 - 6 * s, GROUND - 1.2, 5.2, 2.6, 3, furA, z=17)
    for i in range(3):
        C.ell(bx - 8 - 6 * s + i * 1.6, GROUND - 0.3, 1.2, 0.8, 1, claw, z=19)
    C.tufts([(bx - 20, by + 6), (bx - 22, by + 14)], furA, z=16, n=3, length=3.4, width=3, out=(-1, 0.4), seed=seed + 9)
    return C


def trail_mutt(f):
    return hound(f, '#8a5f3a', '#c9a678', '#5a3a22', '#f2c45a', collar='#9a2f26', seed=11, scar=True)


def brindle_pup(f):
    return hound(f, '#7b5a33', '#d2b48a', '#4a3020', '#a8d8ff', collar='#3a6ea8', pup=True,
                 brindle=True, seed=21, scar=False)


def ridge_hound(f):
    return hound(f, '#646a76', '#a9adb5', '#33363f', '#ff7a2a', collar='#3a2a22', spikes='#c8ccd4', seed=31)


# =============================================================== toads
def toad(f, skin, belly, dark, eyec, moss=False, ember=False, seed=4):
    C = Canvas()
    sk = Mat(skin, 7, tex=lambda c: tex_skin(c, 1.1, seed))
    bl = Mat(belly, 6, tex=lambda c: tex_skin(c, 0.4, seed + 1))
    dk = Mat(dark, 7, tex=lambda c: tex_skin(c, 0.9, seed + 2))
    eyem = Mat(eyec, 5, emit=True, glow=2)
    s = stride(f, 1.0)
    sit = 0 if f == 0 else -2       # it gathers itself, then rises
    # far legs
    C.limb([(34, 74 + sit, 8, -8), (22, 80, 6, -8), (30, 89, 4, -8)], dk)
    C.ell(34, 89.5, 7, 2.4, 3, dk, z=-6)
    C.limb([(60, 74 + sit, 5, -8), (64, 86, 3.5, -8)], dk)
    # body, low and wide
    C.ell(46, 70 + sit, 26, 17, 18, sk)
    C.ell(52, 78 + sit, 20, 9, 14, bl, z=6)
    # head merges in front, wide mouth line
    C.ell(66, 64 + sit, 17, 12, 14, sk, z=4)
    C.ell(70, 71 + sit, 14, 5, 12, bl, z=8)
    # eye turrets
    C.ball(62, 53 + sit, 7.5, sk, z=14)
    C.ball(74, 54 + sit, 6.5, sk, z=10)
    eye(C, 63, 52 + sit, 4.2, eyem, slit=True)
    eye(C, 75, 53 + sit, 3.4, eyem, slit=True)
    # mouth seam
    for x in range(58, 82):
        y = 68.5 + sit + (x - 70) ** 2 * 0.012
        C.dot(x, y, (34, 24, 22))
    # warts / ridge down the back
    for i, (x, y, r) in enumerate([(30, 56, 3.2), (38, 53, 3.6), (46, 52, 3.0), (54, 54, 2.6), (24, 62, 2.8)]):
        C.ball(x, y + sit, r, dk, z=16)
    if moss:
        mo = Mat('#5e8a2e', 7, tex=lambda c: (vnoise(c.X, c.Y, 0.7, 41) - 0.5) * 3.2)
        cap = Mat('#c2552e', 6, spec=0.3)
        stem = Mat('#e8dcc0', 5)
        C.ell(36, 55 + sit, 15, 6, 6, mo, z=20, rot=-0.12)
        C.ell(48, 52 + sit, 9, 4, 5, mo, z=22)
        for (x, y, h, r) in [(32, 50, 7, 4.5), (41, 47, 9, 5.5), (50, 49, 5, 3.2)]:
            C.limb([(x, y + sit + 2, 1.3, 26), (x, y + sit - h + 2, 1.2, 26)], stem)
            C.ell(x, y + sit - h, r, r * 0.55, r * 0.6, cap, z=30)
            C.dot(x - r * 0.4, y + sit - h - 0.5, (250, 236, 210))
    if ember:
        lava = Mat('#ff8a1e', 6, emit=True, glow=3,
                   tones=[(120, 24, 8), (196, 52, 12), (240, 104, 20), (255, 160, 48), (255, 214, 120), (255, 246, 210)])
        for (x0, y0, x1, y1) in [(30, 60, 40, 72), (40, 72, 52, 70), (52, 70, 58, 80), (44, 58, 50, 66), (62, 60, 70, 62)]:
            C.limb([(x0, y0 + sit, 0.9, 40), (x1, y1 + sit, 0.9, 40)], lava)
    # near legs: the big folded haunch and the front arm
    C.ell(34, 78 + sit, 13, 10, 12, sk, z=18)
    C.limb([(30, 84 + sit, 6, 20), (40, 89, 4, 22)], sk)
    C.ell(44, 89.5, 8, 2.4, 3, dk, z=24)
    C.limb([(68, 76 + sit, 5, 22), (72 + s, 88, 3.5, 24)], sk)
    C.ell(75 + s, 89.5, 5, 2, 3, dk, z=26)
    return C


def bog_frog(f):
    return toad(f, '#5c8a3a', '#d8d29a', '#33502a', '#f0d040', seed=51)


def mossback_toad(f):
    return toad(f, '#6b6a3a', '#cbbf8a', '#3d3a22', '#ff9b2e', moss=True, seed=61)


def emberfrog(f):
    return toad(f, '#3a2422', '#7a4a2e', '#1e1414', '#ffd04a', ember=True, seed=71)


# =============================================================== birds
def wing(C, root, span, up, mat, prim, z, feathers=6, frame=0, w=11.0):
    """a wing as one silhouette: a curved leading edge out to the tip and a
       trailing edge notched into primaries. `up` true raises it."""
    rx, ry = root
    L = span
    if up:
        d = (-0.42, -0.91); p = (-0.91, 0.42)
    else:
        d = (-0.62, 0.78); p = (-0.78, -0.62)
    def P(x, y):
        return (rx + d[0] * x * L + p[0] * y * L, ry + d[1] * x * L + p[1] * y * L)
    lead = [P(0, 0), P(0.3, -0.07), P(0.62, -0.06), P(0.88, -0.01), P(1.0, 0.04)]
    trail = []
    for i in range(feathers):
        t = i / (feathers - 1)
        x = 1.0 - t * 0.62
        trail.append(P(x - 0.02, 0.14 + 0.26 * t))
        trail.append(P(x - 0.09, 0.10 + 0.26 * t))
    trail += [P(0.28, 0.46), P(0.1, 0.42), P(-0.05, 0.24)]
    C.plate(lead + trail, prim, z=z, bevel=2.5, tilt=(-0.25, -0.35))
    # coverts: the lighter, rounded inner half of the wing
    cov = [P(-0.02, 0.0), P(0.3, -0.06), P(0.58, -0.04), P(0.6, 0.16), P(0.36, 0.32), P(0.05, 0.3)]
    C.plate(cov, mat, z=z + 1.5, bevel=3, tilt=(-0.3, -0.4))
    for j in range(3):
        sx, sy = P(0.12 + j * 0.13, 0.13 + j * 0.01)
        ex, ey = P(0.12 + j * 0.13 + 0.05, 0.24)
        C.limb([(sx, sy, 0.7, z + 6), (ex, ey, 0.6, z + 6)], prim)


def bird(f, body, belly, wingc, prim, beak, eyec, size=1.0, raptor=False, crest=None, storm=False,
         hood=None, seed=9, bars=None):
    C = Canvas()
    fb = Mat(body, 8, tex=lambda c: tex_feather(c, 0.9, seed, 3.6))
    fl = Mat(belly, 7, tex=lambda c: tex_feather(c, 0.6, seed + 1, 3.0) +
             ((np.sin(c.Y * 1.4) > 0.6) * -1.2 if bars else 0))
    fw = Mat(wingc, 8, tex=lambda c: tex_feather(c, 0.8, seed + 2, 3.2))
    fp = Mat(prim, 7, tex=lambda c: tex_strands(c, 120, 0.8, seed + 3, 260, 3))
    bk = Mat(beak, 6, spec=0.5, gloss=0.5)
    ey = Mat(eyec, 5, emit=True, glow=1.5)
    tal = Mat('#d8b24a' if raptor else '#3a3030', 5)
    k = size
    cx, cy = 50, 60
    # far wing behind everything
    wing(C, (cx + 6, cy - 6), 44 * k, f == 0, fw, fp, z=-12, frame=f, w=12 * k)
    # tail fan
    for i in range(4):
        a = 2.9 + i * 0.12
        L = 22 * k
        x0, y0 = cx - 14 * k, cy + 4
        C.plate([(x0, y0 - 3), (x0 + math.cos(a) * L, y0 + math.sin(a) * L - 3 + i * 2.2),
                 (x0 + math.cos(a) * L + 1, y0 + math.sin(a) * L + 2 + i * 2.2), (x0, y0 + 3)], fp, z=-2 + i, bevel=1.2)
    # body
    C.ell(cx, cy, 19 * k, 12.5 * k, 13, fb, rot=-0.25)
    C.ell(cx + 6, cy + 5, 12.5 * k, 9 * k, 11, fl, z=4, rot=-0.3)
    # head
    hx, hy = cx + 18 * k, cy - 12 * k
    C.ell(hx, hy, 10 * k, 9 * k, 10, fb, z=8)
    if hood:
        hm = Mat(hood, 6, spec=0.3)
        C.ell(hx - 1, hy - 1.5, 9.4 * k, 6.5 * k, 9, hm, z=10)
    C.ell(hx + 2, hy + 4, 6 * k, 4 * k, 6, fl, z=10)
    # beak: hooked for a raptor
    if raptor:
        C.plate([(hx + 6 * k, hy - 2), (hx + 15 * k, hy + 1), (hx + 13 * k, hy + 6), (hx + 10 * k, hy + 3), (hx + 6 * k, hy + 3)], bk, z=16, bevel=1.4)
    else:
        C.plate([(hx + 6 * k, hy - 1), (hx + 14 * k, hy + 1.5), (hx + 6 * k, hy + 3)], bk, z=16, bevel=1.2)
    if raptor:
        C.ell(hx + 2.5, hy - 3.2, 4.5, 1.6, 3, fb, z=18, rot=-0.15)   # the brow that makes it a raptor
    eye(C, hx + 3, hy - 1, 1.9 * k, ey)
    if crest:
        cm = Mat(crest, 6)
        C.tufts([(hx - 6, hy - 5), (hx + 1, hy - 8)], cm, z=12, n=4, length=6 * k, width=3, out=(-0.7, -0.8), seed=seed)
    # talons tucked under
    C.limb([(cx + 4, cy + 10, 2.4 * k), (cx + 2, cy + 18 * k, 1.8 * k)], tal, z=6)
    C.limb([(cx - 1, cy + 9, 2.4 * k), (cx - 3, cy + 17 * k, 1.8 * k)], tal, z=2)
    for x in (cx + 2, cx - 3):
        for i in range(3):
            C.dot(x + i - 1, cy + 18 * k + (i % 2), (30, 24, 20))
    # near wing over the body
    wing(C, (cx + 4, cy - 2), 50 * k, f == 0, fw, fp, z=20, frame=f, w=13 * k)
    if storm:
        bolt = Mat('#bfe8ff', 5, emit=True, glow=3,
                   tones=[(60, 120, 200), (110, 180, 245), (170, 220, 255), (220, 244, 255), (255, 255, 255)])
        pts = [(cx - 6, cy - 20 if f == 0 else cy - 6), (cx - 14, cy - 28 if f == 0 else cy + 2),
               (cx - 10, cy - 33 if f == 0 else cy + 6), (cx - 22, cy - 44 if f == 0 else cy + 10)]
        for i in range(3):
            C.limb([(pts[i][0], pts[i][1], 0.8, 40), (pts[i + 1][0], pts[i + 1][1], 0.8, 40)], bolt)
        C.ball(hx + 3, hy - 1, 2.4, Mat('#e8f8ff', 4, emit=True, glow=3), z=32)
    return C


def gray_jay(f):
    return bird(f, '#7a8088', '#d8d6cc', '#5f666f', '#3e444c', '#2a2626', '#1a1414', size=0.82, crest='#3a3e44', seed=81)


def sparrowhawk(f):
    return bird(f, '#8a7a66', '#e8dcc4', '#6e5e4c', '#4a3e32', '#3a3434', '#ffb020', size=0.9, raptor=True, bars=True, seed=91)


def peregrine(f):
    return bird(f, '#4e5a6e', '#e6e2d6', '#3e4858', '#262c38', '#e0b040', '#1a1414', size=1.0, raptor=True, bars=True,
                hood='#6a2a22', seed=101)


def eagle_wing(C, root, L, up, cov, prim, z, fingers=5):
    """a broad soaring wing: straight leading edge, deep fingered tip"""
    rx, ry = root
    if up:
        d = (-0.30, -0.95); p = (-0.95, 0.30)
    else:
        d = (-0.55, 0.83); p = (-0.83, -0.55)
    P = lambda x, y: (rx + d[0] * x * L + p[0] * y * L, ry + d[1] * x * L + p[1] * y * L)
    # the broad inner wing
    body = [P(0, -0.02), P(0.35, -0.06), P(0.66, -0.05), P(0.70, 0.30), P(0.45, 0.42), P(0.18, 0.44), P(-0.04, 0.30)]
    C.plate(body, prim, z=z, bevel=3, tilt=(-0.25, -0.35))
    # the fingers: separate primaries spread at the tip
    for i in range(fingers):
        t = i / (fingers - 1)
        y0 = -0.04 + t * 0.32
        x0 = 0.62 - t * 0.06
        ln = 0.42 - t * 0.12
        ang = -0.12 + t * 0.32
        tipx, tipy = x0 + ln * math.cos(ang), y0 + ln * math.sin(ang)
        w = 0.055
        C.plate([P(x0, y0 - w), P(tipx, tipy - w * 0.4), P(tipx + 0.02, tipy + w * 0.3), P(x0, y0 + w)], prim, z=z + t * 0.4, bevel=1.0)
    # coverts: lighter brown rows over the inner wing
    C.plate([P(-0.02, 0.0), P(0.3, -0.05), P(0.5, -0.03), P(0.52, 0.08), P(0.42, 0.18), P(0.22, 0.22), P(0.04, 0.18)], cov, z=z + 2,
            bevel=5, dome=0.8, tilt=(-0.3, -0.4))
    return P


def storm_eagle(f):
    """A bald eagle the size of a man's torso, with the storm in it."""
    C = Canvas()
    brown = Mat('#4a3424', 8, tex=lambda c: tex_feather(c, 0.9, 111, 3.4))
    cov = Mat('#5a4230', 8, tex=lambda c: tex_feather(c, 1.1, 112, 3.0))
    prim = Mat('#2e2018', 7, tex=lambda c: tex_strands(c, 120, 0.8, 113, 300, 3))
    white = Mat('#ecebe4', 8, tex=lambda c: tex_feather(c, 0.6, 114, 2.6))
    beak = Mat('#f0b830', 7, spec=0.6, gloss=0.6)
    tal = Mat('#e8b830', 6)
    eyem = Mat('#9fe8ff', 5, emit=True, glow=3)
    bolt = Mat('#bfe8ff', 5, emit=True, glow=3,
               tones=[(60, 120, 200), (110, 180, 245), (170, 220, 255), (220, 244, 255), (255, 255, 255)])
    up = f == 0
    cx, cy = 50, 62
    eagle_wing(C, (cx + 6, cy - 8), 46, up, cov, prim, z=-12)
    # white tail fan
    for i in range(5):
        a = 2.95 + (i - 2) * 0.10
        x0, y0 = cx - 14, cy + 4
        C.plate([(x0, y0 - 3), (x0 + math.cos(a) * 20, y0 + math.sin(a) * 20 - 3 + i * 1.6),
                 (x0 + math.cos(a) * 20 - 1, y0 + math.sin(a) * 20 + 2 + i * 1.6), (x0, y0 + 3)], white, z=-2 + i, bevel=1.2)
    # body
    C.ell(cx, cy, 20, 12, 13, brown, rot=-0.22)
    C.ell(cx + 4, cy + 6, 14, 8, 10, brown, z=3, rot=-0.3)
    # white head on a heavy neck
    C.ell(cx + 16, cy - 10, 10, 9, 10, white, z=8)
    C.ell(cx + 21, cy - 13, 9, 8, 10, white, z=10)
    C.tufts([(cx + 10, cy - 4), (cx + 16, cy + 0)], white, z=11, n=4, length=3, width=3, out=(-0.4, 0.9), seed=7)
    # the hooked beak
    hx, hy = cx + 27, cy - 13
    C.plate([(hx - 2, hy - 4), (hx + 7, hy - 3), (hx + 11, hy + 1), (hx + 9, hy + 6), (hx + 7, hy + 3), (hx - 2, hy + 3)], beak, z=18, bevel=1.6)
    C.dot(hx + 3, hy + 1, (60, 40, 20)); C.dot(hx + 4, hy + 1, (60, 40, 20))
    # the brow that makes the glare
    C.plate([(hx - 9, hy - 7), (hx - 1, hy - 6), (hx - 2, hy - 3), (hx - 9, hy - 4)], white, z=20, bevel=1, tilt=(-0.4, -0.7))
    eye(C, hx - 5, hy - 2.5, 1.8, eyem)
    # talons hanging forward
    for (x, z) in ((cx + 2, 6), (cx - 4, 2)):
        C.limb([(x, cy + 10, 3.2), (x + 3, cy + 20, 2.4)], white, z=z)
        C.limb([(x + 3, cy + 20, 1.8), (x + 4, cy + 26, 1.6)], tal, z=z + 1)
        for i in range(3):
            C.limb([(x + 4, cy + 26, 1.0, z + 2), (x + 2 + i * 2.4, cy + 29, 0.7, z + 2)], Mat('#1a1414', 4))
    # near wing, and the storm along its edge
    P = eagle_wing(C, (cx + 4, cy - 4), 52, up, cov, prim, z=20)
    pts = [P(0.15, 0.1), P(0.28, 0.02), P(0.36, 0.14), P(0.5, 0.05), P(0.58, 0.16), P(0.72, 0.08)]
    for i in range(len(pts) - 1):
        C.limb([(pts[i][0], pts[i][1], 0.8, 40), (pts[i + 1][0], pts[i + 1][1], 0.8, 40)], bolt)
    return C


# ============================================================== golems
def golem(f, stone, accent, glowc, kind='mite', seed=12):
    C = Canvas()
    st = Mat(stone, 8, tex=lambda c: tex_stone(c, 1.2, seed, 6.0))
    dk = Mat(stone, 8, tex=lambda c: tex_stone(c, 1.0, seed + 1, 5.0), dark=0.85, light=0.3)
    gl = Mat(glowc, 6, emit=True, glow=3)
    s = stride(f, 1.5)
    if kind == 'mite':
        # a fist sized beetle of rock: four stubby legs and one eye
        for (x, z) in ((36, -8), (58, -8)):
            C.limb([(x, 74, 4.5, z), (x - 3 - s, GROUND - 3, 3.6, z)], dk)
        C.ell(48, 68, 26, 18, 18, st)
        C.ell(42, 56, 17, 10, 12, st, z=8)
        C.plate([(30, 62), (40, 50), (52, 52), (46, 64)], dk, z=18, bevel=2)
        C.plate([(52, 54), (62, 50), (68, 60), (58, 66)], st, z=16, bevel=2)
        mo = Mat('#5e8a2e', 6, tex=lambda c: (vnoise(c.X, c.Y, 0.7, 41) - 0.5) * 3)
        C.ell(40, 56, 9, 3, 4, mo, z=22, rot=-0.2)
        C.ball(68, 70, 6.5, dk, z=10)
        C.ball(71, 69, 3.4, gl, z=20)
        C.dot(70, 67, (255, 255, 230))
        for (x, z) in ((40, 14), (62, 14)):
            C.limb([(x, 76, 5, z), (x + 2 + s, GROUND - 3, 3.8, z)], st)
            C.ell(x + 3 + s, GROUND - 1.5, 4.5, 2.2, 3, dk, z=z + 2)
        # glowing seams
        for (x0, y0, x1, y1) in [(34, 70, 44, 74), (44, 74, 54, 72), (54, 72, 60, 78)]:
            C.limb([(x0, y0, 0.7, 30), (x1, y1, 0.7, 30)], gl)
        return C
    # upright golems: copper automaton, quartz titan
    big = kind == 'titan'
    met = kind == 'copper'
    if met:
        st = Mat(stone, 8, tex=lambda c: tex_metal(c, 1.0, seed) + (vnoise(c.X, c.Y, 0.35, seed + 5) > 0.68) * 0.0,
                 spec=0.7, gloss=0.6)
        dk = Mat(stone, 8, tex=lambda c: tex_metal(c, 0.8, seed + 1), dark=0.85, light=0.35, spec=0.4)
        verd = Mat('#4fa38a', 6, tex=lambda c: (vnoise(c.X, c.Y, 0.6, 7) - 0.5) * 2.5)
    cx = 48
    # far arm
    C.limb([(cx + 14, 42, 6, -8), (cx + 20, 58 + s, 5, -8), (cx + 18, 70 + s, 6, -8)], dk)
    C.ball(cx + 18, 72 + s, 8, dk, z=-6)
    # legs
    C.limb([(cx - 8, 66, 7, -4), (cx - 10 - s, GROUND - 4, 6, -4)], dk)
    C.ell(cx - 9 - s, GROUND - 2, 8, 3.5, 5, dk, z=-2)
    # torso: wide shoulders, small head set low
    C.ell(cx, 50, 22 if big else 19, 18, 18, st)
    C.ell(cx - 2, 64, 13, 9, 12, dk, z=2)
    C.ell(cx + 2, 32, 10, 8, 10, st, z=6)
    C.plate([(cx - 6, 28), (cx + 10, 26), (cx + 12, 34), (cx - 4, 36)], dk, z=14, bevel=2)
    C.ball(cx + 6, 31, 2.2, gl, z=24)
    C.dot(cx + 5, 30, (255, 255, 230))
    # core
    C.ball(cx + 2, 50, 6, dk, z=18)
    C.ball(cx + 2, 50, 3.8, gl, z=24)
    if met:
        C.ell(cx, 48, 21, 15, 18, st, z=2)
        C.plate([(cx - 6, 28), (cx + 12, 26), (cx + 13, 36), (cx - 5, 37)], dk, z=20, bevel=2)
        for x in range(int(cx - 2), int(cx + 11)):
            C.dot(x, 31, (255, 200, 90))
        C.plate([(cx + 8, 34), (cx + 24, 32), (cx + 28, 44), (cx + 12, 46)], st, z=-2, bevel=3, tilt=(-0.2, -0.5))
        for (x, y) in [(cx - 10, 44), (cx - 12, 52), (cx + 12, 42), (cx + 14, 54), (cx - 4, 60), (cx + 8, 60)]:
            C.ball(x, y, 1.5, dk, z=24)
        C.ell(cx - 8, 40, 7, 4, 5, verd, z=22, rot=0.4)
        C.ell(cx + 10, 62, 5, 3, 4, verd, z=20)
        for (x0, y0, x1, y1) in [(cx - 14, 50, cx - 6, 50), (cx + 8, 46, cx + 16, 48)]:
            C.limb([(x0, y0, 0.7, 30), (x1, y1, 0.7, 30)], gl)
    if big:
        q = Mat('#d8c8ff', 7, tex=lambda c: tex_crystal(c, 1.2, seed), spec=0.9, gloss=0.8)
        qg = Mat('#c9a8ff', 6, emit=True, glow=3)
        for (x, y, h, w, a) in [(cx - 14, 36, 18, 4.5, -0.5), (cx - 6, 32, 24, 5.5, -0.15), (cx + 4, 34, 16, 4, 0.25),
                                (cx - 20, 44, 12, 3.5, -0.9)]:
            ca, sa = math.cos(a - math.pi / 2), math.sin(a - math.pi / 2)
            tx, ty = x + ca * h, y + sa * h
            px, py = -sa * w, ca * w
            C.plate([(x - px, y - py), (tx - px * 0.2, ty - py * 0.2), (tx + px * 0.3, ty + py * 0.3), (x + px, y + py)],
                    q, z=26, bevel=2, tilt=(-0.5, -0.3))
        C.ball(cx - 6, 30, 3, qg, z=30)
    # near leg
    C.limb([(cx + 6, 66, 7.5, 12), (cx + 8 + s, GROUND - 4, 6.5, 12)], st)
    C.ell(cx + 9 + s, GROUND - 2, 9, 3.6, 5, st, z=14)
    # near arm, heavy fist hanging past the knee
    C.limb([(cx - 16, 40, 7, 20), (cx - 22, 56 - s, 5.5, 20), (cx - 20, 68 - s, 6, 20)], st)
    C.ball(cx - 20, 72 - s, 9, st, z=22)
    C.plate([(cx - 30, 30), (cx - 8, 27), (cx - 6, 40), (cx - 28, 44)], dk if not met else st, z=24, bevel=3,
            tilt=(-0.3, -0.5))
    if met:
        for (x, y) in [(cx - 24, 33), (cx - 13, 31), (cx - 20, 39)]:
            C.ball(x, y, 1.4, dk, z=30)
    return C


def pebble_mite(f):
    return golem(f, '#7a7a80', '#5e8a2e', '#7ae8ff', 'mite', seed=121)


def copper_golem(f):
    return golem(f, '#b4713a', '#4fa38a', '#ffb84a', 'copper', seed=131)


def facet(C, pts, mat, z, light=0):
    """one flat crystal face: the tilt picks which way it catches light"""
    tilts = [(-0.45, -0.45), (-0.1, -0.25), (0.35, -0.05), (0.55, 0.45), (-0.35, 0.15)]
    C.plate(pts, mat, z=z, bevel=1.0, tilt=tilts[light % len(tilts)])


def quartz_titan(f):
    """A walking geode: slate joints, a body of blue quartz cut into flat
       faces, a cold core, and shards breaking out of the shoulders."""
    C = Canvas()
    qz = Mat('#3f8fd8', 8, spec=0.25, gloss=0.9, light=0.5, sat=1.1)
    qd = Mat('#2a5a9a', 8, spec=0.15, gloss=0.6, sat=1.1)
    sl = Mat('#3e4656', 7, tex=lambda c: tex_stone(c, 1.0, 141, 5.0))
    core = Mat('#bff0ff', 6, emit=True, glow=4,
               tones=[(40, 120, 200), (80, 170, 240), (140, 214, 255), (196, 238, 255), (230, 250, 255), (255, 255, 255)])
    s = stride(f, 1.4)
    cx = 48
    # far arm and leg in slate and dark quartz
    C.limb([(cx + 14, 40, 5, -10), (cx + 19, 56 + s, 4, -10)], sl)
    facet(C, [(cx + 13, 56 + s), (cx + 25, 54 + s), (cx + 27, 70 + s), (cx + 15, 72 + s)], qd, -8, 2)
    C.limb([(cx - 6, 66, 4, -6), (cx - 8 - s, GROUND - 6, 3.6, -6)], sl)
    facet(C, [(cx - 15 - s, GROUND - 9), (cx - 2 - s, GROUND - 9), (cx - 1 - s, GROUND), (cx - 16 - s, GROUND)], qd, -4, 3)
    # pelvis
    C.ell(cx, 64, 12, 7, 8, sl)
    # torso: a cut gem, broad at the shoulder, narrow at the waist
    facet(C, [(cx - 20, 36), (cx + 18, 34), (cx + 12, 62), (cx - 12, 62)], qd, 4, 3)
    facet(C, [(cx - 20, 36), (cx - 4, 33), (cx - 2, 48), (cx - 16, 52)], qz, 10, 0)
    facet(C, [(cx - 4, 33), (cx + 18, 34), (cx + 12, 46), (cx - 2, 48)], qz, 10, 1)
    facet(C, [(cx - 16, 52), (cx - 2, 48), (cx + 2, 62), (cx - 12, 62)], qz, 9, 4)
    facet(C, [(cx - 2, 48), (cx + 12, 46), (cx + 12, 62), (cx + 2, 62)], qd, 9, 2)
    # the core, sunk in the chest
    C.ball(cx - 1, 46, 5.4, sl, z=14)
    C.ball(cx - 1, 46, 3.8, core, z=20)
    C.dot(cx - 2.5, 44.5, (255, 255, 255))
    # head: small, low, a slate wedge with one slit of light
    C.ell(cx + 2, 28, 8, 6, 8, sl, z=12)
    facet(C, [(cx - 6, 24), (cx + 9, 22), (cx + 11, 28), (cx - 5, 30)], qz, 16, 0)
    for x in range(int(cx + 1), int(cx + 9)):
        C.dot(x, 27, (200, 244, 255))
    # shards breaking out of the shoulders and back
    for (x, y, h, w, a, li) in [(cx - 18, 36, 20, 4.5, -0.55, 0), (cx - 9, 33, 26, 5.0, -0.18, 1),
                                (cx + 2, 33, 16, 3.6, 0.15, 0), (cx + 13, 35, 12, 3.2, 0.5, 1),
                                (cx - 24, 44, 11, 3.0, -1.0, 4)]:
        ca, sa = math.cos(a - math.pi / 2), math.sin(a - math.pi / 2)
        tx, ty = x + ca * h, y + sa * h
        px, py = -sa * w, ca * w
        facet(C, [(x - px, y - py), (tx, ty), (x + px * 0.1, y + py * 0.1)], qz, 22, li)
        facet(C, [(x + px * 0.1, y + py * 0.1), (tx, ty), (x + px, y + py)], qd, 22, li + 2)
    # near leg
    C.limb([(cx + 6, 66, 4.4, 12), (cx + 8 + s, GROUND - 6, 4, 12)], sl)
    facet(C, [(cx + 1 + s, GROUND - 10), (cx + 16 + s, GROUND - 10), (cx + 18 + s, GROUND), (cx + s, GROUND)], qz, 14, 1)
    # near arm: slate upper, a club of quartz for a forearm
    C.limb([(cx - 16, 40, 6, 20), (cx - 22, 52 - s, 5, 20)], sl)
    facet(C, [(cx - 28, 54 - s), (cx - 20, 51 - s), (cx - 21, 74 - s), (cx - 29, 68 - s)], qz, 24, 0)
    facet(C, [(cx - 20, 51 - s), (cx - 14, 54 - s), (cx - 15, 70 - s), (cx - 21, 74 - s)], qd, 24, 3)
    facet(C, [(cx - 29, 33), (cx - 19, 30), (cx - 19, 42), (cx - 27, 43)], qz, 26, 0)
    facet(C, [(cx - 19, 30), (cx - 11, 32), (cx - 12, 41), (cx - 19, 42)], qd, 26, 2)
    return C


# ============================================================== drakes
def drake(f, scale, belly, membrane, horn, eyec, fire=False, seed=13):
    C = Canvas()
    sc = Mat(scale, 8, tex=lambda c: tex_scale(c, 1.0, seed, 3.0))
    bl = Mat(belly, 7, tex=lambda c: (np.sin(c.Y * 1.3) > 0.55) * -1.4)
    mb = Mat(membrane, 7, tex=lambda c: (vnoise(c.X, c.Y, 0.3, seed) - 0.5) * 1.4)
    hn = Mat(horn, 6, spec=0.6, gloss=0.5)
    ey = Mat(eyec, 5, emit=True, glow=2.5)
    up = f == 0
    cx, cy = 44, 58

    def dwing(z, dx, raise_):
        root = (cx + 4 + dx, cy - 6)
        if raise_:
            tips = [(cx - 26 + dx, cy - 44), (cx - 34 + dx, cy - 30), (cx - 36 + dx, cy - 14)]
            arm = (cx - 8 + dx, cy - 40)
        else:
            tips = [(cx - 30 + dx, cy + 18), (cx - 36 + dx, cy + 8), (cx - 34 + dx, cy - 4)]
            arm = (cx - 14 + dx, cy + 6)
        poly = [root, arm]
        prev = arm
        for i, t in enumerate(tips):
            if i:
                a0 = tips[i - 1]
                mx, my = (a0[0] + t[0]) / 2, (a0[1] + t[1]) / 2
                poly.append((mx + (arm[0] - mx) * 0.28, my + (arm[1] - my) * 0.28))
            poly.append(t)
        end = (cx - 6 + dx, cy + 4)
        mx, my = (tips[-1][0] + end[0]) / 2, (tips[-1][1] + end[1]) / 2
        poly += [(mx + (arm[0] - mx) * 0.25, my + (arm[1] - my) * 0.25), end]
        C.plate(poly, mb, z=z, bevel=2.5, tilt=(-0.3, -0.4))
        C.limb([(root[0], root[1], 2.6, z + 3), (arm[0], arm[1], 2.0, z + 3)], sc)
        for t in tips:
            C.limb([(arm[0], arm[1], 1.8, z + 3), (t[0], t[1], 0.9, z + 3)], sc)
        C.plate([(arm[0] - 1, arm[1]), (arm[0] + 1, arm[1] - 6), (arm[0] + 3, arm[1])], hn, z=z + 5, bevel=1)

    dwing(-10, 6, up)
    # tail curling back
    C.limb([(cx - 12, cy + 8, 7), (cx - 26, cy + 14, 5), (cx - 36, cy + 8, 3.5), (cx - 40, cy - 2, 2.2)], sc, z=-2)
    C.plate([(cx - 42, cy - 1), (cx - 46, cy - 10), (cx - 37, cy - 4)], hn, z=0, bevel=1.2)
    # far legs
    C.limb([(cx + 10, cy + 12, 6, -6), (cx + 14, cy + 24, 4.4, -6), (cx + 12, GROUND - 2, 3.6, -6)], sc)
    # body
    C.ell(cx - 2, cy + 7, 21, 14, 15, sc, rot=-0.15)
    C.ell(cx + 4, cy + 12, 14, 6, 10, bl, z=6, rot=-0.2)
    # neck, s curve to a horned head
    C.limb([(cx + 12, cy - 2, 9), (cx + 20, cy - 12, 7), (cx + 24, cy - 22, 5.6)], sc, z=6)
    C.limb([(cx + 14, cy + 2, 4.5), (cx + 22, cy - 10, 3.4)], bl, z=10)
    hx, hy = cx + 30, cy - 26
    C.ell(hx, hy, 9, 6.5, 8, sc, z=12, rot=0.1)
    C.ell(hx + 9, hy + 2, 7, 4, 6, sc, z=14, rot=0.2)
    C.ell(hx + 8, hy + 5, 6, 2, 4, bl, z=15, rot=0.2)
    C.dot(hx + 14, hy + 1, (20, 12, 12))
    for (a, b, c) in [((hx - 4, hy - 4), (hx - 14, hy - 14), (hx - 1, hy - 6)), ((hx, hy - 5), (hx - 6, hy - 16), (hx + 3, hy - 6))]:
        C.plate([a, b, c], hn, z=16, bevel=1.4, tilt=(-0.4, -0.4))
    C.ell(hx + 3, hy - 3, 4, 1.6, 3, sc, z=20, rot=-0.2)
    eye(C, hx + 4, hy - 1, 1.8, ey, slit=True)
    # spines down the back
    C.tufts([(cx + 22, cy - 20), (cx + 14, cy - 6), (cx - 2, cy - 4), (cx - 20, cy + 6), (cx - 34, cy + 6)], hn, z=8, n=9,
            length=4, width=3, out=(-0.2, -1), seed=seed)
    if fire:
        fm = Mat('#ff8a1e', 6, emit=True, glow=3,
                 tones=[(140, 30, 10), (210, 70, 14), (245, 120, 24), (255, 170, 60), (255, 220, 130), (255, 248, 220)])
        C.ell(cx + 4, cy + 12, 10, 3, 8, fm, z=12, rot=-0.2)
        C.ball(hx + 15, hy + 4, 2.2, fm, z=20)
        C.ball(hx + 18, hy + 2, 1.6, fm, z=20)
    else:
        ice = Mat('#d8f6ff', 6, spec=0.9, gloss=0.9, tex=lambda c: tex_crystal(c, 1.0, seed))
        for (x, y, h) in [(cx - 6, cy - 4, 9), (cx + 4, cy - 6, 7), (cx - 16, cy + 2, 6)]:
            C.plate([(x - 2.5, y + 1), (x - 1, y - h), (x + 2.5, y + 1)], ice, z=22, bevel=1.4, tilt=(-0.5, -0.4))
        C.ball(hx + 16, hy + 2, 1.6, Mat('#eaffff', 4, emit=True, glow=2), z=22)
    # near legs
    C.ell(cx - 8, cy + 14, 10, 9, 10, sc, z=12)
    C.limb([(cx - 8, cy + 16, 6.5, 14), (cx - 14, cy + 26, 4.6, 14), (cx - 7, GROUND - 2, 3.8, 15)], sc)
    C.limb([(cx + 12, cy + 12, 6, 16), (cx + 17, cy + 23, 4.2, 16), (cx + 18, GROUND - 2, 3.6, 17)], sc)
    for x in (cx - 6, cx + 18):
        for i in range(3):
            C.ell(x + i * 1.6 + 1, GROUND - 0.6, 1.2, 0.8, 1, hn, z=20)
    dwing(24, 0, up)
    return C


def frost_wyrmling(f):
    return drake(f, '#5a9cc8', '#cfe8f0', '#8fc4e0', '#e8f4ff', '#bff4ff', fire=False, seed=151)


def cinder_drake(f):
    return drake(f, '#7a2a1e', '#e8a060', '#c4482a', '#2a1a16', '#ffd84a', fire=True, seed=161)


BUILD = [
    ('Trail Mutt', trail_mutt), ('Brindle Pup', brindle_pup), ('Bog Frog', bog_frog),
    ('Mossback Toad', mossback_toad), ('Gray Jay', gray_jay), ('Sparrowhawk', sparrowhawk),
    ('Pebble Mite', pebble_mite), ('Ridge Hound', ridge_hound), ('Copper Golem', copper_golem),
    ('Peregrine', peregrine), ('Emberfrog', emberfrog), ('Quartz Titan', quartz_titan),
    ('Storm Eagle', storm_eagle), ('Frost Wyrmling', frost_wyrmling), ('Cinder Drake', cinder_drake),
]
