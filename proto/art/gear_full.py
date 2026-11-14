# -*- coding: utf-8 -*-
"""Full colour gear, one design per shape, coloured per piece.

The letter sprites made 100 pieces out of 38 shapes by swapping a
palette. This keeps that economy (the same shape numbers, the same
materials from PAL in trek.html) but each piece is rendered by forge.py
with its own colours, and the rarity changes the build, not just the
tint: a common blade is plain and nicked, a rare one carries a fuller
and a gem, an epic one filigree and runes, a legendary one light.

    piece(g) -> Canvas, where g is the GEAR row from trek.html
"""
import math, os, re
from forge import *

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = open(os.path.join(os.path.dirname(HERE), 'trek.html')).read()


def _block(a, b):
    i = HTML.index(a); return HTML[i:HTML.index(b, i) + len(b)]


PAL = {m.group(1): [m.group(2), m.group(3), m.group(4)]
       for m in re.finditer(r"(\w+):\['(#\w+)','(#\w+)','(#\w+)'\]", _block('const PAL={', '};'))}
GEAR = [[m.group(2), m.group(3), int(m.group(4)), int(m.group(5))] + [m.group(i) for i in range(6, 10)]
        for m in re.finditer(r"\[(['\"])(.*?)\1,'(\w+)',(\d),(\d+),'(\w+)','(\w+)','(\w+)','(\w+)'\]",
                             _block('const GEAR=[', "leather']];"))]


def gid(g):
    return g[1][0] + re.sub(r'[^a-z0-9]', '', g[0].lower())


GLOW = {'sun': ('#ffd060', [(200, 90, 20), (240, 140, 30), (255, 190, 60), (255, 222, 120), (255, 244, 200), (255, 255, 245)]),
        'ember': ('#ff8a1e', [(150, 30, 10), (215, 70, 14), (245, 120, 24), (255, 170, 60), (255, 220, 130), (255, 248, 220)]),
        'void': ('#b070ff', [(60, 20, 110), (100, 40, 170), (150, 80, 230), (190, 130, 250), (226, 190, 255), (250, 240, 255)]),
        'frost': ('#9fe8ff', [(40, 110, 170), (80, 160, 220), (130, 205, 245), (180, 232, 255), (225, 248, 255), (255, 255, 255)]),
        'sea': ('#6ff0d8', [(20, 100, 110), (40, 150, 150), (80, 200, 190), (140, 235, 220), (200, 250, 240), (245, 255, 252)]),
        'storm': ('#bfe8ff', [(60, 110, 200), (100, 160, 240), (160, 210, 255), (210, 236, 255), (240, 250, 255), (255, 255, 255)]),
        'venom': ('#a8ff5a', [(40, 100, 20), (70, 150, 30), (120, 200, 50), (170, 235, 90), (215, 250, 160), (245, 255, 230)]),
        'mithril': ('#bff0ff', [(60, 130, 190), (100, 180, 230), (150, 215, 250), (200, 240, 255), (235, 250, 255), (255, 255, 255)])}


class Kit:
    """the materials one piece is made of"""
    def __init__(self, g):
        self.g = g
        A, B, C = PAL[g[4]]
        G0, G1, _ = PAL.get(g[5], PAL['leather'])
        self.rar = g[2]
        wood = g[4] in ('wood', 'leather', 'moss') and g[6] != 'metal'
        self.soft = g[6] in ('cloth', 'leather', 'fur')
        if self.soft and g[1] in ('helm', 'chest', 'shoes'):
            self.body = Mat(A, 8, tex=lambda c: (np.sin(c.X * 1.6) * np.sin(c.Y * 1.6) > 0.55) * -0.9 +
                            (vnoise(c.X, c.Y, 0.3, 4) - 0.5) * 1.2, light=0.5)
        elif wood:
            self.body = Mat(A, 8, tex=lambda c: tex_bark(c, 1.0, 3))
        else:
            self.body = Mat(B, 8, spec=0.55, gloss=0.6, tex=lambda c: tex_metal(c, 0.7, 5), dark=0.82, light=0.62)
        self.dark = Mat(A, 7, spec=0.2, dark=0.85)
        self.edge = Mat(_lite(B, 0.45), 6, spec=0.8, gloss=0.8)
        self.acc = Mat(C, 7, spec=0.8, gloss=0.8)
        self.grip = Mat(G0, 7, tex=lambda c: (np.sin((c.X + c.Y) * 1.25) > 0.35) * -1.6 + (np.sin((c.X - c.Y) * 1.25) > 0.6) * 0.8)
        self.wood = Mat(G0, 7, tex=lambda c: tex_bark(c, 0.9, 7))
        key = g[4] if g[4] in GLOW else None
        self.glow = None
        if key and (self.rar >= 2 or 'arcane' in (g[6], g[7])):
            self.glow = Mat(GLOW[key][0], 6, emit=True, glow=3, tones=GLOW[key][1])
        elif 'arcane' in (g[6], g[7]):
            self.glow = Mat('#7ae8c0', 6, emit=True, glow=2,
                            tones=[(20, 100, 70), (40, 150, 110), (80, 200, 150), (140, 235, 195), (200, 250, 230), (245, 255, 250)])
        self.gem = self.glow or Mat('#c03040', 6, spec=0.9, gloss=0.9)
        self.v = dict(VARIANT.get(g[0], {}))
        self.v.setdefault('len', 1.0); self.v.setdefault('wid', 1.0)
        self.v.setdefault('nicks', 2 if self.rar == 0 else 0)


def _lite(h, t):
    c = hexc(h); return tuple(int(v + (255 - v) * t) for v in c)


# ============================================================ variety
# per piece: what makes two commons of the same shape different things
VARIANT = {
    # swords
    'Notched Shortsword': dict(len=0.8, wid=1.15, nicks=4, pommel='ball'),
    'Militia Arming Blade': dict(len=1.05, wid=0.95, nicks=0, pommel='fish', wrap='#7a2a24'),
    'Carved Oak Waster': dict(len=0.95, wid=1.3, nicks=0, guardk='disc', pommel='ball'),
    "Hunter's Falchion": dict(wrap='#d8c8a8', pommel='spike', guard=0.7),
    "Scavenger's Saber": dict(wrap='#5a2a30', pommel='ring', tassel='#a83a2a', nicks=2),
    'Tin Cutter': dict(len=0.8, wid=1.6, guard=0.8, pommel='ball'),
    "Poacher's Dirk": dict(len=0.62, wid=1.8, guardk='none', pommel='ring', wrap='#3a4a2a'),
    "Bandit's Shiv": dict(len=0.55, wid=1.6, guardk='none', pommel='spike', wrap='#8a7a6a', tassel='#3a3a44'),
    'Ridge Cleaver': dict(pommel='ring', wrap='#4a3a30'),
    "Woodcutter's Seax": dict(len=1.1, wid=0.8, pommel='fish', guard=0.6, wrap='#6a4a2a'),
    'Steel Longsword': dict(len=1.12, grip=1.3, pommel='fish', wrap='#2a3048'),
    'Ironwood Backsword': dict(pommel='spike', wrap='#5a3a22', tassel='#2a5a3a'),
    'Rusted Gladius': dict(guardk='disc', pommel='ball'),
    # shields
    'Bark Buckler': dict(face='bark'), 'Hide Targe': dict(face='hide', paint='stripe'),
    'Wicker Guard': dict(face='weave'), 'Tin Roundshield': dict(paint='quarters', dents=True),
    'Cobbled Boss': dict(face='patch'), 'Militia Kite': dict(paint='halves'),
    'Scrap Heater': dict(face='patch', paint='none'), 'Steel Kite Shield': dict(paint='bands'),
    'Strapped Planks': dict(straps=True),
    # helms
    'Woolen Hood': dict(hood='knit'), 'Leather Coif': dict(hood='coif'), "Ranger's Hood": dict(hood='ranger'),
    'Trail Cap': dict(cap='visor'), 'Tin Skullcap': dict(cap='metal'), 'Padded Arming Cap': dict(cap='padded'),
    "Miner's Helm": dict(cap='miner'), 'Felt Pilgrim Cap': dict(cap='pilgrim'),
    # armour
    'Padded Gambeson': dict(robe='diamond'), 'Trail Vest': dict(robe='vest'), 'Hide Jerkin': dict(robe='laced'),
    'Woolen Robe-Top': dict(robe='sash'), 'Quilted Vest': dict(robe='vquilt'), 'Rangerwool Jerkin': dict(robe='ranger'),
    'Frostlinen Vest': dict(robe='frost'),
}


