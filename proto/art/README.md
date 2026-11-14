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

## Full colour gear (Nov 2026)

Every piece and pet is now drawn in full colour and stored in the
`FULLRGB` table in `trek.html`, which the page prefers over the letter
sprites above (those stay as the fallback and for the worn hero layers).

    forge.py       the 2.5D renderer: modelled forms, hue shifted ramps,
                   surface patterns, selective outline, glow
    pets_full.py   the fifteen companions, two frames each
    gear_full.py   one design per gear shape, coloured from PAL per piece
    items_full.py  one-off pieces (the legendary staff)
    fullpack.py    render all of it and splice FULLRGB into trek.html
    petsheet.py, gearsheet.py, sheet.py   PNG contact sheets for review

After changing any of them: `python3 proto/art/fullpack.py`, then
`node tools/mkdev.js` and check the dev tool.
