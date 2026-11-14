# -*- coding: utf-8 -*-
"""A small 2.5D renderer for full colour pixel sprites.

The letter sprites (pixlib.py) are one shape with a palette swapped in,
which is how 40 shapes became 115 pieces, and why none of them can look
like the bosses: a hand drawn boss carries sixty colours chosen for that
one creature. This builds a sprite the way a pixel artist shades one,
only from code:

  * The form is modelled, not outlined. A creature is a stack of
    ellipsoids, capsules and bevelled plates, each with depth, so every
    pixel knows which way it faces and what is in front of it.
  * Light comes from the upper left. Each material has its own ramp of
    six to eight tones, and the ramp is hue shifted the way painters do
    it: shadows lean cool and lose saturation, lights lean warm.
  * The surface carries a pattern per material (fur, feather, scale,
    stone, metal, skin, bark, crystal) that moves the tone index rather
    than painting colour on top, so it is shaded with the form.
  * Selective outline: the silhouette takes the darkest tone of the
    material it bounds, and parts that overlap get a dark seam where
    the nearer one passes over the further one.
  * Emissive materials ignore the light and throw a glow onto what is
    around them.
  * Stray single pixels are cleaned away at the end.

Everything is quantised to the ramps, nothing is blended, so the result
is crisp pixel art at its native size.
"""
import math
import numpy as np

N = 96
LIGHT = np.array([-0.58, -0.74, 0.42]); LIGHT /= np.linalg.norm(LIGHT)
RIM = np.array([0.80, -0.25, 0.25]); RIM /= np.linalg.norm(RIM)


# ------------------------------------------------------------------ colour
def _hsl(c):
    import colorsys
    r, g, b = [v / 255.0 for v in c]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l


def _rgb(h, s, l):
    import colorsys
    r, g, b = colorsys.hls_to_rgb(h % 1.0, max(0, min(1, l)), max(0, min(1, s)))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def ramp(base, n=7, dark=0.80, light=0.55, cool=0.09, warm=0.05, sat=1.0):
    """n tones from deep shadow to highlight around a base colour.

       The base sits a little above the middle. Going down, lightness
       falls, the hue drifts toward blue violet and saturation dips; going
       up, it lifts and drifts toward yellow and loses a little
       saturation, the way a lit surface bleaches."""
    h, s, l = _hsl(hexc(base) if isinstance(base, str) else base)
    s *= sat
    out = []
    mid = int(n * 0.55)
    for i in range(n):
        if i <= mid:
            t = (mid - i) / max(1, mid)          # 0 at base, 1 at deepest
            ll = l * (1 - dark * t) + 0.02 * t
            hh = _toward(h, 0.70, cool * t)
            ss = s * (1 - 0.25 * t) + 0.10 * t
        else:
            t = (i - mid) / max(1, n - 1 - mid)
            ll = l + (1 - l) * light * t
            hh = _toward(h, 0.14, warm * t)
            ss = s * (1 - 0.30 * t)
        out.append(_rgb(hh, ss, ll))
    return out


def _toward(h, target, amt):
    d = ((target - h + 0.5) % 1.0) - 0.5
    return h + d * amt


class Mat:
    def __init__(self, base, n=7, tex=None, emit=False, glow=0.0, spec=0.0, gloss=0.0,
                 tones=None, **rk):
        self.ramp = tones or ramp(base, n, **rk)
        self.n = len(self.ramp)
        self.tex = tex
        self.emit = emit
        self.glow = glow          # how far it lights its surroundings, in px
        self.spec = spec          # strength of a hard specular
        self.gloss = gloss


# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, n=N):
        self.n = n
        self.z = np.full((n, n), -1e9)
        self.mat = np.full((n, n), -1, dtype=int)
        self.part = np.full((n, n), -1, dtype=int)
        self.nrm = np.zeros((n, n, 3)); self.nrm[..., 2] = 1
        self.u = np.zeros((n, n)); self.v = np.zeros((n, n))
        self.bias = np.zeros((n, n))      # hand placed shade offsets
        self.mats = []
        self.parts = 0
        yy, xx = np.mgrid[0:n, 0:n]
        self.X = xx + 0.5; self.Y = yy + 0.5
        self.over = {}                    # (y,x) -> rgb, painted last

    def m(self, mat):
        if mat not in self.mats:
            self.mats.append(mat)
        return self.mats.index(mat)

    def _write(self, mask, z, nrm, mat, u=None, v=None, top=False):
        pid = self.parts; self.parts += 1
        if top:
            z = np.where(mask, 1e6 + pid, -1e9)
        w = mask & (z > self.z)
        self.z[w] = z[w]
        self.mat[w] = self.m(mat)
        self.part[w] = pid
        self.nrm[w] = nrm[w]
        if u is not None:
            self.u[w] = u[w]; self.v[w] = v[w]
        return pid

    # ellipsoid, axis aligned or rotated in the picture plane
    def ell(self, cx, cy, rx, ry, rz, mat, z=0.0, rot=0.0, top=False, flat=1.0):
        ca, sa = math.cos(rot), math.sin(rot)
        dx = self.X - cx; dy = self.Y - cy
        lx = dx * ca + dy * sa; ly = -dx * sa + dy * ca
        d2 = (lx / rx) ** 2 + (ly / ry) ** 2
        mask = d2 <= 1.0
        h = np.sqrt(np.clip(1 - d2, 0, 1))
        nx_l = lx / rx; ny_l = ly / ry
        nz = h * flat + 1e-3
        nx = nx_l * ca - ny_l * sa; ny = nx_l * sa + ny_l * ca
        nrm = np.stack([nx, ny, nz], -1)
        nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True)
        return self._write(mask, z + rz * h, nrm, mat, lx / rx, ly / ry, top)

    def ball(self, cx, cy, r, mat, z=0.0, **k):
        return self.ell(cx, cy, r, r, r, mat, z, **k)

    def limb(self, pts, mat, z=0.0, steps=None):
        """a tapered capsule through (x, y, r[, z]) points"""
        pts = [p if len(p) == 4 else (p[0], p[1], p[2], z) for p in pts]
        segs = []
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            k = max(2, int(L * 1.5))
            for j in range(k):
                t = j / k
                segs.append(tuple(a[q] + (b[q] - a[q]) * t for q in range(4)))
        segs.append(pts[-1])
        mask = np.zeros((self.n, self.n), bool)
        zb = np.full((self.n, self.n), -1e9)
        nb = np.zeros((self.n, self.n, 3))
        for (x, y, r, zz) in segs:
            dx = self.X - x; dy = self.Y - y
            d2 = (dx * dx + dy * dy) / (r * r)
            m = d2 <= 1
            h = np.sqrt(np.clip(1 - d2, 0, 1))
            zc = zz + r * h
            w = m & (zc > zb)
            zb[w] = zc[w]
            n3 = np.stack([dx / r, dy / r, h + 1e-3], -1)
            nb[w] = n3[w]
            mask |= m
        nb /= np.linalg.norm(nb, axis=-1, keepdims=True) + 1e-9
        return self._write(mask, zb, nb, mat)

    def plate(self, pts, mat, z=0.0, tilt=(0, 0), bevel=2.0, dome=0.0, top=False):
        """a flat polygon with a rounded edge: wings, ears, blades, horns.
           tilt leans the whole plate's normal; bevel rounds its border."""
        mask = poly_mask(self.n, pts)
        dist = dist_in(mask)
        e = np.clip(dist / max(bevel, 0.5), 0, 1)
        # gradient of the distance field gives the outward direction
        gy, gx = np.gradient(dist)
        nx = -gx * (1 - e) * 1.6 + tilt[0]
        ny = -gy * (1 - e) * 1.6 + tilt[1]
        nz = np.ones_like(dist) * (0.6 + 0.4 * e)
        nrm = np.stack([nx, ny, nz], -1)
        nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True) + 1e-9
        zz = z + np.minimum(dist, bevel) * 0.5 + dome * np.sqrt(np.clip(dist, 0, None))
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        u = (self.X - min(xs)) / max(1, max(xs) - min(xs))
        v = (self.Y - min(ys)) / max(1, max(ys) - min(ys))
        return self._write(mask, zz, nrm, mat, u, v, top)

    def tufts(self, pts, mat, z=0.0, n=6, length=5.0, width=3.0, out=(0, -1), jitter=0.5, seed=0):
        """a row of pointed fur tufts along a path, pointing `out`:
           what breaks a furred silhouette into a pixel artist's edge"""
        L = len(pts)
        for i in range(n):
            t = i / max(1, n - 1)
            k = t * (L - 1); j = min(int(k), L - 2); u = k - j
            x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * u
            y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * u
            h = 0.7 + 0.6 * ((math.sin(i * 7.3 + seed) + 1) / 2)
            ox, oy = out
            ox += math.sin(i * 3.1 + seed) * jitter * 0.4
            tip = (x + ox * length * h, y + oy * length * h)
            px, py = -oy, ox
            self.plate([(x - px * width / 2, y - py * width / 2), tip,
                        (x + px * width / 2, y + py * width / 2)], mat, z=z, bevel=1.2,
                       tilt=(ox * 0.3, oy * 0.3))

    def dot(self, x, y, rgb):
        self.over[(int(y), int(x))] = rgb

    def shade(self, x, y, d):
        """nudge the tone at a pixel by d steps (hand placed accents)"""
        if 0 <= x < self.n and 0 <= y < self.n:
            self.bias[int(y), int(x)] += d


