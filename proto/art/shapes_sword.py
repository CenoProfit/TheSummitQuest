# -*- coding: utf-8 -*-
"""Eight blades. All of them run lower-left to upper-right so the tip
   lands in the corner and the hilt fills the opposite one."""
from pixlib import *
import math

U = (0.7071, -0.7071)      # along the blade
P = (0.7071,  0.7071)      # across it

def along(B, t):  return (B[0] + U[0]*t, B[1] + U[1]*t)
def across(B, t): return (B[0] + P[0]*t, B[1] + P[1]*t)

def hilt(g, B, grip=12, pom=3.4, bands=4, pomshape='disc', stone=True):
    """Grip, ferrule and pommel. The binding is a criss-cross, which is
       what a wrapped hilt actually looks like, and the pommel carries a
       cut stone, which is where the eye lands on a weapon icon."""
    # The grip starts almost at B. Starting it two units down the axis
    # left room for a guard that sits forward of B (a curved quillon,
    # say) to lift clear of it, and the hilt came apart.
    a = along(B, -1.0); b = along(B, -grip)
    haft(g, a[0], a[1], b[0], b[1], 5)
    cordwrap(g, a[0], a[1], b[0], b[1], 5, bands + 3)
    f = along(B, -3)
    taper(g, across(f, -3.2)[0], across(f, -3.2)[1],
             across(f, 3.2)[0], across(f, 3.2)[1], 3.0, 3.0, 'C')
    p = along(B, -(grip + 3.5))
    if pomshape == 'disc':
        disc(g, p[0], p[1], pom + 0.6, 'c'); disc(g, p[0], p[1], pom, 'C')
    else:
        poly(g, [across(p, -pom), along(p, -pom), across(p, pom), along(p, pom)], 'C')
    if stone: gem(g, p[0], p[1], pom * 0.62, 'A', 5)
    else: put(g, p[0] - 1, p[1] - 1, 'Z')

def quillons(g, B, half=8, thick=4.2, knuckle=2.1, curve=0.0, langet=True):
    l = across(B, -half); r = across(B, half)
    if curve:
        l = (l[0] + U[0]*curve, l[1] + U[1]*curve)
        r = (r[0] + U[0]*curve, r[1] + U[1]*curve)
    taper(g, l[0], l[1], r[0], r[1], thick, thick, 'C')
    if langet:                       # the tongue of brass up onto the blade
        t = along(B, 5)
        taper(g, B[0], B[1], t[0], t[1], thick * 0.72, thick * 0.34, 'C')
    if knuckle:
        stud(g, l[0], l[1], knuckle); stud(g, r[0], r[1], knuckle)
    line_on(g, l[0], l[1]-1, r[0], r[1]-1, 'Z', 'C')
    line_on(g, l[0], l[1]+1.4, r[0], r[1]+1.4, 'x', 'C')

def wavy(g, B, T, amp=2.6, n=6):
    """bite alternating scallops out of both edges of a finished blade"""
    L = math.hypot(T[0]-B[0], T[1]-B[1])
    for i in range(n):
        t = 6 + (L - 12) * (i + 0.5) / n
        c = along(B, t)
        s = 1 if i % 2 else -1
        disc(g, c[0] + P[0]*s*amp*1.9, c[1] + P[1]*s*amp*1.9, amp, '.')

def chip(g, pt, r):
    disc(g, pt[0], pt[1], r, '.')

# ------------------------------------------------------------------ 0..7
def s_arming():
    g = blank(); B = (21, 43); T = (55, 9)
    hilt(g, B)
    blade(g, B[0], B[1], T[0], T[1], 9, 2.0, 7)
    fuller(g, B[0], B[1], T[0], T[1])
    etch(g, B[0], B[1], T[0], T[1], 4)
    glint(g, B[0], B[1], T[0], T[1], 0.58, 2.6)
    quillons(g, B)
    return g

def s_falchion():
    g = blank(); B = (20, 45)
    # the knuckle bow is cut out BEFORE the grip is laid in; cutting it
    # afterwards took the grip with it, and with no grip material left
    # the engine could not work out where the thing is held
    poly(g, [(14, 44), (10, 50), (16, 55), (22, 52)], 'C')
    poly(g, [(16, 46), (13, 50), (17, 53), (21, 51)], '.')
    hilt(g, B, 11, 3.0, 3)
    # a belly that widens toward the point, built from three segments
    taper(g, B[0], B[1], 36, 29, 8, 11, 'A')
    taper(g, 36, 29, 48, 17, 11, 12, 'A')
    poly(g, [(44, 12), (57, 8), (52, 20), (42, 22)], 'A')      # clipped point
    g = shadeform(g)
    line_on(g, B[0]+3, B[1]-5, 55, 9, 'W', 'A')
    line_on(g, B[0]+6, B[1]-1, 50, 20, 'd', 'A')
    quillons(g, B, 7, 4.0, 2.0)
    return g

