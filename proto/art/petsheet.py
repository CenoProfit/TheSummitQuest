#!/usr/bin/env python3
"""Preview the full colour pets: python3 proto/art/petsheet.py OUT.png [scale]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from forge import render, to_image
import pets_full


def main():
    out = sys.argv[1]; sc = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    items = pets_full.BUILD
    S = 96 * sc
    sheet = Image.new('RGBA', (S * 4, S * ((len(items) + 1) // 2)), (26, 32, 48, 255))
    for i, (name, fn) in enumerate(items):
        for f in (0, 1):
            im = to_image(*render(fn(f))).resize((S, S), Image.NEAREST)
            sheet.alpha_composite(im, (((i % 2) * 2 + f) * S, (i // 2) * S))
    sheet.save(out); print(out)


if __name__ == '__main__':
    main()