def poly_mask(n, pts):
    yy, xx = np.mgrid[0:n, 0:n]
    X = xx + 0.5; Y = yy + 0.5
    inside = np.zeros((n, n), bool)
    m = len(pts)
    for i in range(m):
        x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % m]
        cond = ((y0 <= Y) & (Y < y1)) | ((y1 <= Y) & (Y < y0))
        with np.errstate(divide='ignore', invalid='ignore'):
            xi = x0 + (Y - y0) * (x1 - x0) / (y1 - y0 + 1e-12)
        inside ^= cond & (X < xi)
    return inside


def dist_in(mask, cap=12):
    """distance to the edge of a mask, by repeated erosion"""
    d = np.zeros(mask.shape)
    cur = mask.copy()
    for i in range(cap):
        d[cur] += 1
        e = cur.copy()
        e[1:, :] &= cur[:-1, :]; e[:-1, :] &= cur[1:, :]
        e[:, 1:] &= cur[:, :-1]; e[:, :-1] &= cur[:, 1:]
        cur = e
        if not cur.any():
            break
    return d


# ---------------------------------------------------------------- patterns
def hsh(x, y, s=0):
    v = np.sin(x * 12.9898 + y * 78.233 + s * 37.719) * 43758.5453
    return v - np.floor(v)


def vnoise(x, y, f=0.25, s=0):
    x = x * f; y = y * f
    xi = np.floor(x); yi = np.floor(y); xf = x - xi; yf = y - yi
    u = xf * xf * (3 - 2 * xf); v = yf * yf * (3 - 2 * yf)
    a = hsh(xi, yi, s); b = hsh(xi + 1, yi, s); c = hsh(xi, yi + 1, s); d = hsh(xi + 1, yi + 1, s)
    return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v


def tex_fur(C, ang=0.4, k=1.0, s=1):
    a = math.radians(ang * 180) if abs(ang) < 3 else math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    along = C.X * ca + C.Y * sa; across = -C.X * sa + C.Y * ca
    st = vnoise(across, along * 0.22, 0.9, s) - 0.5
    clump = vnoise(C.X, C.Y, 0.18, s + 3) - 0.5
    return (st * 1.6 + clump * 0.9) * k


def tex_strands(C, ang=20, k=1.0, s=1, count=520, length=4.0):
    """drawn fur: short strokes laid along a direction, each one lit on
       its upper edge and dark under it, the way fur is clumped by hand"""
    out = np.zeros((C.n, C.n))
    rng = np.random.RandomState(s)
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    for i in range(count):
        x = rng.uniform(0, C.n); y = rng.uniform(0, C.n)
        L = length * rng.uniform(0.6, 1.3)
        for t in np.linspace(0, L, int(L * 2) + 1):
            px = int(x + dx * t); py = int(y + dy * t)
            if 0 <= px < C.n and 0 <= py < C.n:
                out[py, px] = max(out[py, px], 1.3 * (1 - t / (L + 1)))
                if py + 1 < C.n:
                    out[py + 1, px] = min(out[py + 1, px], -1.4)
    return out * k


