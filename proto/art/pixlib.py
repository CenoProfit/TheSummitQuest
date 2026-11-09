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
N = 64

# ---------------------------------------------------------------- canvas
def blank():
    return [['.' for _ in range(N)] for _ in range(N)]

def put(g, x, y, ch):
    x = int(round(x)); y = int(round(y))
    if 0 <= x < N and 0 <= y < N:
        g[y][x] = ch

def get(g, x, y):
    x = int(round(x)); y = int(round(y))
    return g[y][x] if 0 <= x < N and 0 <= y < N else '.'

# ------------------------------------------------------------ primitives
def rect(g, x0, y0, x1, y1, ch):
    for y in range(int(min(y0,y1)), int(max(y0,y1)) + 1):
        for x in range(int(min(x0,x1)), int(max(x0,x1)) + 1):
            put(g, x, y, ch)

def disc(g, cx, cy, r, ch):
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                put(g, x, y, ch)

def ring(g, cx, cy, r, t, ch):
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            dd = (x - cx) ** 2 + (y - cy) ** 2
            if (r - t) ** 2 <= dd <= r * r:
                put(g, x, y, ch)

def ellipse(g, cx, cy, rx, ry, ch):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                put(g, x, y, ch)

def poly(g, pts, ch):
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
                put(g, x, y, ch)

def line(g, x0, y0, x1, y1, ch, w=1):
    steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
    h = (w - 1) / 2.0
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
        for dy in range(int(-h), int(h) + 1):
            for dx in range(int(-h), int(h) + 1):
                put(g, x + dx, y + dy, ch)

def line_on(g, x0, y0, x1, y1, ch, only):
    """rule a line but only over pixels already holding `only`"""
    steps = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 1
    for i in range(steps + 1):
        t = i / steps
        x = int(round(x0 + (x1 - x0) * t)); y = int(round(y0 + (y1 - y0) * t))
        if 0 <= x < N and 0 <= y < N and g[y][x] == only:
            g[y][x] = ch

def erase(g, pts): poly(g, pts, '.')

# --------------------------------------------------------------- shaping
def _perp(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    L = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    return -dy / L, dx / L

def taper(g, x0, y0, x1, y1, w0, w1, ch):
    """a quad from (x0,y0) width w0 to (x1,y1) width w1"""
    px, py = _perp(x0, y0, x1, y1)
    poly(g, [(x0 + px * w0 / 2, y0 + py * w0 / 2), (x1 + px * w1 / 2, y1 + py * w1 / 2),
             (x1 - px * w1 / 2, y1 - py * w1 / 2), (x0 - px * w0 / 2, y0 - py * w0 / 2)], ch)

def blade(g, x0, y0, x1, y1, wbase, wtip=1.5, point=6, edge='W', body='A', back='d'):
    """A tapered blade from base to tip, lit on its upper-left edge.
       `point` is how many pixels of the tip are brought to a spike."""
    L = max(1e-6, ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    sx, sy = x1 - ux * point, y1 - uy * point
    taper(g, x0, y0, sx, sy, wbase, wtip + (wbase - wtip) * 0.15, body)
    px, py = _perp(x0, y0, x1, y1)
    poly(g, [(sx + px * wtip / 2, sy + py * wtip / 2), (x1, y1),
             (sx - px * wtip / 2, sy - py * wtip / 2)], body)
    # the two long edges: light on the side the lamp is on, shadow opposite
    lit = 1 if (px - py) > 0 else -1
    for k, ch in ((lit, edge), (-lit, back)):
        line_on(g, x0 + px * k * wbase * 0.42, y0 + py * k * wbase * 0.42,
                   x1 + px * k * wtip * 0.30, y1 + py * k * wtip * 0.30, ch, body)

def fuller(g, x0, y0, x1, y1, ch='d', inset=0.16):
    """the blood groove down the middle of a blade"""
    L = max(1e-6, ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    line_on(g, x0 + ux * L * inset, y0 + uy * L * inset,
               x1 - ux * L * inset, y1 - uy * L * inset, ch, 'A')

def haft(g, x0, y0, x1, y1, w, mid='G', lite='H', dark='g'):
    """a wooden or leather shaft, lit along its upper-left side"""
    taper(g, x0, y0, x1, y1, w, w, mid)
    px, py = _perp(x0, y0, x1, y1)
    lit = 1 if (px - py) > 0 else -1
    line_on(g, x0 + px * lit * w * 0.34, y0 + py * lit * w * 0.34,
               x1 + px * lit * w * 0.34, y1 + py * lit * w * 0.34, lite, mid)
    line_on(g, x0 - px * lit * w * 0.36, y0 - py * lit * w * 0.36,
               x1 - px * lit * w * 0.36, y1 - py * lit * w * 0.36, dark, mid)

def wrap(g, x0, y0, x1, y1, w, n=5, ch='g'):
    """binding bands across a grip"""
    px, py = _perp(x0, y0, x1, y1)
    for i in range(n):
        t = (i + 0.5) / n
        cx = x0 + (x1 - x0) * t; cy = y0 + (y1 - y0) * t
        line_on(g, cx + px * w * 0.6, cy + py * w * 0.6,
                   cx - px * w * 0.6, cy - py * w * 0.6, ch, 'G')
        line_on(g, cx + px * w * 0.6, cy + py * w * 0.6,
                   cx - px * w * 0.6, cy - py * w * 0.6, ch, 'H')

def stud(g, cx, cy, r=1.6, ch='C', hi='W'):
    disc(g, cx, cy, r, ch)
    put(g, cx - r * 0.4, cy - r * 0.4, hi)

# ----------------------------------------------------------------- finish
def outline(g, ch='o'):
    """1px ink line, eaten inward so the sprite does not grow"""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            if g[y][x] == '.':
                continue
            for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= N or ny >= N or g[ny][nx] == '.':
                    out[y][x] = ch
                    break
    return out

def rimlight(g, body='A', ch='B'):
    """lift the upper-left inside edge of every mass by one pixel"""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            if g[y][x] != body:
                continue
            if get(g, x - 1, y) in ('.', 'o') or get(g, x, y - 1) in ('.', 'o'):
                out[y][x] = ch
    return out

def shadeform(g, body='A', lo='d', hi='B'):
    """3 step ramp across each mass: upper-left lights, lower-right shades"""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            if g[y][x] != body:
                continue
            up = get(g, x, y - 1) in ('.', 'o') or get(g, x, y - 2) in ('.', 'o')
            lf = get(g, x - 1, y) in ('.', 'o')
            dn = get(g, x, y + 1) in ('.', 'o') or get(g, x, y + 2) in ('.', 'o')
            rt = get(g, x + 1, y) in ('.', 'o')
            if up or lf:   out[y][x] = hi
            elif dn or rt: out[y][x] = lo
    return out

def despeckle(g):
    """remove lone pixels with no orthogonal neighbour of their own kind"""
    out = [row[:] for row in g]
    for y in range(N):
        for x in range(N):
            c = g[y][x]
            if c == '.':
                continue
            if all(get(g, x+dx, y+dy) != c for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
                out[y][x] = get(g, x+1, y) if get(g, x+1, y) != '.' else '.'
    return out

ALLOWED = set('.odABWCcgGH')
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
