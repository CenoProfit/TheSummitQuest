# Summit

A single-file, pixel-art RPG that turns hiking into a leveling system. Open `index.html` in any browser. No build step, no dependencies, no server.

Pick a region from the overworld map and it opens into a full game world for that region: a procedurally drawn tile map, real trailheads plotted by latitude and longitude, an XP curve, badges, and turn-based boss fights behind the multi-day treks.

## Regions

| Region | Drive times from | Locations | Bosses |
| --- | --- | --- | --- |
| Western North Carolina | Hendersonville | 60 | 7 |
| Northern Virginia | Fairfax | 57 | 7 |

**Western North Carolina** covers Pisgah and DuPont, the Great Smokies, Linville Gorge and Grandfather, Panthertown and the Jocassee Gorges, Roan Highlands, and upstate South Carolina. Mountainous edge to edge.

**Northern Virginia** covers Shenandoah National Park end to end, Massanutten and Fort Valley, Great North Mountain, the Potomac Gorge, Harpers Ferry, Sky Meadows and the Loudoun Appalachian Trail, Bull Run and Prince William Forest, and south to the Priest and Three Ridges. Fairfax was chosen as the origin because it is the population centre of the region while still holding Great Falls inside half an hour and all of Shenandoah inside two hours.

The two regions are deliberately different to generate. Western North Carolina is uniformly high ground. Northern Virginia is not: its Blue Ridge runs diagonally southwest to northeast, so elevation trends *perpendicular* to that spine, dropping through the piedmont to tidal flatland in the southeast. That is why the eastern third comes out as farmland and open valley with a dense road and city network, and the western third as ridge and hollow.

Adding a third region is a data change, not an engine change: a region supplies its own bounds, terrain features, quest list, bosses, level titles, and four landmark badges.

## Sections

**MAP** the region's world map, with the quest list on a bar beneath it. **LOGBOOK** everything cleared, newest first. **BADGES** the 20 achievements. **AVATAR** your climber: name them, pick a kit, and see your lifetime record and rope team. **REGIONS** goes back to the overworld.

The climber sprites are drawn at runtime from primitives on a 34x44 grid — a fighting-game idle in trail gear: colour-blocked shell jacket, baggy hiking pants cuffed over trail shoes, wraparound shades with a different lens colourway per kit, and a bandana on two of the four. Four tones per material with fold lines at the elbows, waist and knees. The dark keyline is derived from the silhouette rather than drawn, so it cannot fall out of step with the art, and limbs are held off the body by a column of transparency so they read as separate limbs instead of melting into the jacket.

The climber is global rather than per-region, so the same person walks every map. Skins, gear and titles are the intended next step there.

## Progression

Each region keeps its own progress, level, and badges. Level titles are flavoured to their own terrain, so Western North Carolina climbs from COUCH POTATO to MOUNTAIN LEGEND while Northern Virginia goes from BELTWAY BOUND to BLUE RIDGE LEGEND.

- Seven quest categories per region: waterfalls and swim holes, short hikes, scenic overlooks, moderate, steep and difficult, long day hikes, and multi-day boss treks
- 12 levels, with the top rank's threshold derived from the region's own quest list so it lands exactly on full completion (1,970 XP in Western North Carolina, 2,050 in Northern Virginia)
- 20 badges, sixteen shared and four specific to the region's landmarks
- Turn-based boss encounters gated behind the multi-day treks, each with its own name, palette, move set, and intro

The overworld map totals lifetime progress across every region.

Category filtering is inclusive: nothing selected shows everything, and clicking a type shows only that type. Click more to add them. The map's filter bar and the quest list's chips are two views of the same selection, so the map and the list never disagree.

The quest list opens as a full-height scrollable panel above the rest of the UI. Picking a quest keeps the list open and holds your scroll position, marking the row you chose, so you can work through several without starting over each time. On a phone the detail sheet layers over the panel; closing it drops you back where you were.

## On a phone

A region opens on FIT, so the whole map is visible before you zoom into it. The page is a flex column the height of the viewport and the map frame absorbs the slack with the canvas centred in it, so the layout reaches the bottom of the screen rather than ending in a band of empty background. The header collapses and the map sits above the fold. Choosing a destination opens it as a bottom sheet over the map rather than a panel below it, so the description and the MARK COMPLETE button are reachable without scrolling — even for a multi-day boss trek, the longest entry there is. A boss fight hides the page chrome and lays the art, party bar, log and action buttons out to fill exactly one screen.

Nothing in either layout depends on a CSS animation finishing. A throttled or backgrounded tab freezes animations mid-flight, and a sheet that animates into place would be left parked off screen with the destination unreachable.

## Saving progress

Progress saves automatically to the browser's `localStorage` on every change: completions, boss kills, badges, and the date each hike was logged. One save file holds every region.

That store is per-browser and disappears with site data, so the toolbar also has a real door out:

- **EXPORT** writes a `summit-save-YYYY-MM-DD.json` carrying every region, not just the one on screen
- **IMPORT** reads one back, on this machine or any other

Import asks for confirmation before replacing anything, and validates as it goes: unknown locations, unparseable dates, and boss kills with no matching completion are dropped rather than trusted, and it reports how many entries it skipped. A file that is not a save is refused without touching what you already have. Saves written before regions existed migrate into the Western North Carolina slot.

If the browser refuses storage entirely (private browsing, storage disabled, a full quota), the game says so up front rather than pretending to save, and EXPORT still works.

## How the maps are drawn

Terrain is generated at runtime rather than loaded as an image. A seeded PRNG feeds a stack of value-noise layers, then the region's ridges, peaks, valleys, rivers, lakes, canyons, crest road, and road network are stamped in as bumps and paths over a tile grid. Elevation bands drive the colour palette, and a BFS pass computes distance-to-water and distance-to-land for coastline and shoreline detailing. Labels use a hand-rolled bitmap font.

Each region's seed is fixed, so its map renders identically every time.

The overworld map is drawn the same way, from a coarse eastern-US coastline, the Chesapeake and Delaware bays, the Great Lakes, and three roughly parallel Appalachian belts — Blue Ridge, Valley and Ridge, Allegheny Plateau — which is what gives the range its banded grain instead of one smooth hump. A distance-from-the-sea pass creates the coastal plain.

Ground colour runs on two axes: elevation decides how grey and bright it gets, and a low-frequency band decides green forest against beige open country, so the interior breaks into patches rather than reading as one flat fill. The mix lands near 68% green, 21% beige, 5% grey ridge and 5% coastal sand. State and provincial lines are drawn over the top as hairlines; the long surveyed borders are exact and the river borders (Ohio, Potomac, Savannah, Mississippi) are traced loosely.

The continent takes about a second to generate, so it is built once into an offscreen canvas behind the loader and then blitted. Repainting for pin hover costs about a third of a millisecond instead of regenerating the whole map.

## Stack

Vanilla HTML, CSS, and JavaScript in one file. Canvas for rendering. `Press Start 2P` from Google Fonts, with a monospace fallback. No build step and no dependencies.

A region is addressed by URL hash, so `index.html#nova` links straight into Northern Virginia and switching regions is a clean reload with no chance of one world's state reaching the next.