def tex_feather(C, k=1.0, s=2, scale=4.2):
    # overlapping scallops in rows: a bright top edge and a dark lower lip
    x = C.X / scale; y = C.Y / (scale * 0.8)
    row = np.floor(y); xo = x + (row % 2) * 0.5
    fx = xo - np.floor(xo) - 0.5; fy = y - row
    d = np.sqrt(fx * fx * 1.4 + (fy - 0.15) ** 2)
    edge = (d > 0.42) & (d < 0.62)
    return (np.where(edge, -1.4, 0.0) + (0.6 - fy) * 0.9) * k


def tex_scale(C, k=1.0, s=3, scale=3.4):
    x = C.X / scale; y = C.Y / (scale * 0.75)
    row = np.floor(y); xo = x + (row % 2) * 0.5
    fx = xo - np.floor(xo) - 0.5; fy = y - row
    d = np.sqrt(fx * fx + (fy - 0.1) ** 2)
    return (np.where(d > 0.48, -1.5, 0.0) + (0.55 - fy) * 1.3) * k


def tex_stone(C, k=1.0, s=4, cell=7.0):
    # voronoi facets: each cell tilts a little, the borders crack dark
    px = C.X / cell; py = C.Y / cell
    best = np.full(px.shape, 9.0); second = np.full(px.shape, 9.0); cid = np.zeros(px.shape)
    bx = np.floor(px); by = np.floor(py)
    for oy in (-1, 0, 1):
        for ox in (-1, 0, 1):
            gx = bx + ox; gy = by + oy
            fx = gx + hsh(gx, gy, s); fy = gy + hsh(gx, gy, s + 1)
            d = np.hypot(px - fx, py - fy)
            nb = d < best
            second = np.where(nb, best, np.minimum(second, d))
            cid = np.where(nb, hsh(gx, gy, s + 2), cid)
            best = np.where(nb, d, best)
    crack = (second - best) < 0.07
    return (np.where(crack, -2.0, 0.0) + (cid - 0.5) * 1.6) * k


def tex_skin(C, k=1.0, s=5):
    sp = vnoise(C.X, C.Y, 0.55, s)
    wart = (sp > 0.78)
    return (np.where(wart, 1.2, 0.0) + (vnoise(C.X, C.Y, 0.2, s + 1) - 0.5) * 1.0) * k


def tex_bark(C, k=1.0, s=6):
    g = vnoise(C.X * 0.3, C.Y * 1.6, 0.6, s)
    return ((g - 0.5) * 2.6 + np.where(g < 0.25, -1.2, 0)) * k


def tex_metal(C, k=1.0, s=7):
    sc = vnoise(C.X * 2.2, C.Y * 0.4, 0.5, s)
    return (np.where(sc > 0.86, 1.0, 0.0) + (vnoise(C.X, C.Y, 0.12, s + 1) - 0.5) * 0.8) * k


def tex_crystal(C, k=1.0, s=8):
    f = np.floor((C.X * 0.7 + C.Y * 0.35) / 5.0) + np.floor((C.X * -0.4 + C.Y * 0.8) / 6.0)
    return ((hsh(f, f * 1.3, s) - 0.5) * 2.4) * k


