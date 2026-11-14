#!/usr/bin/env python3
"""Preview full colour gear: python3 proto/art/gearsheet.py OUT.png cat [cat ...]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from forge import render, to_image
import gear_full

out = sys.argv[1]; cats = sys.argv[2:]
items = [g for g in gear_full.GEAR if g[1] in cats]
S = 96 * 2; cols = 6
sheet = Image.new('RGBA', (S * cols, S * ((len(items) + cols - 1) // cols)), (26, 32, 48, 255))
for i, g in enumerate(items):
    C = gear_full.piece(g)
    if C is None: continue
    im = to_image(*render(C)).resize((S, S), Image.NEAREST)
    sheet.alpha_composite(im, ((i % cols) * S, (i // cols) * S))
sheet.save(out); print(out, len(items))
