#!/usr/bin/env python3
"""Collect every shapes_*.py module (NOT shapes_boss: the bosses are
   hand drawn .ase files now and asepack.py handles those), run-length encode the sprites and
   splice them into proto/trek.html.

   A 64x64 sprite is 4096 characters and most of them are '.', so the
   raw table would be a quarter of a megabyte. Encoding runs as
   <char><count> takes it to a fraction of that and costs one tiny
   decoder at the far end."""
import sys, os, importlib, re
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
ROOT=os.path.dirname(os.path.dirname(HERE))
HTML=os.path.join(ROOT,'proto','trek.html')
ALLOWED=set(".on"+"qdeABWV"+"xcCYZ"+"jgGHK"+"umM")

CATS=[('sword','shapes_sword',8),('staff','shapes_staff',6),
      ('shield','shapes_shield',6),('helm','shapes_helm',9),
      ('chest','shapes_chest',5),('shoes','shapes_shoes',4)]
PETS=[('shapes_pets_a',5),('shapes_pets_b',5)]

def rle(sp):
    flat=''.join(sp)
    assert len(flat)==96*96, len(flat)
    out=[]; i=0
    while i<len(flat):
        c=flat[i]; j=i
        while j<len(flat) and flat[j]==c: j+=1
        n=j-i
        out.append(c if n==1 else c+str(n))
        i=j
    return ''.join(out)

def unrle(s):
    out=[];i=0
    while i<len(s):
        c=s[i];i+=1;n=''
        while i<len(s) and s[i].isdigit(): n+=s[i];i+=1
        out.append(c*(int(n) if n else 1))
    return ''.join(out)

def load(mod,want):
    m=importlib.import_module(mod)
    S=m.SHAPES
    assert len(S)==want,'%s: expected %d sprites, got %d'%(mod,want,len(S))
    for i,sp in enumerate(S):
        assert len(sp)==96,'%s[%d] has %d rows'%(mod,i,len(sp))
        for y,r in enumerate(sp):
            assert len(r)==96,'%s[%d] row %d is %d wide'%(mod,i,y,len(r))
            assert not (set(r)-ALLOWED),'%s[%d] row %d: %r'%(mod,i,y,set(r)-ALLOWED)
    return S

def main():
    raw=0; enc=0
    shape_js=["const SHAPE={"]
    for cat,mod,n in CATS:
        S=load(mod,n)
        rows=[]
        for sp in S:
            e=rle(sp); assert unrle(e)==''.join(sp)
            raw+=9216; enc+=len(e); rows.append('"%s"'%e)
        shape_js.append(" %s:[%s],"%(cat,",\n  ".join(rows)))
    petA=[]; petB=[]
    for mod,n in PETS:
        S=load(mod,n*2)
        for i in range(n):
            for src,dst in ((S[i*2],petA),(S[i*2+1],petB)):
                e=rle(src); assert unrle(e)==''.join(src)
                raw+=9216; enc+=len(e); dst.append('"%s"'%e)
    shape_js.append(" pet:[%s]};"%",\n  ".join(petA))
    import importlib
    H=importlib.import_module('shapes_hero').SHAPES
    assert len(H)==32, len(H)
    hero=[]
    for sp in H:
        assert len(sp)==64 and all(len(r)==64 for r in sp), 'hero layer is not 64x64'
        flat=''.join(sp); o=[]; i=0
        while i<len(flat):
            c=flat[i]; j=i
            while j<len(flat) and flat[j]==c: j+=1
            o.append(c if j-i==1 else c+str(j-i)); i=j
        e=''.join(o); assert unrle(e)==flat
        raw+=4096; enc+=len(e); hero.append('"%s"'%e)
    SC=load('shapes_scen',4)
    scen=[]
    for sp in SC:
        e=rle(sp); assert unrle(e)==''.join(sp)
        raw+=9216; enc+=len(e); scen.append('"%s"'%e)
    E=load('shapes_enc',5)
    encs=[]
    for sp in E:
        e=rle(sp); assert unrle(e)==''.join(sp)
        raw+=9216; enc+=len(e); encs.append('"%s"'%e)
    out=("\n".join(shape_js)+"\nconst PETALT=[%s];\nconst HERO=[%s];\n"
         "const ENCPIX=[%s];\nconst SCENPIX=[%s];\n")%(
        ",\n  ".join(petB), ",\n  ".join(hero),
        ",\n  ".join(encs), ",\n  ".join(scen))
    s=open(HTML).read()
    a=s.index("const SHAPE={"); b=s.index("/* [name, category",a)
    s=s[:a]+out+"\n"+s[b:]
    open(HTML,'w').write(s)
    print("packed %d sprites: %d raw chars -> %d encoded (%.1f%%)"%(
        len(petA)*2+sum(n for _,_,n in CATS), raw, enc, 100.0*enc/raw))
    print("trek.html is now %d bytes"%len(s))

if __name__=='__main__': main()
