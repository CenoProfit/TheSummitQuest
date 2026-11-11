#!/usr/bin/env node
/* Build proto/trek-dev.html from proto/trek.html.
 *
 * The dev tool is a SEPARATE FILE so that nothing about it can reach
 * the game, but it is GENERATED rather than hand kept, because two
 * hand edited copies of a 560KB file drift. They drifted twice before:
 * once the boss art was fixed in dev and not in the game, once the dev
 * buttons shipped in the game.
 *
 * So: edit proto/trek.html, run this, test the dev tool. The game only
 * changes when `npm run sync` is run, which is the approval gate.
 *
 * Every substitution below is checked. If a rename upstream makes one
 * of them miss, this exits non-zero and says which, rather than
 * quietly handing back a dev tool that shares the game's save file or
 * has its buttons switched off.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SRC = path.join(ROOT, 'proto', 'trek.html');
const OUT = path.join(ROOT, 'proto', 'trek-dev.html');

let s = fs.readFileSync(SRC, 'utf8');
const fails = [];

function sub(what, find, replace, count) {
  const hits = s.split(find).length - 1;
  if (hits !== count) {
    fails.push(`${what}: expected ${count} match(es) of ${JSON.stringify(find)}, found ${hits}`);
    return;
  }
  s = s.split(find).join(replace);
}

/* 1. dev mode on, unconditionally. No ?dev=1 to remember, and no way
      for the game's copy to be switched into it by a URL. */
sub('DEVMODE flag',
    "const DEVMODE=new URLSearchParams(location.search).get('dev')==='1';",
    "const DEVMODE=true; /* generated dev tool: see tools/mkdev.js */",
    1);

/* 2. its own save. Walking 5,000 steps a click through a test must not
      land in the real progress; same origin when both are served from
      http-server, so the key is the only thing keeping them apart. */
sub('save key', "'sq_trek_proto4'", "'sq_trek_dev4'", 2);
sub('music key', "const MKEY='sq_trek_music';", "const MKEY='sq_trek_music_dev';", 1);

/* 3. say so on screen and in the tab, so a screenshot of the dev tool
      is never mistaken for the game. */
sub('title', '<title>Summit Quest', '<title>DEV: Summit Quest', 1);
sub('badge', '</body>',
    '<div id="devbadge">DEV TOOL</div>\n' +
    '<style>#devbadge{position:fixed;left:6px;top:6px;z-index:9999;' +
    'font:700 10px/1 ui-monospace,monospace;letter-spacing:.14em;' +
    'color:#ffd98a;background:rgba(0,0,0,.62);border:1px solid #ffd98a;' +
    'border-radius:3px;padding:4px 6px;pointer-events:none}</style>\n</body>',
    1);

if (fails.length) {
  console.error('mkdev: proto/trek.html no longer matches what this script edits.\n');
  for (const f of fails) console.error('  - ' + f);
  console.error('\nFix tools/mkdev.js to match, then rerun. Not writing ' +
                path.relative(ROOT, OUT) + '.');
  process.exit(1);
}

fs.writeFileSync(OUT, s);
console.log('mkdev: wrote proto/trek-dev.html (' +
            (Buffer.byteLength(s) / 1024).toFixed(0) + 'KB) from proto/trek.html');