# ============================================================== swords
U = (0.7071, -0.7071)       # along the blade, toward the tip (upper right)
P = (-0.7071, -0.7071)      # across it, toward the lit edge (upper left)


def at(b, t, s=0.0):
    return (b[0] + U[0] * t + P[0] * s, b[1] + U[1] * t + P[1] * s)


def blade(C, K, base, L, wl, wr, n=14, curve=0.0, fuller=0.0, wave=0.0, nicks=0, tip=1.0):
    """A blade from base (the guard) along U for L pixels. wl(t), wr(t)
       give the half width on the lit and the shadow side at t in 0..1;
       curve bends it toward the shadow side; wave scallops the edges."""
    lit, sh, mid = [], [], []
    vv = getattr(K, 'v', {})
    L *= 1.16 * vv.get('len', 1.0)
    W = 1.4 * vv.get('wid', 1.0)
    base = (base[0] - 6, base[1] + 6)
    for i in range(n + 1):
        t = i / n
        off = curve * math.sin(t * math.pi * 0.8) * L * 0.12
        w1 = wl(t) * W; w2 = wr(t) * W
        if wave:
            k = math.sin(t * math.pi * 7) * wave * (1 - t)
            w1 += k; w2 -= k
        lit.append(at(base, t * L * tip, w1 - off))
        sh.append(at(base, t * L * tip, -w2 - off))
        mid.append(at(base, t * L * tip, -off))
    C.plate(lit + mid[::-1], K.body, z=6, bevel=1.0, tilt=(-1.1, -1.1))
    C.plate(mid + sh[::-1], K.body, z=6, bevel=1.0, tilt=(0.9, 0.9))
    if K.glow and K.rar >= 2:
        for i in range(len(sh) - 1):
            (x0, y0), (x1, y1) = sh[i], sh[i + 1]
            C.limb([(x0, y0, 0.7, 14), (x1, y1, 0.7, 14)], K.glow)
    if fuller:
        fuller *= 1.4
        a = [at(base, t * L * 0.72, (fuller - (lambda t: curve * math.sin(t * math.pi * 0.8) * L * 0.12)(t)))
             for t in np.linspace(0.06, 1, 8)]
        b = [at(base, t * L * 0.72, (-fuller * 0.6 - (lambda t: curve * math.sin(t * math.pi * 0.8) * L * 0.12)(t)))
             for t in np.linspace(0.06, 1, 8)]
        C.plate(a + b[::-1], K.dark, z=8, bevel=0.8, tilt=(0.3, 0.3))
    # a bright line down the lit edge
    for i in range(len(lit) - 1):
        (x0, y0), (x1, y1) = lit[i], lit[i + 1]
        C.limb([(x0 - P[0] * -0.6, y0 - P[1] * -0.6, 0.55, 12), (x1 - P[0] * -0.6, y1 - P[1] * -0.6, 0.55, 12)], K.edge)
    for j in range(nicks):
        t = 0.25 + j * 0.23
        x, y = at(base, t * L, wl(t) - 0.4)
        C.dot(x, y, (0, 0, 0, 0)) if False else None
        C.ball(x, y, 1.2, K.dark, z=12)
    return lit, sh, mid


def hilt(C, K, base, grip=13.0, half=9.0, pom=3.4, curve=0.0, ring=False, tsuba=False):
    base = (base[0] - 6, base[1] + 6)
    v = getattr(K, 'v', {})
    grip *= 1.15 * v.get('grip', 1.0); half *= 1.3 * v.get('guard', 1.0); pom *= 1.25
    curve = v.get('curve', curve)
    if v.get('wrap'):
        K.grip = Mat(v['wrap'], 7, tex=lambda c: (np.sin((c.X + c.Y) * 1.25) > 0.35) * -1.6)
    gb = at(base, -2.0)
    ge = at(base, -grip)
    C.limb([(gb[0], gb[1], 2.9), (ge[0], ge[1], 2.9)], K.grip, z=4)
    pm = at(base, -grip - pom * 0.6)
    pk = v.get('pommel', 'ball')
    if pk == 'ring':
        C.ell(pm[0], pm[1], pom * 1.1, pom * 1.1, 2, K.acc, z=8)
        C.ball(pm[0], pm[1], pom * 0.5, Mat('#141018', 4), z=10)
    elif pk == 'fish':
        a1 = at(pm, -pom * 0.6, pom * 1.4); a2 = at(pm, -pom * 0.6, -pom * 1.4)
        C.plate([a1, at(pm, pom * 0.8), a2, at(pm, -pom * 0.2)], K.acc, z=8, bevel=1.2)
    elif pk == 'spike':
        C.plate([at(pm, 0, pom * 0.9), at(pm, -pom * 2.2), at(pm, 0, -pom * 0.9)], K.acc, z=8, bevel=1.2)
    else:
        C.ball(pm[0], pm[1], pom, K.acc, z=8)
    if v.get('tassel'):
        tm = Mat(v['tassel'], 6)
        C.limb([(pm[0], pm[1] + 1, 1.0, 9), (pm[0] - 1, pm[1] + 9, 1.4, 9), (pm[0] + 1, pm[1] + 14, 1.0, 9)], tm)
    if K.rar >= 2:
        C.ball(pm[0], pm[1], pom * 0.45, K.gem, z=12)
    if tsuba:
        C.ell(base[0], base[1], 5.5, 5.5, 3, K.acc, z=10)
        C.ell(base[0], base[1], 3.0, 3.0, 2, K.dark, z=12)
        return
    if v.get('guardk') == 'none':
        C.ball(base[0], base[1], 3.2, K.acc, z=10)
        return
    if v.get('guardk') == 'disc':
        C.ell(base[0], base[1], half * 0.55, half * 0.55, 3, K.acc, z=10)
        C.ball(base[0], base[1], 2.4, K.dark, z=12)
        return
    a = at(base, -0.5, half); b = at(base, -0.5, -half)
    ca = at(base, -0.5 + curve * 3, half + 0.5); cb = at(base, -0.5 + curve * 3, -half - 0.5)
    C.limb([(ca[0], ca[1], 2.0), (a[0], a[1], 3.0), (base[0], base[1], 3.4), (b[0], b[1], 3.0), (cb[0], cb[1], 2.0)], K.acc, z=10)
    if K.rar >= 2:
        for e in (ca, cb):
            C.ball(e[0], e[1], 2.2, K.acc, z=12)
    C.ball(base[0], base[1], 2.6, K.gem if K.rar >= 1 else K.acc, z=14)
    if ring:
        r0 = at(base, -5, -5)
        C.limb([(b[0], b[1], 1.2), (r0[0], r0[1], 1.2), (ge[0], ge[1], 1.2)], K.acc, z=12)


def s_arming(C, K):
    base = (30, 66); v = K.v
    L = 62; w = 4.2
    blade(C, K, base, L, lambda t: w * (1 - t ** 3) + 0.4, lambda t: w * (1 - t ** 3) + 0.4,
          fuller=1.2 if K.rar >= 1 else 0, nicks=v['nicks'])
    hilt(C, K, base)


