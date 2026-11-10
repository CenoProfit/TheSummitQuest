# -*- coding: utf-8 -*-
"""Turn the hand drawn .ase bosses into something trek.html can draw.

   The procedural sprites are a tone ramp tinted per item at runtime.
   These are not: they are finished full colour art and the point is to
   keep the colours the artist chose. So each one becomes a palette plus
   a run length encoded index stream, base64'd, which decodes
   synchronously at first use the same way the letter sprites do.

   Run pack.py FIRST and this second: pack.py owns the block of the
   file this used to be spliced into.
"""
import base64, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aseload

HERE = os.path.dirname(os.path.abspath(__file__))

# the file each boss wants, by the name in the BOSS table
WANT = [
    ('THE BLOOD MOUNTAIN WARDEN', 'trekwarden'),
    ('THE LAUREL HELL',           'treklaurel'),
    ('THE BLY GAP OAK',           'trekoakmonster'),
    ('THE NANTAHALA HOARFROST',   'trekhoarfrost'),
    ('THE GORGE LEVIATHAN',       'trekleviathon'),
    ('THE STORM OVER TRAY',       'trekstorm'),
    ('THE RIDGE WYRM',            'trekworm'),
    ('THE CARRION CROWN',         'trekvulture'),
]


def encode(path):
    w, h, px = aseload.load(path)
    assert w == h, '%s is %dx%d, not square' % (path, w, h)
    pal, idx = {(0, 0, 0, 0): 0}, []
    order = [(0, 0, 0, 0)]
    for i in range(0, len(px), 4):
        a = px[i + 3]
        key = (0, 0, 0, 0) if a < 8 else (px[i], px[i + 1], px[i + 2], 255)
        if key not in pal:
            pal[key] = len(order)
            order.append(key)
        idx.append(pal[key])
    assert len(order) <= 256, '%s has %d colours' % (path, len(order))
    out = bytearray()
    i = 0
    while i < len(idx):
        v = idx[i]
        n = 1
        while i + n < len(idx) and idx[i + n] == v and n < 255:
            n += 1
        out.append(n)
        out.append(v)
        i += n
    cols = ','.join('0' if c[3] == 0 else '0x%02x%02x%02x' % (c[0], c[1], c[2])
                    for c in order)
    return w, cols, base64.b64encode(bytes(out)).decode('ascii')


def main():
    rows = []
    for name, stem in WANT:
        p = os.path.join(HERE, 'ase', stem + '.ase')
        n, cols, data = encode(p)
        rows.append('{n:%d,p:[%s],\n  d:"%s"}' % (n, cols, data))
        print('%-26s %s  %d chars' % (name, stem, len(data)))
    js = 'const BOSSRGB=[\n ' + ',\n '.join(rows) + '];\n'
    html = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                        'proto', 'trek.html')
    s = open(html).read()
    # pack.py rewrites everything between `const SHAPE={` and the gear
    # table, so this block cannot live in there or the next pack run
    # silently deletes it. It goes immediately before ENCPIX, which is
    # the first thing after that region.
    if 'const BOSSRGB=[' in s:
        a = s.index('const BOSSRGB=[')
        b = s.index('];', a) + 3
        s = s[:a] + js + s[b:]
    else:
        a = s.index('const ENCPIX=[')
        s = s[:a] + js + s[a:]
    open(html, 'w').write(s)
    print('spliced into trek.html, now %d bytes' % len(s))


if __name__ == '__main__':
    main()