# ------------------------------------------------------------------ render
def render(C, light=LIGHT, amb=0.0, rim=0.30, ao=True, clean=True, gamma=1.6):
    n = C.n
    filled = C.mat >= 0
    nd = np.clip((np.tensordot(C.nrm, light, axes=([2], [0])) + 0.45) / 1.45, 0, 1)
    shade = amb + (1 - amb) * nd ** gamma
    # occlusion: darker where something nearer stands right beside
    if ao:
        z = np.where(filled, C.z, -1e9)
        occ = np.zeros((n, n))
        for dy, dx in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1), (3, 0), (0, 3)):
            sh = np.roll(np.roll(z, dy, 0), dx, 1)
            occ += np.clip((sh - z) / 6.0, 0, 1)
        shade -= np.clip(occ / 6.0, 0, 0.35)
    # a cool back light along the right hand edge, the moody souls rim
    rn = np.clip(np.tensordot(C.nrm, RIM, axes=([2], [0])), 0, 1) ** 3
    rimt = rn * rim
    out = np.zeros((n, n, 3), dtype=np.uint8)
    idx = np.zeros((n, n), dtype=int)
    for mi, M in enumerate(C.mats):
        w = filled & (C.mat == mi)
        if not w.any():
            continue
        if M.emit:
            s = 0.55 + 0.45 * nd
        else:
            s = shade.copy()
        if M.spec:
            h = LIGHT + np.array([0, 0, 1.0]); h /= np.linalg.norm(h)
            sp = np.clip(np.tensordot(C.nrm, h, axes=([2], [0])), 0, 1) ** (12 + 30 * M.gloss)
            s = s + sp * M.spec
        s = s + rimt
        t = M.tex(C) if M.tex else 0.0
        f = s * (M.n - 1) + t * 0.42 + C.bias
        f = np.clip(np.round(f), 0, M.n - 1).astype(int)
        idx[w] = f[w]
    # glow from emissive materials onto their neighbours
    emit = np.zeros((n, n))
    for mi, M in enumerate(C.mats):
        if M.glow > 0:
            src = (filled & (C.mat == mi)).astype(float)
            g = src.copy()
            r = int(M.glow)
            acc = np.zeros((n, n))
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    d = math.hypot(dx, dy)
                    if d <= r and d > 0:
                        acc = np.maximum(acc, np.roll(np.roll(src, dy, 0), dx, 1) * (1 - d / (r + 1)))
            emit = np.maximum(emit, acc)
    for mi, M in enumerate(C.mats):
        w = filled & (C.mat == mi) & ~np.bool_(M.emit)
        idx[w] = np.clip(idx[w] + np.round(emit[w] * 2.2).astype(int), 0, M.n - 1)

    if clean:
        idx = _clean(idx, C.mat, filled)

    # seams: the far side of an overlap goes to the darkest tone
    seam = np.zeros((n, n), bool)
    for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        pz = np.roll(np.roll(C.z, dy, 0), dx, 1)
        pp = np.roll(np.roll(C.part, dy, 0), dx, 1)
        pm = np.roll(np.roll(C.mat, dy, 0), dx, 1)
        pf = np.roll(np.roll(filled, dy, 0), dx, 1)
        gap = np.where(pm == C.mat, 7.0, 2.6)
        seam |= filled & pf & (pp != C.part) & (pz - C.z > gap)
    # silhouette: inside edge pixels of the whole sprite
    edge = filled & ~(np.roll(filled, 1, 0) & np.roll(filled, -1, 0) &
                      np.roll(filled, 1, 1) & np.roll(filled, -1, 1))
    # which side does the edge face: lit edges keep a little colour
    up = filled & ~np.roll(filled, 1, 0)
    lf = filled & ~np.roll(filled, 1, 1)

    for mi, M in enumerate(C.mats):
        w = filled & (C.mat == mi)
        ramp_ = M.ramp
        for y, x in zip(*np.nonzero(w)):
            i = idx[y, x]
            col = ramp_[i]
            if edge[y, x] and not M.emit:
                if (up[y, x] or lf[y, x]):
                    col = _deep(ramp_[max(0, min(2, i - 3))], 0.55)
                else:
                    col = _deep(ramp_[0], 0.38)
            elif seam[y, x] and not M.emit:
                col = _deep(ramp_[0], 0.70)
            out[y, x] = col
    alpha = filled.astype(np.uint8) * 255
    for (y, x), c in C.over.items():
        if 0 <= y < n and 0 <= x < n:
            out[y, x] = c; alpha[y, x] = 255
    return out, alpha


def _deep(c, t):
    return tuple(int(v * t + 10 * (1 - t)) for v in c)


def _clean(idx, mat, filled):
    """a tone pixel with no neighbour of its own tone (same material)
       takes the most common neighbouring tone: no stray single pixels"""
    out = idx.copy()
    n = idx.shape[0]
    for y in range(1, n - 1):
        for x in range(1, n - 1):
            if not filled[y, x]:
                continue
            me = idx[y, x]; mm = mat[y, x]
            same = 0; votes = {}
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                yy, xx = y + dy, x + dx
                if filled[yy, xx] and mat[yy, xx] == mm:
                    v = idx[yy, xx]
                    if v == me:
                        same += 1
                    votes[v] = votes.get(v, 0) + 1
            if same == 0 and votes:
                out[y, x] = max(votes.items(), key=lambda kv: kv[1])[0]
    return out


def to_image(rgb, alpha):
    from PIL import Image
    a = np.dstack([rgb, alpha])
    return Image.fromarray(a.astype(np.uint8), 'RGBA')