def s_falchion(C, K):
    base = (30, 66)
    blade(C, K, base, 58, lambda t: 3.0 + t * 2.0 - (t > 0.85) * (t - 0.85) * 30, lambda t: 2.4 + t * 3.6 * (1 - t ** 4),
          curve=0.5, nicks=1 if K.rar == 0 else 0)
    hilt(C, K, base, curve=0.6)


def s_great(C, K):
    base = (26, 70)
    blade(C, K, base, 70, lambda t: 6.0 * (1 - t ** 4) + 0.6, lambda t: 6.0 * (1 - t ** 4) + 0.6, fuller=1.8)
    hilt(C, K, base, grip=18, half=13, pom=4.2)
    if K.glow:
        for t in (0.25, 0.4, 0.55):
            x, y = at(base, t * 70, 0.3)
            C.ball(x, y, 1.1, K.glow, z=16)


def s_flamberge(C, K):
    base = (28, 68)
    blade(C, K, base, 64, lambda t: 4.6 * (1 - t ** 3) + 0.5, lambda t: 4.6 * (1 - t ** 3) + 0.5, wave=1.6, fuller=1.0)
    hilt(C, K, base, half=11, grip=15)


def s_rapier(C, K):
    base = (30, 66)
    blade(C, K, base, 66, lambda t: 1.8 * (1 - t ** 2) + 0.4, lambda t: 1.8 * (1 - t ** 2) + 0.4)
    hilt(C, K, base, half=7, ring=True)


def s_cleaver(C, K):
    base = (30, 66)
    blade(C, K, base, 50, lambda t: 3.0 + t * 1.5, lambda t: 5.0 + t * 5.5 - (t > 0.8) * (t - 0.8) * 30,
          nicks=2 if K.rar == 0 else 0)
    hilt(C, K, base, half=7, grip=14)


def s_katana(C, K):
    base = (30, 66)
    blade(C, K, base, 64, lambda t: 2.6 * (1 - t ** 6), lambda t: 2.6 * (1 - t ** 6) + 0.6, curve=0.9)
    # a temper line along the edge
    hilt(C, K, base, grip=17, tsuba=True)


def s_broken(C, K):
    base = (30, 66)
    lit, sh, mid = blade(C, K, base, 40, lambda t: 4.4, lambda t: 4.4, fuller=1.1)
    # a snapped, jagged end
    e = at(base, 40)
    C.plate([at(base, 38, 4.4), at(base, 44, 2.0), at(base, 41, 0), at(base, 45, -2.5), at(base, 38, -4.4)],
            K.body, z=6, bevel=1, tilt=(-0.3, -0.3))
    hilt(C, K, base, half=8)


SWORDS = [s_arming, s_falchion, s_great, s_flamberge, s_rapier, s_cleaver, s_katana, s_broken]


# ============================================================== staffs
def shaft(C, K, top=34, cx=48, lean=2.0, knots=False):
    pts = [(cx + lean, 93, 2.6), (cx + lean * 0.4, 70, 2.9), (cx - lean * 0.2, 50, 3.0), (cx - lean * 0.5, top, 3.1)]
    C.limb(pts, K.wood)
    for y in (top + 4, 76, 89):
        C.ell(cx + lean * (0.6 if y > 70 else -0.3), y, 4.0, 1.6, 4, K.acc, z=4)
    for i in range(6):
        y = 57 + i * 3
        C.limb([(cx - 3.3, y, 1.0, 5), (cx + 3.3, y + 1.6, 1.0, 5)], K.grip)
    if knots:
        for (x, y) in ((cx - 2, 60), (cx + 1, 80)):
            C.ball(x, y, 2.2, K.wood, z=4)


def st_orb(C, K):
    """knotted wood that splits at the top into three roots gripping a sphere"""
    cx = 48
    pts = [(cx + 2, 93, 2.6), (cx - 1, 84, 3.0), (cx + 2, 74, 2.8), (cx - 2, 62, 3.1), (cx + 1, 50, 3.0),
           (cx - 1, 40, 3.2), (cx, 34, 3.6)]
    C.limb(pts, K.wood)
    for (x, y, r) in ((cx - 1, 84, 3.6), (cx + 2, 72, 3.2), (cx - 2, 60, 3.5), (cx + 1, 36, 4.0)):
        C.ball(x, y, r, K.wood, z=3)
        C.dot(x - r * 0.3, y - r * 0.2, (40, 26, 18))
    for i in range(6):
        y = 57 + i * 3
        C.limb([(cx - 3.3, y, 1.0, 5), (cx + 3.3, y + 1.6, 1.0, 5)], K.grip)
    C.ell(cx + 1, 90, 3.6, 1.6, 4, K.acc, z=4)
    orb = K.glow or Mat(PAL[K.g[4]][2], 7, spec=0.9, gloss=0.9)
    C.ball(cx, 19, 8.6, orb, z=2)
    C.dot(cx - 3, 15, (255, 255, 250)); C.dot(cx - 2, 15, (255, 252, 240))
    for (k, z) in ((-1, 8), (0, -4), (1, 8)):
        C.limb([(cx + k * 2, 34, 2.4), (cx + k * 9, 26, 2.0), (cx + k * 9.5, 16, 1.6), (cx + k * 5, 9, 1.1)], K.wood, z=z)
    C.ball(cx + 1, 35, 3.4, K.wood, z=10)


def st_crystal(C, K):
    shaft(C, K)
    q = K.glow or Mat(PAL[K.g[4]][1], 7, spec=0.8, gloss=0.8)
    for (x, y, h, w, a) in [(48, 34, 28, 5, 0.0), (44, 34, 18, 3.6, -0.35), (53, 34, 20, 3.8, 0.3), (40, 36, 10, 3, -0.7)]:
        ca, sa = math.sin(a), -math.cos(a)
        tx, ty = x + ca * h, y + sa * h
        px, py = -sa * w, ca * w
        C.plate([(x - px, y - py), (tx, ty), (x + px * 0.1, y + py * 0.1)], q, z=6, bevel=1, tilt=(-0.6, -0.4))
        C.plate([(x + px * 0.1, y + py * 0.1), (tx, ty), (x + px, y + py)], q, z=6, bevel=1, tilt=(0.5, 0.2))
    C.ell(48, 36, 7, 3, 4, K.acc, z=10)


def st_crescent(C, K):
    shaft(C, K, top=30)
    C.plate([(30, 10), (40, 26), (48, 30), (56, 26), (66, 10), (58, 20), (48, 23), (38, 20)], K.body, z=6, bevel=1.4, tilt=(-0.4, -0.5))
    C.ball(48, 30, 3.4, K.gem, z=12)
    for x in (36, 60):
        C.ell(x, 30, 2.4, 3.2, 2, K.acc, z=10)


def st_lantern(C, K):
    shaft(C, K, top=14, lean=1.0)
    C.limb([(48, 14, 2.4), (60, 12, 2.0), (66, 18, 1.6)], K.wood, z=4)
    C.limb([(66, 18, 0.7, 6), (66, 24, 0.7, 6)], K.acc)
    lamp = K.glow or Mat('#ffc860', 6, emit=True, glow=3,
                        tones=[(150, 70, 20), (210, 120, 30), (245, 170, 60), (255, 210, 120), (255, 240, 200), (255, 255, 240)])
    C.ell(66, 34, 6, 8, 5, lamp, z=4)
    for x in (60, 66, 72):
        C.limb([(x, 25, 0.9, 10), (x, 42, 0.9, 10)], K.acc)
    C.plate([(59, 23), (73, 23), (70, 26), (62, 26)], K.acc, z=10, bevel=1)
    C.plate([(60, 42), (72, 42), (70, 45), (62, 45)], K.acc, z=10, bevel=1)


