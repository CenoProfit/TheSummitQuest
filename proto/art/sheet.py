#!/usr/bin/env python3
"""Contact sheet of the gear as trek.html draws it, for looking at art.

    python3 proto/art/sheet.py OUT.png [category ...]

Reads GEAR and PAL out of trek.html and the sprite tables it holds, maps
each letter to a colour the same way tones() does in the page, and lays
the pieces out on a grid with the eight bosses underneath for scale.
Nothing here is shipped; it only writes a PNG.
"""
import os, re, sys, json, base64
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HTML = open(os.path.join(ROOT, 'proto', 'trek.html')).read()


def js_block(start, end):
    a = HTML.index(start); b = HTML.index(end, a)
    return HTML[a:b + len(end)]


def rgb(h):
    h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


PAL = {}
for m in re.finditer(r"(\w+):\['(#\w+)','(#\w+)','(#\w+)'\]", js_block('const PAL={', '};')):
    PAL[m.group(1)] = [rgb(m.group(i)) for i in (2, 3, 4)]

GEAR = []
for m in re.finditer(r"\[(['\"])(.*?)\1,'(\w+)',(\d),(\d+),'(\w+)','(\w+)','(\w+)','(\w+)'\]",
                     js_block('const GEAR=[', "leather']];")):
    GEAR.append([m.group(2), m.group(3), int(m.group(4)), int(m.group(5))] + [m.group(i) for i in range(6, 10)])


def unrle(s):
    out = []; i = 0
    while i < len(s):
        c = s[i]; i += 1; n = ''
        while i < len(s) and s[i].isdigit(): n += s[i]; i += 1
        out.append(c * (int(n) if n else 1))
    return ''.join(out)


def strings(block):
    return re.findall(r'"([^"]*)"', block)


shape_blk = js_block('const SHAPE={', '};')
SHAPE = {}
for cat in ('sword', 'staff', 'shield', 'helm', 'chest', 'shoes', 'pet'):
    m = re.search(r'\b%s:\[(.*?)\](,|\})' % cat, shape_blk, re.S)
    SHAPE[cat] = strings(m.group(1)) if m else []

DARK = [12, 11, 18]
mix = lambda a, b, t: [a[i] + (b[i] - a[i]) * t for i in range(3)]
lite = lambda a, t: mix(a, [255, 255, 255], t)


def tones(g):
    P = PAL[g[4]]; Q = PAL.get(g[5], PAL['leather'])
    A, B, C = P
    return dict(o=mix(A, DARK, .88), n=mix(A, DARK, .66), q=mix(A, DARK, .54), d=mix(A, DARK, .34),
                e=mix(A, DARK, .15), A=A, B=B, W=lite(B, .42), V=lite(B, .76),
                x=mix(C, DARK, .56), c=mix(C, DARK, .27), C=C, Y=lite(C, .32), Z=lite(C, .66),
                j=mix(Q[0], DARK, .56), g=mix(Q[0], DARK, .30), G=Q[0], H=Q[1], K=lite(Q[1], .42),
                u=[132, 94, 70], m=[196, 148, 114], M=[228, 190, 158])


def letter_img(rows, T):
    n = len(rows); im = Image.new('RGBA', (n, n), (0, 0, 0, 0)); px = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.':
                c = T.get(ch, T['A']); px[x, y] = (int(c[0]), int(c[1]), int(c[2]), 255)
    return im


def gear_img(g):
    """the piece as the page draws it; a full colour entry wins if there is one"""
    full = FULL.get(g[1])
    if full and g[3] < len(full) and full[g[3]]:
        return full[g[3]]
    s = unrle(SHAPE[g[1]][g[3]]); n = int(len(s) ** .5)
    return letter_img([s[i * n:(i + 1) * n] for i in range(n)], tones(g))


FULL = {}


def boss_imgs():
    blk = js_block('const BOSSRGB=[', '];')
    out = []
    for m in re.finditer(r'\{n:(\d+),p:\[([^\]]*)\],\s*d:"([^"]*)"', blk):
        n = int(m.group(1)); pal = [int(v, 16) if v.startswith('0x') else 0 for v in m.group(2).split(',')]
        d = base64.b64decode(m.group(3)); im = Image.new('RGBA', (n, n)); px = im.load(); o = 0
        for k in range(0, len(d), 2):
            run, col = d[k], pal[d[k + 1]]
            for _ in range(run):
                if col: px[o % n, o // n] = ((col >> 16) & 255, (col >> 8) & 255, col & 255, 255)
                o += 1
        out.append(im)
    return out


def main():
    out = sys.argv[1]; cats = sys.argv[2:] or None
    items = [g for g in GEAR if not cats or g[1] in cats]
    S, cols = 96, 10
    rows = (len(items) + cols - 1) // cols
    bosses = boss_imgs()
    W = cols * S; H = rows * S + (S * 2 if bosses else 0)
    sheet = Image.new('RGBA', (W, H), (26, 32, 48, 255))
    for i, g in enumerate(items):
        im = gear_img(g).resize((S, S), Image.NEAREST)
        sheet.alpha_composite(im, ((i % cols) * S, (i // cols) * S))
    for i, b in enumerate(bosses[:5]):
        sheet.alpha_composite(b.resize((S * 2, S * 2), Image.NEAREST), (i * S * 2, rows * S))
    sheet.save(out)
    print('%d pieces -> %s' % (len(items), out))


if __name__ == '__main__':
    main()
