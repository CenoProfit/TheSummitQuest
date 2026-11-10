# -*- coding: utf-8 -*-
"""64x64 pixel-art composition library for Summit Quest gear sprites.

TONE RAMP (these are the only characters allowed in a sprite):
  .  transparent
  o  outline, the dark ink line around everything
  d  body shadow        A  body mid        B  body light     W  body highlight
  c  accent shadow      C  accent          (brass, gem, trim, glow)
  g  grip shadow        G  grip mid        H  grip light     (wood / leather)

The palette behind those letters is chosen per item at runtime, so one
shape becomes many items. Author the FORM, never the colour.

HOUSE STYLE, taken from the reference art:
  * Hard edges. No gradients, no anti-aliasing, no stray single pixels.
  * Every shape is wrapped in a 1px `o` outline. outline() does this.
  * Light comes from the upper left. Upper-left faces take B/W,
    lower-right faces take d. A is everything in between.
  * Blades run DIAGONALLY, lower-left to upper-right, tip in the corner.
  * Brass (C) at the guard, the pommel, the ferrule, the trim.
  * Fill the frame. A 64x64 sprite with a 30px object in the middle has
    thrown away three quarters of its resolution.
"""
N = 96
K = N / 64.0          # builders are written in a 64 unit space and scaled up

def setsize(n):
    global N, K
    N = n; K = n / 64.0

# ---------------------------------------------------------------- canvas
def blank():
    return [['.' for _ in range(N)] for _ in range(N)]

def put(g, x, y, ch, raw=False):
    if not raw:
        x *= K; y *= K
    x = int(round(x)); y = int(round(y))
    if 0 <= x < N and 0 <= y < N:
        g[y][x] = ch

def get(g, x, y, raw=True):
    if not raw:
        x *= K; y *= K
    x = int(round(x)); y = int(round(y))
    return g[y][x] if 0 <= x < N and 0 <= y < N else '.'

# ------------------------------------------------------------ primitives
# Builders are written in a 64 unit space. Every primitive converts its
# arguments to canvas pixels on the way in and then works in whole
# pixels, so raising N raises the detail instead of punching holes.

def _s(v): return v * K

def rect(g, x0, y0, x1, y1, ch):
    x0, y0, x1, y1 = _s(x0), _s(y0), _s(x1), _s(y1)
    for y in range(int(round(min(y0, y1))), int(round(max(y0, y1))) + 1):
        for x in range(int(round(min(x0, x1))), int(round(max(x0, x1))) + 1):
            put(g, x, y, ch, True)

def disc(g, cx, cy, r, ch):
    cx, cy, r = _s(cx), _s(cy), _s(r)
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                put(g, x, y, ch, True)

def ring(g, cx, cy, r, t, ch):
    cx, cy, r, t = _s(cx), _s(cy), _s(r), _s(t)
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            dd = (x - cx) ** 2 + (y - cy) ** 2
            if (r - t) ** 2 <= dd <= r * r:
                put(g, x, y, ch, True)

def ellipse(g, cx, cy, rx, ry, ch):
    cx, cy, rx, ry = _s(cx), _s(cy), _s(rx), _s(ry)
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                put(g, x, y, ch, True)

def poly(g, pts, ch):
    pts = [(_s(p[0]), _s(p[1])) for p in pts]
    ys = [p[1] for p in pts]
    for y in range(int(min(ys)) - 1, int(max(ys)) + 2):
        xs = []
        for i in range(len(pts)):
            x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % len(pts)]
            if (y0 <= y < y1) or (y1 <= y < y0):
                xs.append(x0 + (x1 - x0) * (y - y0) / (y1 - y0))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            for x in range(int(round(xs[i])), int(round(xs[i + 1])) + 1):
                put(g, x, y, ch, True)