def st_branch(C, K):
    """a length of old wood: a thick crooked trunk leaning a little, the
       stubs of broken branches, knots, and a round burl for a head"""
    tc = PAL['wood'][0] if K.g[4] == 'moss' else PAL[K.g[4]][0]
    w = Mat(tc, 8, tex=lambda c: tex_bark(c, 1.3, 11), light=0.55)
    dk = Mat(tc, 7, dark=0.9, light=0.25)
    head = Mat(PAL[K.g[4]][0], 8, tex=lambda c: tex_bark(c, 1.0, 12), light=0.55)
    trunk = [(43, 93, 2.8), (45, 84, 3.3), (44, 74, 3.0), (46, 64, 3.4), (47, 54, 3.0), (49, 44, 3.4), (49, 34, 3.1),
             (50, 24, 3.5)]
    C.limb(trunk, w)
    # broken branch stubs, alternating sides
    for (x0, y0, x1, y1, r) in [(46, 62, 57, 54, 1.8), (47, 54, 38, 46, 1.6), (49, 40, 58, 33, 1.5),
                                (45, 80, 37, 75, 1.4), (50, 30, 42, 23, 1.3)]:
        C.limb([(x0, y0, r + 0.6), (x1, y1, r)], w, z=-2 if x1 < x0 else 2)
        C.ell(x1, y1, r, r * 0.8, 2, dk, z=8)                   # the broken end grain
    # knots
    for (x, y) in ((45, 70), (48, 48), (45, 86)):
        C.ell(x, y, 1.5, 1.1, 2, dk, z=10)
        C.dot(x - 0.6, y - 0.6, (210, 180, 130))
    # the burl head
    C.ball(50, 17, 6.8, head, z=4)
    for a_ in range(2):
        C.ell(50, 17, 6.8 - a_ * 3, 0.9, 1, dk, z=12 + a_, rot=0.2)
    C.ell(47.5, 14, 1.7, 1.2, 2, dk, z=16)
    # a few turns of leather where the hand goes
    for i in range(4):
        y = 59 + i * 3
        C.limb([(44, y, 0.9, 8), (50, y + 1.2, 0.9, 8)], K.grip)
    if K.glow:
        C.ball(50, 17, 2.4, K.glow, z=20)


def st_totem(C, K):
    shaft(C, K, top=36)
    bone = Mat('#e0d6bc', 7)
    C.ell(48, 24, 9, 10, 8, bone, z=4)
    C.ell(48, 31, 6, 4, 5, bone, z=6)
    for x in (44.5, 51.5):
        C.ball(x, 23, 2.4, Mat('#1a1414', 4), z=12)
        if K.glow:
            C.ball(x, 23, 1.3, K.glow, z=14)
    for x in range(44, 53, 2):
        C.dot(x, 32, (40, 30, 26))
    for (x0, x1) in ((40, 34), (56, 62)):
        C.limb([(x0, 30, 0.7, 8), (x1, 44, 0.7, 8)], Mat(PAL.get(K.g[5], PAL['leather'])[1], 5))
        C.plate([(x1 - 2, 44), (x1 + 2, 44), (x1, 54)], Mat(PAL[K.g[4]][1], 6), z=9, bevel=1)
    for a in (-0.5, 0, 0.5):
        C.plate([(48 + a * 6 - 2, 15), (48 + a * 16, 2), (48 + a * 6 + 2, 15)], Mat(PAL[K.g[4]][0], 6), z=2, bevel=1)


STAFFS = [st_orb, st_crystal, st_crescent, st_lantern, st_branch, st_totem]


# ============================================================== shields
def face(C, K, pts, z=4, studs=0):
    C.plate(pts, K.acc if K.g[4] in ('wood',) else K.dark, z=z, bevel=3.0, tilt=(-0.2, -0.2), dome=0.0)
    inner = _shrink(pts, 0.86)
    C.plate(inner, K.body, z=z + 3, bevel=4.0, dome=0.9, tilt=(-0.1, -0.1))
    for i in range(studs):
        a = i / studs
        x, y = _along(pts, a)
        cx, cy = _centre(pts)
        x, y = cx + (x - cx) * 0.93, cy + (y - cy) * 0.93
        C.ball(x, y, 1.6, K.acc, z=z + 8)
    return inner


def _centre(pts):
    return sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)


def _shrink(pts, k):
    cx, cy = _centre(pts)
    return [(cx + (x - cx) * k, cy + (y - cy) * k) for x, y in pts]


