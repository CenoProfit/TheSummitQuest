#!/usr/bin/env python3
"""Verify a shapes module: python3 check.py shapes_sword 8"""
import sys, importlib
sys.path.insert(0, __file__.rsplit('/',1)[0])
ALLOWED=set('.odABWCcgGH')
mod=importlib.import_module(sys.argv[1]); want=int(sys.argv[2])
S=getattr(mod,'SHAPES')
assert len(S)==want, 'expected %d sprites, got %d'%(want,len(S))
for i,sp in enumerate(S):
    assert len(sp)==64, 'sprite %d has %d rows'%(i,len(sp))
    for y,r in enumerate(sp):
        assert len(r)==64, 'sprite %d row %d is %d wide'%(i,y,len(r))
        bad=set(r)-ALLOWED
        assert not bad, 'sprite %d row %d has %r'%(i,y,bad)
    fill=sum(1 for r in sp for ch in r if ch!='.')
    xs=[x for y in range(64) for x in range(64) if sp[y][x]!='.']
    ys=[y for y in range(64) for x in range(64) if sp[y][x]!='.']
    w=max(xs)-min(xs)+1; h=max(ys)-min(ys)+1
    flag=''
    if fill<420: flag+=' TOO-SPARSE(%d px)'%fill
    if max(w,h)<40: flag+=' TOO-SMALL(%dx%d)'%(w,h)
    print('sprite %d: %d px, bbox %dx%d%s'%(i,fill,w,h,flag))
print('OK', len(S), 'sprites')
