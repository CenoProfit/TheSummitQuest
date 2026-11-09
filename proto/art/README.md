# Sprite source

`proto/trek.html` holds the sprites as run-length-encoded strings, which
are not editable by hand. This directory is where they come from.

    pixlib.py          the 64x64 composition library and the house style
    example_sword.py   one worked sprite, read it first
    shapes_*.py        one module per gear category, each exporting SHAPES
    check.py           verify a module:  python3 check.py shapes_sword 8
    render.py          print one sprite:  python3 render.py shapes_sword 0
    pack.py            encode every module and splice it into trek.html

To change a piece of gear: edit its builder, run `check.py` on the module,
then run `pack.py` from the repo root and reload the page.

The sprites are authored at 64x64 and drawn with nearest-neighbour
scaling, so everything you want to see has to be a pixel someone placed.
There is no bevel, no lighting pass and no texture at runtime; the
renderer maps a character to a colour and stops. The palette behind each
character is chosen per item, which is how forty-six shapes become a
hundred and fifteen pieces.