def s_great():
    g = blank(); B = (18, 47); T = (58, 6)
    hilt(g, B, 17, 4.2, 6)
    blade(g, B[0], B[1], T[0], T[1], 12, 2.4, 9)
    fuller(g, B[0], B[1], T[0], T[1])
    etch(g, B[0], B[1], T[0], T[1], 6)
    glint(g, B[0], B[1], T[0], T[1], 0.55, 3.2)
    r = along(B, 5)                                             # ricasso
    taper(g, B[0], B[1], r[0], r[1], 7, 7, 'G')
    quillons(g, B, 12, 4.6, 2.6)
    return g

def s_flamberge():
    g = blank(); B = (21, 44); T = (55, 10)
    hilt(g, B, 12, 3.2, 4)
    blade(g, B[0], B[1], T[0], T[1], 10, 2.2, 7)
    wavy(g, B, T)
    glint(g, B[0], B[1], T[0], T[1], 0.62, 2.4)
    g = shadeform(g)
    line_on(g, B[0]+2, B[1]-4, T[0]-3, T[1]+3, 'W', 'A')
    quillons(g, B, 9, 4.0, 2.2, curve=1.0)
    return g

def s_rapier():
    g = blank(); B = (20, 46); T = (57, 8)
    hilt(g, B, 13, 2.8, 5)
    blade(g, B[0], B[1], T[0], T[1], 4.4, 1.6, 9)
    glint(g, B[0], B[1], T[0], T[1], 0.55, 1.4)
    # swept basket of brass curves around the grip
    for k in (1, -1):
        for r in (7.5, 11.0):
            a = across(B, k * r); b = along(B, -11)
            line(g, a[0], a[1], b[0] + P[0]*k*2.5, b[1] + P[1]*k*2.5, 'C', 2)
    ring(g, B[0] - U[0]*5, B[1] - U[1]*5, 8.5, 2.5, 'C')
    quillons(g, B, 10, 3.2, 2.0)
    return g

def s_cleaver():
    """The blade used to start seven units up the axis from the hilt,
       which left a clear gap between the ferrule and the bolster and
       the cleaver read as a blade floating above a handle. It is
       translated back onto the hilt, and its front edge extended by the
       same amount so the tip still reaches the corner."""
    g = blank(); B = (18, 48)
    hilt(g, B, 13, 3.0, 3)
    poly(g, [(16, 50), (26, 60), (56, 30), (46, 20), (25, 41)], 'A')
    g = shadeform(g)
    line_on(g, 46, 19, 56, 29, 'W', 'A')                        # the edge
    line_on(g, 19, 49, 29, 59, 'd', 'A')
    taper(g, 16, 50, 26, 60, 4.0, 4.0, 'C')                     # bolster
    return g

def s_katana():
    g = blank(); B = (19, 48)
    hilt(g, B, 16, 0, 7, stone=False)
    pts = [(B[0] + 38*(i/10)**1.0, B[1] - 40*(i/10) + 5*math.sin(math.pi*i/10)) for i in range(11)]
    for i in range(len(pts)-1):
        taper(g, pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1],
              6.5 - i*0.25, 6.2 - i*0.25, 'A')
    poly(g, [(pts[-1][0]-4, pts[-1][1]+4), (60, 6), (pts[-1][0]+3, pts[-1][1]+1)], 'A')
    g = shadeform(g)
    for i in range(len(pts)-1):
        line_on(g, pts[i][0]+2, pts[i][1]-2.4, pts[i+1][0]+2, pts[i+1][1]-2.4, 'W', 'A')
    ring(g, B[0], B[1], 7.0, 2.8, 'C'); disc(g, B[0], B[1], 4.6, 'C')   # tsuba
    for i in range(6):
        import math as _m
        a = i * _m.pi / 3
        disc(g, B[0] + _m.cos(a) * 4.6, B[1] + _m.sin(a) * 4.6, 1.0, 'x')
    p = along(B, -17.5); poly(g, [across(p,-3.4), along(p,-3.4), across(p,3.4), along(p,3.4)], 'C')
    return g

def s_broken():
    g = blank(); B = (21, 44)
    hilt(g, B, 12, 3.2, 3)
    blade(g, B[0], B[1], 42, 23, 10.5, 7.5, 0)
    etch(g, B[0], B[1], 42, 23, 3, 0.22)
    # the snapped end, bitten into a jagged edge
    for k, r in ((-4.0, 3.2), (0.0, 4.0), (4.5, 3.0)):
        c = across(along(B, 23), k)
        chip(g, (c[0] + U[0]*2.5, c[1] + U[1]*2.5), r)
    for k, r in ((-6.0, 2.2), (7.0, 2.6), (2.0, 1.8)):
        chip(g, across(along(B, 10 + abs(k)), k), r)
    g = shadeform(g)
    line_on(g, B[0]+2, B[1]-4, 40, 24, 'W', 'A')
    quillons(g, B, 8, 4.0, 0)
    return g

SHAPES = [dump(paint(f())) for f in
          (s_arming, s_falchion, s_great, s_flamberge, s_rapier, s_cleaver, s_katana, s_broken)]
