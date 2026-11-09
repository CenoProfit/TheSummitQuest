#!/usr/bin/env python3
"""Print one sprite as ASCII: python3 render.py shapes_pets_a 3"""
import sys, importlib
sys.path.insert(0, __file__.rsplit('/',1)[0])
mod=importlib.import_module(sys.argv[1])
print('\n'.join(mod.SHAPES[int(sys.argv[2])]))
