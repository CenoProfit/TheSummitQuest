# -*- coding: utf-8 -*-
"""Read an Aseprite .ase/.aseprite file into flat RGBA pixels.

   There is no Aseprite CLI on this machine, so this reads the format
   directly. It covers what the Summit Quest files actually use: one
   frame, RGBA or indexed colour, normal blending, raw or zlib cels.
   It is not a general importer and will say so rather than guess if it
   meets something it does not handle.

   Format reference: Aseprite's own ase-file-specs.md.
"""
import struct, zlib


def _u16(b, o): return struct.unpack_from('<H', b, o)[0]
def _i16(b, o): return struct.unpack_from('<h', b, o)[0]
def _u32(b, o): return struct.unpack_from('<I', b, o)[0]


def load(path):
    """-> (w, h, bytearray of w*h*4 RGBA), frame 0, layers composited."""
    with open(path, 'rb') as f:
        raw = f.read()

    if _u16(raw, 4) != 0xA5E0:
        raise ValueError('%s: not an Aseprite file' % path)
    frames = _u16(raw, 6)
    W, H = _u16(raw, 8), _u16(raw, 10)
    depth = _u16(raw, 12)
    trans = raw[28]
    if depth not in (32, 8, 16):
        raise ValueError('%s: colour depth %d not handled' % (path, depth))

    out = bytearray(W * H * 4)
    pal = {}
    layers = []          # (visible, opacity) in index order
    o = 128

    for _ in range(frames):
        fsize = _u32(raw, o)
        if _u16(raw, o + 4) != 0xF1FA:
            raise ValueError('%s: bad frame magic' % path)
        nchunks = _u32(raw, o + 12) or _u16(raw, o + 6)
        p = o + 16
        for _ in range(nchunks):
            csize = _u32(raw, p)
            ctype = _u16(raw, p + 4)
            d = raw[p + 6: p + csize]

            if ctype == 0x2004:                       # layer
                flags = _u16(d, 0)
                ltype = _u16(d, 2)
                # opacity is at 12: flags, type, child level, default w,
                # default h, blend mode, THEN opacity. Reading it at 10
                # picks up the blend mode, which is 0 for normal, so
                # every layer came through completely transparent.
                opac = d[12]
                layers.append((bool(flags & 1) and ltype == 0, opac))

            elif ctype == 0x2019:                     # palette
                n = _u32(d, 0)
                first, last = _u32(d, 4), _u32(d, 8)
                q = 20
                for i in range(first, last + 1):
                    fl = _u16(d, q); q += 2
                    r, g, b, a = d[q], d[q+1], d[q+2], d[q+3]; q += 4
                    if fl & 1:                        # has a name
                        q += 2 + _u16(d, q)
                    pal[i] = (r, g, b, a)

            elif ctype in (0x0004, 0x0011):           # old palette
                npk = _u16(d, 0); q = 2; idx = 0
                for _ in range(npk):
                    idx += d[q]; cnt = d[q+1] or 256; q += 2
                    for k in range(cnt):
                        r, g, b = d[q], d[q+1], d[q+2]; q += 3
                        pal[idx + k] = (r, g, b, 255)
                    idx += cnt

            elif ctype == 0x2005:                     # cel
                li = _u16(d, 0)
                cx, cy = _i16(d, 2), _i16(d, 4)
                copac = d[6]
                ctyp = _u16(d, 7)
                if ctyp == 1:
                    raise ValueError('%s: linked cels not handled' % path)
                cw, ch = _u16(d, 16), _u16(d, 18)
                body = d[20:]
                if ctyp == 2:
                    body = zlib.decompress(bytes(body))
                vis, lopac = layers[li] if li < len(layers) else (True, 255)
                if not vis:
                    p += csize
                    continue
                a_mul = (copac / 255.0) * (lopac / 255.0)
                _blit(out, W, H, body, cw, ch, cx, cy, depth, pal, trans, a_mul)

            p += csize
        o += fsize
        break                                          # frame 0 only

    return W, H, out


def _blit(out, W, H, src, cw, ch, cx, cy, depth, pal, trans, a_mul):
    bpp = {32: 4, 16: 2, 8: 1}[depth]
    for y in range(ch):
        oy = cy + y
        if oy < 0 or oy >= H:
            continue
        for x in range(cw):
            ox = cx + x
            if ox < 0 or ox >= W:
                continue
            s = (y * cw + x) * bpp
            if depth == 32:
                r, g, b, a = src[s], src[s+1], src[s+2], src[s+3]
            elif depth == 16:                          # grayscale + alpha
                r = g = b = src[s]; a = src[s+1]
            else:
                i = src[s]
                if i == trans:
                    continue
                r, g, b, a = pal.get(i, (0, 0, 0, 0))
            a = int(a * a_mul)
            if a <= 0:
                continue
            k = (oy * W + ox) * 4
            if a >= 255:
                out[k], out[k+1], out[k+2], out[k+3] = r, g, b, 255
            else:                                      # normal blend
                sa = a / 255.0
                da = out[k+3] / 255.0
                na = sa + da * (1 - sa)
                if na <= 0:
                    continue
                for c in range(3):
                    out[k+c] = int((src_c(r, g, b, c) * sa +
                                    out[k+c] * da * (1 - sa)) / na)
                out[k+3] = int(na * 255)


def src_c(r, g, b, c): return (r, g, b)[c]
