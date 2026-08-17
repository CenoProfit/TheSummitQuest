# Blue Ridge Quest III

A single-file, pixel-art RPG that turns Western North Carolina hiking into a leveling system. Open `index.html` in any browser. No build step, no dependencies, no server.

## What it is

An interactive tile map of the Blue Ridge region with 57 real destinations plotted by latitude and longitude. Check off a hike, earn XP, climb from COUCH POTATO to MOUNTAIN LEGEND.

**Seven quest categories**

| Category | Count |
| --- | --- |
| Waterfalls and swim holes | 14 |
| Short hikes | 8 |
| Scenic overlooks | 6 |
| Moderate hikes | 8 |
| Steep and difficult | 7 |
| Long day hikes | 7 |
| Multi-day boss treks | 7 |

Each entry carries drive time, difficulty, mileage, time estimate, a highlight note, and a nearby food stop. XP scales with difficulty (Easy 10 to Extreme 65) plus a category bonus for long and multi-day routes.

**Progression**

- 12 levels across a 1,910 XP curve
- 20 achievement badges for category sweeps and specific combinations
- Turn-based boss encounters gated behind the seven multi-day treks, each with its own sprite, palette, and move set

## How the map is drawn

The terrain is generated at runtime rather than loaded as an image. A seeded PRNG feeds a stack of value-noise layers, then ridges, peaks, valleys, rivers, lakes, canyons, the Blue Ridge Parkway, and road networks are stamped in as bumps and paths over a 104 x 78 tile grid. Elevation bands drive the color palette, and a BFS pass computes distance-to-water and distance-to-land for coastline and shoreline detailing. Text labels use a hand-rolled bitmap font.

The seed is fixed, so the map renders identically every time.

## Coverage

Roughly bounded by 83.76 W to 81.58 W and 36.38 N to 34.52 N: Pisgah and DuPont, the Great Smokies, Linville Gorge and Grandfather, Panthertown and the Jocassee Gorges, Roan Highlands, and upstate South Carolina.

## Saving progress

Progress saves automatically to the browser's `localStorage` on every change: completions, boss kills, badges, and the date each hike was logged. Close the tab and come back and it is all still there.

That store is per-browser and disappears with site data, so the toolbar also has a real door out:

- **EXPORT** writes a small `blue-ridge-quest-YYYY-MM-DD.json` file
- **IMPORT** reads one back, on this machine or any other

Import asks for confirmation before replacing anything, and validates as it goes: unknown locations, unparseable dates, and boss kills with no matching completion are dropped rather than trusted, and it tells you how many entries it skipped. A file that is not a save is refused without touching what you already have.

If the browser refuses storage entirely (private browsing, storage disabled, a full quota), the game says so up front rather than pretending to save, and EXPORT still works.

## Stack

Vanilla HTML, CSS, and JavaScript in one file. Canvas for rendering. `Press Start 2P` from Google Fonts, with a monospace fallback. No build step and no dependencies.