def _along(pts, a):
    n = len(pts); f = a * n; i = int(f) % n; u = f - int(f)
    (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
    return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u


def circ(cx, cy, r, n=28):
    return [(cx + math.cos(i / n * 2 * math.pi) * r, cy + math.sin(i / n * 2 * math.pi) * r) for i in range(n)]


def planks(C, K, x0, x1, y0, y1, n=5):
    for i in range(1, n):
        x = x0 + (x1 - x0) * i / n
        C.limb([(x, y0, 0.6, 14), (x, y1, 0.6, 14)], K.dark)


def dress(C, K, pts, cx=48, cy=50):
    """what is painted or built on a face: the per piece variety"""
    v = K.v; inner = _shrink(pts, 0.82)
    f = v.get('face')
    if f == 'bark':
        C.plate(inner, Mat('#6a4a2a', 7, tex=lambda c: tex_bark(c, 1.4, 9)), z=24, bevel=3, dome=0.8)
        for (x, y) in ((cx - 8, cy - 6), (cx + 9, cy + 8)):
            C.ell(x, y, 3, 2.2, 2, Mat('#3a2616', 5), z=28)
    elif f == 'hide':
        C.plate(inner, Mat('#a87a50', 7, tex=lambda c: (vnoise(c.X, c.Y, 0.25, 3) - 0.5) * 1.6), z=24, bevel=4, dome=0.9)
        for i in range(18):
            a = i / 18 * 2 * math.pi
            C.dot(cx + math.cos(a) * 24, cy + math.sin(a) * 24, (60, 36, 20))
    elif f == 'weave':
        C.plate(inner, Mat('#b89a5a', 7, tex=lambda c: ((np.floor(c.X / 3) + np.floor(c.Y / 3)) % 2) * 1.4 - 0.7), z=24, bevel=3, dome=0.8)
    elif f == 'patch':
        for (dx, dy, w, h) in ((-14, -14, 14, 12), (4, -10, 12, 16), (-12, 6, 16, 12)):
            x0, y0 = cx + dx, cy + dy
            C.plate([(x0, y0), (x0 + w, y0 + 1), (x0 + w - 1, y0 + h), (x0 + 1, y0 + h - 1)], K.dark, z=26, bevel=1.4, tilt=(-0.2, -0.3))
            for (px, py) in ((x0 + 2, y0 + 2), (x0 + w - 2, y0 + 2), (x0 + 2, y0 + h - 2), (x0 + w - 2, y0 + h - 2)):
                C.ball(px, py, 1.0, K.acc, z=30)
    p_ = v.get('paint')
    paintm = Mat('#8a2a24', 6)
    if p_ == 'quarters':
        for (a0, a1) in ((0, 0.25), (0.5, 0.75)):
            C.plate([(cx, cy)] + [(cx + math.cos(t * 2 * math.pi) * 30, cy + math.sin(t * 2 * math.pi) * 30) for t in np.linspace(a0, a1, 8)],
                    paintm, z=23, bevel=2, dome=0.6)
    elif p_ == 'halves':
        C.plate([(cx, 4), (cx + 30, 14), (cx + 28, 44), (cx, 90)], Mat('#2a4a7a', 6), z=23, bevel=2, dome=0.6)
    elif p_ == 'stripe':
        C.plate([(cx - 30, cy - 4), (cx + 30, cy - 4), (cx + 30, cy + 4), (cx - 30, cy + 4)], paintm, z=26, bevel=1.4)
    elif p_ == 'bands':
        for y in (24, 36):
            C.plate([(22, y), (74, y), (72, y + 4), (24, y + 4)], Mat('#2a3a6a', 6), z=26, bevel=1.2)
    if v.get('dents'):
        for (x, y) in ((cx - 12, cy + 10), (cx + 14, cy - 12), (cx + 6, cy + 18)):
            C.ball(x, y, 2.4, K.dark, z=27)
    if v.get('straps'):
        for x in (32, 64):
            C.plate([(x - 3, 10), (x + 3, 10), (x + 3, 84), (x - 3, 84)], Mat('#4a2e1a', 6), z=26, bevel=1.2)
            for y in (20, 46, 72):
                C.ball(x, y, 1.4, K.acc, z=30)


def sh_round(C, K):
    face(C, K, circ(48, 50, 40), studs=12)
    if K.g[4] == 'wood':
        planks(C, K, 14, 82, 16, 84)
    dress(C, K, circ(48, 50, 40))
    C.ball(48, 50, 10, K.acc, z=34)
    C.ball(48, 50, 4, K.gem if K.rar >= 1 else K.acc, z=40)


def emblem(C, K, cx, cy, kind):
    m = K.glow or K.acc
    if kind == 'hourglass':
        C.plate([(cx - 9, cy - 16), (cx + 9, cy - 16), (cx + 1.6, cy), (cx + 9, cy + 16), (cx - 9, cy + 16), (cx - 1.6, cy)], K.acc, z=30, bevel=1.4)
        C.plate([(cx - 6, cy - 13), (cx + 6, cy - 13), (cx, cy - 2)], m, z=34, bevel=1)
        C.plate([(cx - 6, cy + 13), (cx + 6, cy + 13), (cx, cy + 6)], m, z=34, bevel=1)
        for a in range(12):
            ang = a / 12 * 2 * math.pi
            C.ball(cx + math.cos(ang) * 22, cy + math.sin(ang) * 22, 1.3, K.acc, z=30)
    elif kind == 'chevron':
        C.plate([(cx - 18, cy - 4), (cx, cy + 10), (cx + 18, cy - 4), (cx + 18, cy + 4), (cx, cy + 18), (cx - 18, cy + 4)], K.acc, z=30, bevel=1.4)
    elif kind == 'eye':
        C.ell(cx, cy, 12, 6, 3, K.acc, z=30)
        C.ball(cx, cy, 4.4, m, z=34)
    elif kind == 'wave':
        for k in range(3):
            y = cy - 8 + k * 8
            C.limb([(cx - 16 + i * 4, y + math.sin(i * 1.4) * 2.4, 1.3, 16) for i in range(9)], m)
    elif kind == 'flame':
        C.plate([(cx, cy - 18), (cx + 8, cy - 2), (cx + 4, cy + 12), (cx, cy + 6), (cx - 4, cy + 12), (cx - 8, cy - 2)], m, z=30, bevel=1.4)


def sh_kite(C, K):
    pts = [(48, 6), (78, 14), (76, 44), (48, 92), (20, 44), (18, 14)]
    face(C, K, pts, studs=10)
    dress(C, K, pts, 48, 44)
    emblem(C, K, 48, 40, 'hourglass' if K.rar >= 3 else ('eye' if K.rar >= 1 else 'chevron'))


def sh_tower(C, K):
    pts = [(20, 8), (76, 8), (78, 76), (48, 92), (18, 76)]
    face(C, K, pts, studs=10)
    dress(C, K, pts)
    for y in (26, 58):
        C.plate([(20, y - 3), (76, y - 3), (76, y + 3), (20, y + 3)], K.acc, z=14, bevel=1.4)
    if K.rar >= 2:
        emblem(C, K, 48, 42, 'eye')


def sh_buckler(C, K):
    face(C, K, circ(48, 50, 30), studs=0 if K.v.get('face') else 8)
    if K.g[4] in ('wood', 'leather') and not K.v.get('face'):
        planks(C, K, 22, 74, 24, 76, 4)
    dress(C, K, circ(48, 50, 30))
    C.ball(48, 50, 8, K.acc, z=34)
    C.plate([(44, 50), (48, 36), (52, 50)], K.acc, z=44, bevel=1.4)
    if K.glow:
        for a in range(6):
            ang = a / 6 * 2 * math.pi
            C.ball(48 + math.cos(ang) * 20, 50 + math.sin(ang) * 20, 1.6, K.glow, z=18)


def sh_heater(C, K):
    pts = [(16, 10), (80, 10), (78, 46), (64, 74), (48, 88), (32, 74), (18, 46)]
    face(C, K, pts, studs=0)
    dress(C, K, pts, 48, 44)
    emblem(C, K, 48, 44, 'wave' if K.g[4] == 'sea' else ('chevron' if not K.v.get('face') else 'eye'))


def sh_spiked(C, K):
    for a in range(10):
        ang = a / 10 * 2 * math.pi + 0.3
        x0, y0 = 48 + math.cos(ang) * 32, 50 + math.sin(ang) * 32
        x1, y1 = 48 + math.cos(ang) * 46, 50 + math.sin(ang) * 46
        px, py = -math.sin(ang) * 4, math.cos(ang) * 4
        C.plate([(x0 - px, y0 - py), (x1, y1), (x0 + px, y0 + py)], K.acc, z=2, bevel=1.2)
    face(C, K, circ(48, 50, 36), studs=10)
    if K.g[4] == 'moss':
        vine = Mat('#4a6e2a', 6)
        for a in range(5):
            ang = a / 5 * 2 * math.pi
            C.limb([(48 + math.cos(ang) * 10, 50 + math.sin(ang) * 10, 1.2, 14), (48 + math.cos(ang + 0.6) * 26, 50 + math.sin(ang + 0.6) * 26, 1.0, 14)], vine)
    emblem(C, K, 48, 50, 'flame' if K.g[4] == 'ember' else 'eye')


SHIELDS = [sh_round, sh_kite, sh_tower, sh_buckler, sh_heater, sh_spiked]


# ================================================================ helms
def dome(C, K, cx=48, cy=46, rx=28, ry=30, m=None):
    C.ell(cx, cy, rx, ry, 24, m or K.body)


def hm_hood(C, K):
    C.plate([(18, 88), (22, 40), (34, 14), (48, 8), (62, 14), (76, 40), (80, 88), (64, 82), (48, 86), (32, 82)], K.body, z=4, bevel=8, dome=1.4)
    C.ell(48, 52, 15, 19, 6, Mat('#141018', 4), z=14)
    for x in (42, 54):
        C.dot(x, 50, (60, 50, 50))
    h = K.v.get('hood')
    if h == 'knit':
        for y in range(16, 86, 5):
            C.limb([(22, y, 0.5, 12), (74, y, 0.5, 12)], K.dark)
        C.ball(48, 8, 5, K.body, z=10)
        C.limb([(26, 80, 2.4, 20), (48, 84, 2.4, 20), (70, 80, 2.4, 20)], K.grip)
    elif h == 'coif':
        for x in (34, 48, 62):
            C.limb([(x, 12, 0.6, 12), (x + (x - 48) * 0.5, 86, 0.6, 12)], K.dark)
        C.limb([(34, 72, 1.6, 22), (48, 76, 1.6, 22), (62, 72, 1.6, 22)], K.grip)
        C.ball(62, 72, 2.2, K.acc, z=26)
    elif h == 'ranger':
        C.limb([(62, 16, 4, 2), (76, 26, 3, 2), (84, 44, 2.2, 2), (86, 62, 1.6, 2)], K.body)
        C.limb([(26, 80, 2.4, 20), (48, 84, 2.4, 20), (70, 80, 2.4, 20)], K.grip)
        leaf = Mat('#c8a040', 6, spec=0.6)
        C.plate([(44, 78), (48, 72), (52, 78), (48, 86)], leaf, z=26, bevel=1.2)
    else:
        C.limb([(26, 80, 2.4, 20), (48, 84, 2.4, 20), (70, 80, 2.4, 20)], K.grip)


def hm_horned(C, K):
    bone = Mat('#e8dcc0', 7)
    for k in (-1, 1):
        C.limb([(48 + k * 22, 40, 5.5), (48 + k * 34, 30, 4.4), (48 + k * 40, 16, 3.0), (48 + k * 37, 6, 1.4)], bone, z=2)
    dome(C, K, 48, 52, 26, 26)
    C.plate([(22, 54), (74, 54), (74, 60), (22, 60)], K.acc, z=26, bevel=1.4)
    C.plate([(45, 54), (51, 54), (50, 80), (46, 80)], K.acc, z=28, bevel=1.2)
    for x in (32, 64):
        C.ell(x, 66, 7, 4, 3, Mat('#141018', 4), z=26)
    if K.glow:
        for x in (32, 64):
            C.ball(x, 66, 1.6, K.glow, z=30)


def hm_great(C, K):
    C.plate([(22, 20), (34, 8), (62, 8), (74, 20), (76, 82), (20, 82)], K.body, z=4, bevel=7, dome=1.2)
    C.plate([(24, 40), (72, 40), (72, 46), (24, 46)], Mat('#141018', 4), z=18, bevel=0.6)
    C.plate([(45, 10), (51, 10), (50, 38), (46, 38)], K.acc, z=20, bevel=1.4)
    for i in range(4):
        for j in range(2):
            C.ball(34 + j * 28, 58 + i * 5, 1.0, Mat('#141018', 4), z=20)
    if K.rar >= 3:
        for k in (-1, 1):
            C.plate([(48 + k * 4, 10), (48 + k * 18, -2), (48 + k * 12, 14)], K.acc, z=10, bevel=1.4)
        if K.glow:
            C.plate([(26, 41), (70, 41), (70, 45), (26, 45)], K.glow, z=19, bevel=0.5)


def hm_crown(C, K):
    thorn = K.wood
    C.ell(48, 56, 32, 12, 10, thorn, z=0)
    C.ell(48, 56, 24, 7, 8, Mat('#141018', 4), z=6)
    for i in range(9):
        a = i / 9 * math.pi
        x = 48 - math.cos(a) * 30; y = 52 - math.sin(a) * 6
        C.plate([(x - 3, y + 2), (x + math.cos(a) * -2, y - 18 - (i % 2) * 6), (x + 3, y + 2)], thorn, z=10, bevel=1.2)
    leaf = Mat('#4a8a3a', 6)
    for i in range(6):
        C.ell(22 + i * 10, 62 + (i % 2) * 3, 3.6, 2, 2, leaf, z=14, rot=0.5)
    if K.glow:
        for x in (30, 48, 66):
            C.ball(x, 46, 2.4, K.glow, z=16)


def hm_brim(C, K):
    peaked = 'Peaked' in K.g[0]
    C.ell(48, 70, 44, 11, 8, K.body, z=0)
    if peaked:
        C.plate([(28, 70), (44, 32), (58, 10), (72, 6), (64, 18), (60, 40), (68, 70)], K.body, z=8, bevel=6, dome=1.0)
        C.plate([(30, 62), (66, 62), (68, 68), (28, 68)], K.acc, z=20, bevel=1.4)
        if K.glow:
            C.ball(48, 65, 2.4, K.glow, z=24)
    else:
        C.ell(48, 56, 22, 18, 16, K.body, z=6)
        C.plate([(26, 60), (70, 60), (70, 67), (26, 67)], Mat('#9a3a2a', 6), z=20, bevel=1.4)
    C.ell(48, 72, 30, 5, 4, Mat('#141018', 4), z=1)


def hm_barbute(C, K):
    dome(C, K, 48, 50, 27, 34)
    C.plate([(30, 44), (66, 44), (66, 49), (52, 49), (52, 80), (44, 80), (44, 49), (30, 49)], Mat('#141018', 4), z=26, bevel=0.6)
    C.limb([(48, 16, 2.0, 22), (48, 30, 2.0, 22)], K.acc)
    for x in (30, 66):
        C.ball(x, 62, 1.4, K.acc, z=26)


def hm_cap(C, K):
    C.plate([(18, 62)] + [(48 - math.cos(a) * 30, 60 - math.sin(a) * 30) for a in np.linspace(0.12, math.pi - 0.12, 14)] + [(78, 62)],
            K.body, z=4, bevel=9, dome=1.6)
    C.plate([(16, 58), (80, 58), (80, 68), (16, 68)], K.acc if not K.soft else K.grip, z=26, bevel=1.4)
    if not K.soft:
        for x in range(22, 78, 9):
            C.ball(x, 63, 1.3, K.dark, z=30)
        C.limb([(48, 32, 1.8, 24), (48, 58, 1.8, 24)], K.acc)
    else:
        C.ball(48, 33, 3.2, K.grip, z=24)
    cp = K.v.get('cap')
    if cp == 'visor':
        C.ell(62, 66, 20, 5, 4, K.body, z=28, rot=0.06)
        C.ball(48, 33, 3.2, K.grip, z=24)
    elif cp == 'padded':
        for x in range(24, 76, 8):
            C.limb([(x, 38, 0.6, 26), (x + (x - 48) * 0.1, 58, 0.6, 26)], K.dark)
        for k in (-1, 1):
            C.limb([(48 + k * 26, 66, 1.6, 20), (48 + k * 24, 84, 1.6, 20)], K.grip)
    elif cp == 'pilgrim':
        C.ell(48, 60, 36, 7, 5, K.body, z=2)
        shell = Mat('#efe6d0', 6)
        C.ell(62, 50, 5, 5, 4, shell, z=30)
        for a in (-0.6, -0.2, 0.2, 0.6):
            C.dot(62 + math.sin(a) * 4, 50 + math.cos(a) * -1, (150, 130, 110))
        C.limb([(30, 52, 1.0, 30), (18, 36, 0.8, 30), (14, 26, 0.5, 30)], Mat('#a83a2a', 6))
    elif cp == 'metal':
        for (x, y) in ((36, 44), (60, 40), (52, 50)):
            C.ball(x, y, 2.2, K.dark, z=26)
    if 'Miner' in K.g[0]:
        lamp = Mat('#ffd060', 6, emit=True, glow=3, tones=GLOW['sun'][1])
        C.ball(48, 48, 5.5, K.acc, z=28)
        C.ball(48, 48, 3.6, lamp, z=32)


def hm_crown_grand(C, K):
    C.ell(48, 66, 30, 9, 8, K.body, z=0)
    C.ell(48, 66, 23, 5, 6, Mat('#141018', 4), z=4)
    for i in range(7):
        a = i / 6
        x = 20 + a * 56
        h = 22 + 14 * math.sin(a * math.pi)
        C.plate([(x - 4.5, 64), (x, 64 - h), (x + 4.5, 64)], K.body, z=10, bevel=1.4, tilt=(-0.3, -0.3))
        C.ball(x, 64 - h, 2.2, K.gem, z=16)
    C.ball(48, 52, 5.5, K.gem, z=20)
    C.plate([(18, 66), (78, 66), (78, 72), (18, 72)], K.acc, z=14, bevel=1.4)
    for x in (30, 48, 66):
        C.ball(x, 69, 2.0, K.gem, z=18)


def hm_wolf(C, K):
    """A wolf's head worn as a hood: the skull rides on top, the snout
       juts at you over a dark face, the upper fangs hang down across it
       and the pelt falls to the shoulders with the forepaws knotted."""
    fur = Mat(PAL[K.g[4]][0], 8, tex=lambda c: tex_strands(c, 95, 1.3, 5, 700, 4))
    dfur = Mat(PAL[K.g[4]][0], 8, tex=lambda c: tex_strands(c, 80, 1.1, 6, 500, 4), dark=0.9, light=0.3)
    pale = Mat('#c8b8a0', 7, tex=lambda c: tex_strands(c, 90, 1.0, 7, 300, 3))
    bone = Mat('#ece2c8', 6, spec=0.4)
    # the pelt, falling wide to the shoulders
    C.plate([(10, 92), (14, 56), (24, 30), (48, 22), (72, 30), (82, 56), (86, 92), (66, 86), (48, 90), (30, 86)],
            dfur, z=0, bevel=9, dome=1.0)
    C.tufts([(12, 88), (16, 60), (24, 36)], dfur, z=2, n=6, length=4, width=4, out=(-1, 0.1), seed=3)
    C.tufts([(84, 88), (80, 60), (72, 36)], dfur, z=2, n=6, length=4, width=4, out=(1, 0.1), seed=4)
    # the face inside
    C.ell(48, 70, 12, 11, 4, Mat('#141018', 4), z=8)
    # the head on top
    C.ell(48, 32, 15, 13, 16, fur, z=10)
    for k in (-1, 1):
        C.plate([(48 + k * 5, 26), (48 + k * 16, -6), (48 + k * 18, 24)], fur, z=12, bevel=2.5, tilt=(k * 0.3, -0.4))
        C.plate([(48 + k * 9, 22), (48 + k * 15.5, 2), (48 + k * 16, 21)], pale, z=13, bevel=1.4)
    # a long narrow muzzle running down toward you
    C.plate([(41, 34), (55, 34), (53, 52), (50, 61), (46, 61), (43, 52)], fur, z=18, bevel=4, dome=1.6)
    C.plate([(43, 50), (53, 50), (51, 58), (45, 58)], pale, z=24, bevel=2)
    C.ball(48, 58, 3.2, Mat('#1a1416', 5, spec=0.7), z=30)
    C.ell(48, 29, 10, 3, 6, dfur, z=22)             # brow
    eyem = Mat('#ffb040', 4, emit=True, glow=2)
    for k in (-1, 1):
        C.ell(48 + k * 9, 32, 2.6, 1.6, 2, Mat('#141018', 4), z=24)
        C.ball(48 + k * 9, 32, 1.2, eyem, z=26)
    # upper fangs over the face
    for x in (40, 43.5, 52.5, 56):
        L = 8 if x in (40, 56) else 5
        C.plate([(x - 1.5, 61), (x + 1.5, 61), (x, 61 + L)], bone, z=28, bevel=0.8)
    C.limb([(30, 84, 1.6, 20), (48, 88, 1.6, 20), (66, 84, 1.6, 20)], K.grip)
    C.ball(48, 87, 3.4, K.acc, z=26)


HELMS = [hm_hood, hm_horned, hm_great, hm_crown, hm_brim, hm_barbute, hm_cap, hm_crown_grand, hm_wolf]


# ================================================================ chest
def torso(C, K, m=None, w=30, waist=22):
    pts = [(48 - w, 20), (48 - 10, 14), (48 + 10, 14), (48 + w, 20), (48 + w - 2, 50), (48 + waist, 86), (48 - waist, 86), (48 - w + 2, 50)]
    C.plate(pts, m or K.body, z=4, bevel=7, dome=1.0)
    C.ell(48, 16, 9, 5, 4, Mat('#141018', 4), z=14)
    return pts


def pauldrons(C, K, m=None):
    for k in (-1, 1):
        C.ell(48 + k * 30, 24, 13, 11, 12, m or K.body, z=10)
        C.ell(48 + k * 30, 30, 12, 4, 6, K.acc, z=16)


def ch_cuirass(C, K):
    torso(C, K)
    C.plate([(30, 22), (66, 22), (64, 56), (48, 62), (32, 56)], K.body, z=10, bevel=5, dome=1.0)
    C.limb([(48, 24, 1.4, 22), (48, 60, 1.4, 22)], K.edge)
    pauldrons(C, K)
    C.plate([(26, 66), (70, 66), (70, 72), (26, 72)], K.grip, z=18, bevel=1.4)
    C.ball(48, 69, 3, K.acc, z=24)
    for i in range(3):
        C.plate([(28 + i * 15, 74), (40 + i * 15, 74), (39 + i * 15, 86), (29 + i * 15, 86)], K.dark, z=12, bevel=1.4)
    if K.glow:
        C.ball(48, 40, 5, K.acc, z=24)
        C.ball(48, 40, 3.2, K.glow, z=28)
    if K.rar >= 4:
        for k in (-1, 1):
            C.limb([(48 + k * 6, 28, 0.9, 24), (48 + k * 14, 40, 0.9, 24), (48 + k * 8, 54, 0.9, 24)], K.acc)


def ch_scale(C, K):
    sc = Mat(PAL[K.g[4]][1], 8, spec=0.5, tex=lambda c: tex_scale(c, 1.2, 3, 3.6))
    torso(C, K, sc)
    pauldrons(C, K, sc)
    C.plate([(26, 66), (70, 66), (70, 72), (26, 72)], K.grip, z=18, bevel=1.4)


def ch_robe(C, K):
    rb = K.v.get('robe')
    if rb in ('diamond', 'vquilt'):
        base = K.body.tex
        if rb == 'diamond':
            q = lambda c: ((np.abs(((c.X + c.Y) % 8) - 4) < 0.7) | (np.abs(((c.X - c.Y) % 8) - 4) < 0.7)) * -4.5
        else:
            q = lambda c: (np.abs((c.X % 6) - 3) < 0.7) * -4.5
        K.body = Mat(PAL[K.g[4]][0], 8, tex=lambda c: q(c) + base(c) * 0.5, light=0.5)
    torso(C, K, w=28, waist=26)
    C.plate([(38, 14), (58, 14), (52, 40), (44, 40)], K.dark, z=12, bevel=2)
    for k in (-1, 1):
        C.ell(48 + k * 28, 26, 10, 10, 10, K.body, z=8)
    for y in (34, 46, 58):
        C.limb([(26, y, 0.6, 14), (70, y, 0.6, 14)], K.dark)
    rb = K.v.get('robe')
    if rb == 'vest':
        for k in (-1, 1):
            C.ell(48 + k * 28, 26, 9, 9, 10, Mat('#c8b898', 6), z=10)
            C.plate([(48 + k * 8, 40), (48 + k * 20, 40), (48 + k * 20, 52), (48 + k * 8, 52)], K.dark, z=16, bevel=1.4)
            C.limb([(48 + k * 8, 40, 0.6, 20), (48 + k * 20, 40, 0.6, 20)], K.acc)
        C.limb([(48, 20, 0.8, 18), (48, 84, 0.8, 18)], K.dark)
    elif rb == 'laced':
        C.ell(48, 20, 22, 7, 8, Mat('#c8b8a0', 7, tex=lambda c: tex_strands(c, 90, 1.0, 7, 300, 3)), z=16)
        for y in range(28, 60, 6):
            C.limb([(44, y, 0.7, 20), (52, y + 3, 0.7, 20)], K.grip)
            C.limb([(52, y, 0.7, 20), (44, y + 3, 0.7, 20)], K.grip)
    elif rb == 'sash':
        C.plate([(24, 22), (34, 18), (74, 70), (66, 76)], Mat('#8a2a34', 7), z=20, bevel=2)
    elif rb == 'ranger':
        C.plate([(20, 18), (76, 18), (70, 34), (26, 34)], Mat('#3a5a2a', 7, tex=lambda c: tex_strands(c, 100, 0.8, 5, 300, 3)), z=18, bevel=3)
        C.ball(48, 30, 3.2, Mat('#c8a040', 6, spec=0.6), z=24)
    elif rb == 'frost':
        for (x, y) in ((34, 34), (60, 44), (40, 56), (58, 26)):
            for a in range(3):
                ang = a * math.pi / 3
                C.limb([(x - math.cos(ang) * 3, y - math.sin(ang) * 3, 0.5, 20), (x + math.cos(ang) * 3, y + math.sin(ang) * 3, 0.5, 20)],
                       K.glow or K.acc)
    if rb != 'sash':
        C.plate([(24, 62), (72, 62), (72, 69), (24, 69)], K.grip, z=18, bevel=1.4)
        C.plate([(44, 61), (52, 61), (52, 70), (44, 70)], K.acc, z=22, bevel=1)
    if K.glow:
        C.ball(48, 28, 2.6, K.glow, z=20)


def ch_banded(C, K):
    torso(C, K, K.dark)
    for i in range(6):
        y = 24 + i * 9
        C.plate([(22 + i * 0.6, y), (74 - i * 0.6, y), (72 - i, y + 7), (24 + i, y + 7)], K.body, z=10 + i, bevel=2, tilt=(-0.2, -0.5))
        C.ball(26 + i, y + 3.5, 1.2, K.acc, z=20 + i)
        C.ball(70 - i, y + 3.5, 1.2, K.acc, z=20 + i)
    pauldrons(C, K)


def ch_carapace(C, K):
    sh = Mat(PAL[K.g[4]][0], 8, spec=0.8, gloss=0.7)
    torso(C, K, K.dark)
    for (pts) in ([(26, 20), (46, 18), (44, 50), (28, 46)], [(50, 18), (70, 20), (68, 46), (52, 50)],
                  [(30, 52), (46, 54), (44, 70), (32, 66)], [(50, 54), (66, 52), (64, 66), (52, 70)],
                  [(36, 72), (60, 72), (56, 86), (40, 86)]):
        C.plate(pts, sh, z=12, bevel=3, dome=0.8, tilt=(-0.3, -0.3))
    for k in (-1, 1):
        C.plate([(48 + k * 20, 18), (48 + k * 38, 8), (48 + k * 34, 30)], sh, z=14, bevel=2)
    if K.glow:
        C.limb([(30, 22, 0.8, 20), (40, 36, 0.8, 20), (36, 44, 0.8, 20), (52, 60, 0.8, 20),
                (48, 66, 0.8, 20), (62, 82, 0.8, 20)], K.glow)


CHESTS = [ch_cuirass, ch_scale, ch_robe, ch_banded, ch_carapace]


# ================================================================ boots
def boot(C, K, cx, z, dy=0, shaft_h=40, metal=False, cuff=False, laces=True, sandal=False, far=False):
    m = K.body if not far else Mat(PAL[K.g[4]][0], 7, dark=0.9, light=0.3, tex=K.body.tex)
    sole = Mat('#2a221e', 6)
    gy = 90 + dy
    if sandal:
        C.plate([(cx - 12, gy - 6), (cx + 22, gy - 6), (cx + 23, gy), (cx - 13, gy)], K.wood, z=z, bevel=1.4)
        C.limb([(cx - 2, gy - 50, 6, z + 2), (cx - 1, gy - 22, 5.5, z + 2)], Mat('#c8a07a', 7))
        C.ell(cx + 6, gy - 10, 15, 6, 6, Mat('#c8a07a', 7), z=z + 3)
        for y in range(int(gy - 46), int(gy - 8), 6):
            C.limb([(cx - 8, y, 1.2, z + 10), (cx + 6, y + 3, 1.2, z + 10)], K.grip)
        return
    top = gy - 18 - shaft_h
    # shaft: a rounded tube, slightly flared at the top
    C.plate([(cx - 11, top), (cx + 9, top), (cx + 8, gy - 20), (cx - 10, gy - 16)], m, z=z, bevel=7, dome=1.6)
    # foot: instep, rounded toe, heel
    C.ell(cx + 5, gy - 9, 13, 6.5, 8, m, z=z + 2)
    C.ell(cx + 15, gy - 6.5, 7, 4.2, 6, m, z=z + 3)
    C.ell(cx - 7, gy - 8, 5, 5.5, 6, m, z=z + 1)
    # sole with tread
    C.plate([(cx - 13, gy - 4), (cx + 25, gy - 4), (cx + 24, gy + 1), (cx - 13, gy + 1)], sole, z=z + 6, bevel=1.0)
    for x in range(int(cx - 10), int(cx + 24), 4):
        C.dot(x, gy, (12, 10, 10))
    C.plate([(cx - 13, gy - 6), (cx - 2, gy - 6), (cx - 2, gy + 1), (cx - 13, gy + 1)], sole, z=z + 7, bevel=1.0)
    if metal:
        for y in range(int(top + 4), int(gy - 20), 7):
            C.plate([(cx - 11, y), (cx + 9, y), (cx + 9, y + 5), (cx - 11, y + 5)], m, z=z + 6, bevel=1.4, tilt=(-0.2, -0.6))
            C.ball(cx + 7, y + 2.5, 0.9, K.acc, z=z + 10)
        C.ell(cx - 1, top + shaft_h * 0.62, 7, 6, 6, K.acc, z=z + 10)
        if K.glow:
            C.ball(cx - 1, top + shaft_h * 0.62, 2.8, K.glow, z=z + 14)
        C.plate([(cx + 10, gy - 11), (cx + 20, gy - 9), (cx + 22, gy - 4), (cx + 10, gy - 4)], K.acc, z=z + 8, bevel=1.4)
    if laces:
        for y in range(int(top + 6), int(gy - 12), 5):
            C.ball(cx + 7, y, 0.9, K.acc, z=z + 9)
            C.limb([(cx + 1, y + 2, 0.7, z + 10), (cx + 8, y - 1, 0.7, z + 10)], K.grip)
        C.limb([(cx + 8, top + 6, 0.6, z + 10), (cx + 13, top + 12, 0.6, z + 10)], K.grip)
    if cuff:
        C.ell(cx - 1, top + 2, 13, 5.5, 8, K.grip if not metal else K.acc, z=z + 8)
        if K.rar >= 4:
            for k in (-1, 1):
                C.plate([(cx + k * 10, top), (cx + k * 21, top - 12), (cx + k * 14, top + 6)], K.acc, z=z + 9, bevel=1.4)
    # a stitched seam down the back and a buckle at the ankle
    C.limb([(cx - 9, top + 4, 0.5, z + 9), (cx - 9, gy - 16, 0.5, z + 9)], K.dark)
    C.plate([(cx - 4, gy - 22), (cx + 3, gy - 22), (cx + 3, gy - 18), (cx - 4, gy - 18)], K.acc, z=z + 10, bevel=0.8)


def pair(C, K, **kw):
    boot(C, K, 44, -8, dy=-4, far=True, **kw)
    boot(C, K, 28, 10, **kw)


def sh_trail(C, K):
    pair(C, K, shaft_h=34)


def sh_greaves(C, K):
    pair(C, K, shaft_h=44, metal=True, laces=False)


def sh_sandals(C, K):
    pair(C, K, sandal=True)


def sh_cuffed(C, K):
    pair(C, K, shaft_h=38, cuff=True, laces=K.g[4] != 'wood', metal=K.g[6] == 'metal')


SHOES = [sh_trail, sh_greaves, sh_sandals, sh_cuffed]
TABLE = {'staff': STAFFS, 'shield': SHIELDS, 'helm': HELMS, 'chest': CHESTS, 'shoes': SHOES}


def piece(g):
    C = Canvas(); K = Kit(g); C.kit = K
    if g[1] == 'sword':
        SWORDS[g[3]](C, K)
        if g[0] == "Oathbreaker's Dawn":
            # the legendary: the blade itself holds light
            base = (30, 66)
            blade(C, K, base, 62, lambda t: 1.6 * (1 - t ** 3), lambda t: 1.0 * (1 - t ** 3))
            for t in np.linspace(0.1, 0.9, 6):
                x, y = at(base, t * 62, 0.2)
                C.ball(x, y, 1.0, K.glow, z=20)
        return C
    if g[1] in TABLE and g[3] < len(TABLE[g[1]]):
        TABLE[g[1]][g[3]](C, K)
        return C
    return None


def build(cats):
    return [(g, piece) for g in GEAR if g[1] in cats]
