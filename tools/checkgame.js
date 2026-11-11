#!/usr/bin/env node
/* Refuse to ship a www/ that has the dev tool in it.
 *
 * The dev buttons reached the real web game once already. A build that
 * silently succeeds is how that happened, so this runs at the end of
 * every build and fails loudly instead.
 */
const fs = require('fs');
const path = require('path');

const F = path.join(__dirname, '..', 'www', 'trek.html');
const s = fs.readFileSync(F, 'utf8');
const bad = [];

if (!s.includes("new URLSearchParams(location.search).get('dev')==='1'"))
  bad.push('DEVMODE is not behind the ?dev=1 URL check');
if (s.includes('const DEVMODE=true'))
  bad.push('DEVMODE is hard wired on');
if (s.includes('devbadge'))
  bad.push('the DEV TOOL badge is present');
if (s.includes('sq_trek_dev4'))
  bad.push("it is using the dev tool's save key");

if (bad.length) {
  console.error('\ncheckgame: www/trek.html looks like the DEV TOOL, not the game.\n');
  for (const b of bad) console.error('  - ' + b);
  console.error('\nBuild from proto/trek.html, not proto/trek-dev.html.\n');
  process.exit(1);
}
console.log('checkgame: www/trek.html is the game build, dev controls off');