def line(g, x0, y0, x1, y1, ch, w=1):
    x0, y0, x1, y1, w = _s(x0), _s(y0), _s(x1), _s(y1), max(1.0, _s(w))
    steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
    h = (w - 1) / 2.0
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        for dy in range(int(-h), int(h) + 1):
            for dx in range(int(-h), int(h) + 1):
                put(g, x + dx, y + dy, ch, True)

def line_on(g, x0, y0, x1, y1, ch, only, w=1):
    """rule a line but only over pixels already holding `only`"""
    x0, y0, x1, y1, w = _s(x0), _s(y0), _s(x1), _s(y1), max(1.0, _s(w))
    steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
    h = (w - 1) / 2.0
    for i in range(steps + 1):
        t = i / steps
        for dy in range(int(-h), int(h) + 1):
            for dx in range(int(-h), int(h) + 1):
                x = int(round(x0 + (x1 - x0) * t)) + dx
                y = int(round(y0 + (y1 - y0) * t)) + dy
                if 0 <= x < N and 0 <= y < N and g[y][x] == only:
                    g[y][x] = ch

def erase(g, pts): poly(g, pts, '.')

# --------------------------------------------------------------- shaping
def _perp(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    L = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    return -dy / L, dx / L

def taper(g, x0, y0, x1, y1, w0, w1, ch):
    px, py = _perp(x0, y0, x1, y1)
    poly(g, [(x0 + px * w0 / 2, y0 + py * w0 / 2), (x1 + px * w1 / 2, y1 + py * w1 / 2),
             (x1 - px * w1 / 2, y1 - py * w1 / 2), (x0 - px * w0 / 2, y0 - py * w0 / 2)], ch)

def blade(g, x0, y0, x1, y1, wbase, wtip=1.5, point=6, edge='W', body='A', back='d'):
    """A tapered blade from base to tip, lit on its upper-left edge."""
    L = max(1e-6, ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    sx, sy = x1 - ux * point, y1 - uy * point
    taper(g, x0, y0, sx, sy, wbase, wtip + (wbase - wtip) * 0.15, body)
    px, py = _perp(x0, y0, x1, y1)
    poly(g, [(sx + px * wtip / 2, sy + py * wtip / 2), (x1, y1),
             (sx - px * wtip / 2, sy - py * wtip / 2)], body)
    lit = 1 if (px - py) > 0 else -1
    for k, ch, w in ((lit, edge, 1.4), (lit, 'V', 0.7), (-lit, back, 1.6), (-lit, 'q', 0.8)):
        line_on(g, x0 + px * k * wbase * 0.42, y0 + py * k * wbase * 0.42,
                   x1 + px * k * wtip * 0.30, y1 + py * k * wtip * 0.30, ch, body, w)

def fuller(g, x0, y0, x1, y1, ch='d', inset=0.16):
    L = max(1e-6, ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    line_on(g, x0 + ux * L * inset, y0 + uy * L * inset,
               x1 - ux * L * inset, y1 - uy * L * inset, ch, 'A', 1.6)
    px, py = _perp(x0, y0, x1, y1)
    line_on(g, x0 + ux * L * inset + px, y0 + uy * L * inset + py,
               x1 - ux * L * inset + px, y1 - uy * L * inset + py, 'e', 'A', 0.9)

def haft(g, x0, y0, x1, y1, w, mid='G', lite='H', dark='g'):
    taper(g, x0, y0, x1, y1, w, w, mid)
    px, py = _perp(x0, y0, x1, y1)
    lit = 1 if (px - py) > 0 else -1
    line_on(g, x0 + px * lit * w * 0.34, y0 + py * lit * w * 0.34,
               x1 + px * lit * w * 0.34, y1 + py * lit * w * 0.34, lite, mid, 1.3)
    line_on(g, x0 - px * lit * w * 0.36, y0 - py * lit * w * 0.36,
               x1 - px * lit * w * 0.36, y1 - py * lit * w * 0.36, dark, mid, 1.3)
    line_on(g, x0 - px * lit * w * 0.50, y0 - py * lit * w * 0.50,
               x1 - px * lit * w * 0.50, y1 - py * lit * w * 0.50, 'j', mid, 0.9)

def wrap(g, x0, y0, x1, y1, w, n=5, ch='j'):
    px, py = _perp(x0, y0, x1, y1)
    for i in range(n):
        t = (i + 0.5) / n
        cx = x0 + (x1 - x0) * t; cy = y0 + (y1 - y0) * t
        for src in ('G', 'H', 'g'):
            line_on(g, cx + px * w * 0.6, cy + py * w * 0.6,
                       cx - px * w * 0.6, cy - py * w * 0.6, ch, src, 1.1)

def flute(g, x0, y0, x1, y1, n=3, spread=6, body='A', bow=0.0):
    """Parallel grooves down a plate: a dark channel with a lit ridge
       beside it, which is what makes a breastplate read as hammered
       steel rather than as a flat shape."""
    for i in range(n):
        t = (i - (n - 1) / 2.0) / max(1, (n - 1) / 2.0)
        ox = t * spread
        mid = bow * (1 - abs(t))
        line_on(g, x0 + ox, y0, x1 + ox + mid, y1, 'd', body, 1.2)
        line_on(g, x0 + ox + 1.2, y0, x1 + ox + mid + 1.2, y1, 'B', body, 0.9)

def folds(g, x0, x1, y0, y1, n=5, body='A'):
    """Cloth drapery: a soft shadow and a lift, paired, wandering a
       little so it does not read as corduroy."""
    for i in range(n):
        t = (i + 0.5) / n
        x = x0 + (x1 - x0) * t
        sway = 1.4 * (1 if i % 2 else -1)
        line_on(g, x, y0, x + sway, y1, 'e', body, 1.1)
        line_on(g, x + 1.3, y0, x + sway + 1.3, y1, 'B', body, 0.8)
        line_on(g, x, y0 + (y1 - y0) * 0.55, x + sway, y1, 'd', body, 0.8)

def lames(g, x0, x1, y0, y1, n=5, body='A', rivet='C'):
    """Horizontal plate bands with a real gap between them, a lit top
       edge on each, and a rivet at either end."""
    for i in range(n):
        y = y0 + (y1 - y0) * (i + 1) / float(n + 1)
        line_on(g, x0, y, x1, y, 'q', body, 1.1)
        line_on(g, x0, y - 1.1, x1, y - 1.1, 'W', body, 0.9)
        if rivet:
            stud(g, x0 + 2.0, y - 2.0, 1.2, rivet)
            stud(g, x1 - 2.0, y - 2.0, 1.2, rivet)

def scales(g, x0, x1, y0, y1, step=3.4, r=1.9, body='A'):
    """An overlapping scale field, each scale lit on its crown and
       shadowed where the one below tucks under it."""
    rows = int((y1 - y0) / step)
    for row in range(rows + 1):
        y = y0 + row * step
        off = step / 2.0 if row % 2 else 0.0
        x = x0 + off
        while x <= x1:
            disc(g, x, y, r, body)
            put(g, x - r * 0.4, y - r * 0.5, 'W')
            put(g, x, y + r * 0.6, 'd')
            put(g, x - r, y + r * 0.5, 'q')
            x += step

def pauldron(g, cx, cy, k, w=11, h=7, body='A', trim='C', plates=3):
    """A layered shoulder. k is -1 for his left, +1 for his right; the
       two are deliberately not identical, because a matched pair of
       perfect arcs is the thing that reads as machine made."""
    for i in range(plates):
        f = 1.0 - i * 0.22
        poly(g, [(cx + k * 2, cy + i * (h * 0.42)),
                 (cx + k * w * f, cy + i * (h * 0.42) + h * 0.22 * f),
                 (cx + k * w * f * 0.92, cy + i * (h * 0.42) + h * f),
                 (cx + k * 2, cy + i * (h * 0.42) + h * 0.86 * f)], body)
    if trim:
        poly(g, [(cx + k * 3, cy), (cx + k * w, cy + h * 0.22),
                 (cx + k * w, cy + h * 0.44), (cx + k * 3, cy + h * 0.22)], trim)
        stud(g, cx + k * (w - 2), cy + h * 0.30, 1.3, trim)

def strap(g, x0, y0, x1, y1, w=3.0, buckle=True):
    taper(g, x0, y0, x1, y1, w, w, 'G')
    line_on(g, x0, y0 - w * 0.3, x1, y1 - w * 0.3, 'H', 'G', 0.9)
    line_on(g, x0, y0 + w * 0.4, x1, y1 + w * 0.4, 'j', 'G', 0.9)
    if buckle:
        mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        rect(g, mx - 2.0, my - 2.0, mx + 2.0, my + 2.0, 'C')
        rect(g, mx - 0.8, my - 0.8, mx + 0.8, my + 0.8, 'x')

def gorget(g, cx, y, w=11, h=4, ch='C'):
    poly(g, [(cx - w, y), (cx + w, y), (cx + w * 0.88, y + h), (cx - w * 0.88, y + h)], ch)
    line_on(g, cx - w, y + 0.8, cx + w, y + 0.8, 'Z', ch, 0.9)
    line_on(g, cx - w * 0.9, y + h - 0.8, cx + w * 0.9, y + h - 0.8, 'x', ch, 0.9)

def stud(g, cx, cy, r=1.6, ch='C', hi='Z'):
    disc(g, cx, cy, r, ch)
    disc(g, cx - r * 0.28, cy - r * 0.28, r * 0.45, hi)
    line_on(g, cx - r*0.2, cy + r*0.55, cx + r*0.7, cy + r*0.1, 'x', ch, 1.0)

# ----------------------------------------------------------------- finish
# Three families, each a ramp from dark to light. A builder places the
# MID tone of a family ('A', 'C', 'G') to mean "this is made of that",
# and anything else it places is an explicit artist override that the
# modelling pass leaves alone.
BODY = 'qdeABWV'
ACC  = 'xcCYZ'
GRIP = 'jgGHK'
SKIN = 'umM'        # only the character uses this one
FAM  = {}
for _f in (BODY, ACC, GRIP, SKIN):
    for _i, _c in enumerate(_f):
        FAM[_c] = (_f, _i)
MID = {BODY: 3, ACC: 2, GRIP: 2, SKIN: 1}
ALLOWED = set('.on' + BODY + ACC + GRIP + SKIN)

def shift(ch, k):
    f = FAM.get(ch)
    if not f: return ch
    fam, i = f
    return fam[max(0, min(len(fam) - 1, i + k))]

def _run(g, x, y, dx, dy, fam):
    n = 0
    while True:
        x += dx; y += dy; n += 1
        if not (0 <= x < N and 0 <= y < N): return n
        c = g[y][x]
        if c not in FAM or FAM[c][0] is not fam: return n
        if n > N: return n

def model(g):
    """Light the form. Every pixel a builder left at its family's mid
       tone gets a tone chosen from where it sits inside its own mass:
       top-left faces catch the lamp, the underside falls away. This is
       what separates a painted object from a flat fill."""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            c = g[y][x]
            f = FAM.get(c)
            if not f or f[1] != MID[f[0]]: continue
            fam = f[0]
            up = _run(g, x, y, 0, -1, fam); dn = _run(g, x, y, 0, 1, fam)
            lf = _run(g, x, y, -1, 0, fam); rt = _run(g, x, y, 1, 0, fam)
            tv = up / float(up + dn); th = lf / float(lf + rt)
            lvl = (len(fam) - 1) * 0.86 - (len(fam) - 1) * 0.62 * tv - (len(fam) - 1) * 0.26 * th
            out[y][x] = fam[max(0, min(len(fam) - 1, int(round(lvl))))]
    return out

def ao(g, depth=2):
    """Contact shadow. A pixel sitting against the outline, or against a
       DIFFERENT material, loses a step or two. Without this every joint
       in the sprite reads as a sticker laid on top of another sticker."""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            c = g[y][x]
            f = FAM.get(c)
            if not f: continue
            k = 0
            for dx, dy in ((1, 0), (0, 1), (1, 1), (-1, 1)):
                n = get(g, x + dx, y + dy)
                if n == '.' or n == 'o': k = max(k, 1)
                elif n in FAM and FAM[n][0] is not f[0]: k = max(k, depth)
            for dx, dy in ((-1, 0), (0, -1)):
                n = get(g, x + dx, y + dy)
                if n in FAM and FAM[n][0] is not f[0]: k = max(k, depth)
            if k: out[y][x] = shift(c, -k)
    return out

def rim(g):
    """and the opposite: the top-left lip of every mass takes the light"""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            c = g[y][x]
            if c not in FAM: continue
            if get(g, x, y - 1) in ('.', 'o') or get(g, x - 1, y) in ('.', 'o'):
                out[y][x] = shift(c, 1)
    return out

def dither(g):
    """Break the banding where two tones meet, on a checker, so the
       gradient reads as a surface rather than as contour lines."""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            if (x + y) % 2: continue
            c = g[y][x]
            f = FAM.get(c)
            if not f: continue
            for dx, dy in ((1, 0), (0, 1)):
                n = get(g, x + dx, y + dy)
                nf = FAM.get(n)
                if nf and nf[0] is f[0] and abs(nf[1] - f[1]) >= 2:
                    out[y][x] = shift(c, 1 if nf[1] > f[1] else -1)
                    break
    return out

def _h(a, b):
    v = (a * 374761393 + b * 668265263) & 0xFFFFFFFF
    v = (v ^ (v >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((v ^ (v >> 16)) & 0xFFFF) / 65535.0

def wear(g, amount=0.16):
    """Nicks and scuffs, deterministic so a rebuild is identical. Only
       near an edge, because that is where a real object wears."""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            c = g[y][x]
            if c not in FAM: continue
            edge = any(get(g, x + dx, y + dy) in ('.', 'o')
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if not edge: continue
            r = _h(x, y)
            if r < amount * 0.55:   out[y][x] = shift(c, -1)
            elif r > 1 - amount * 0.45: out[y][x] = shift(c, 1)
    return out

def outline(g, ch='o'):
    """1px ink line, eaten inward so the sprite does not grow"""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            if g[y][x] == '.': continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= N or ny >= N or g[ny][nx] == '.':
                    out[y][x] = ch; break
    return out

def softline(g):
    """one ring in from the ink, a softer dark, so the edge has weight"""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            c = g[y][x]
            if c not in FAM: continue
            if any(get(g, x + dx, y + dy) == 'o'
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = shift(c, -1)
    return out

def despeckle(g):
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            c = g[y][x]
            if c == '.': continue
            if all(get(g, x + dx, y + dy) != c for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = get(g, x + 1, y) if get(g, x + 1, y) != '.' else '.'
    return out

# kept so the existing builders keep working; model() supersedes it
def shadeform(g, body='A', lo='d', hi='B'): return g
def rimlight(g, body='A', ch='B'): return g

def paint(g, worn=0.16):
    """the whole finishing run, in the order that matters"""
    g = model(g)
    g = ao(g)
    g = rim(g)
    g = dither(g)
    if worn: g = wear(g, worn)
    g = despeckle(g)
    g = outline(g)
    g = softline(g)
    return g

def dump(g):
    rows = [''.join(r) for r in g]
    assert len(rows) == N, len(rows)
    for i, r in enumerate(rows):
        assert len(r) == N, (i, len(r))
        bad = set(r) - ALLOWED
        assert not bad, (i, bad)
    return rows

def show(rows): print('\n'.join(rows))

def js(rows, per=2, indent='  '):
    out = []
    for j in range(0, len(rows), per):
        out.append(','.join('"%s"' % x for x in rows[j:j + per]))
    return '[\n' + indent + (',\n' + indent).join(out) + ']'
