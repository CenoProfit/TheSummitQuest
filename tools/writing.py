#!/usr/bin/env python3
"""Round-trip the game's prose between index.html and plain editable files.

The game is one 811 KB file, which is a fine way to ship it and a miserable way
to write in. This pulls every piece of authored text out into writing/*.md,
where each entry is a heading with a stable id and the text beneath it, and
puts edited text back exactly where it came from.

    python3 tools/writing.py extract     # index.html  -> writing/*.md
    python3 tools/writing.py apply       # writing/*.md -> index.html
    python3 tools/writing.py check       # extract, re-apply, assert no change

Quest ids and boss keys both repeat across regions — there are eleven w1s and
several wyrms — so every entry is addressed as region.id. Replacement is a
single ordered pass over the file, which keeps offsets valid and makes it
impossible to write one region's line into another's.

Only the text inside the quotes is ever touched. Ids, coordinates, XP and every
other field are matched and left alone, and a heading that matches nothing is
reported rather than silently dropped.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "index.html")
OUT  = os.path.join(ROOT, "writing")

STR = r'(?:[^"\\]|\\.)*'                      # a JS double-quoted string body

QUEST = re.compile(r'\{id:"([a-z0-9]+)",c:"\w+",n:"(' + STR + r')"(.*?)hi:"(' + STR + r')"', re.S)
BOSS  = re.compile(r'(\w+):\{name:"(' + STR + r')",hp:(.*?)intro:"(' + STR + r')"', re.S)
# A badge description is not always one string: several are built around a live
# number, as in "Clear all "+P.length+" locations". The whole expression is
# captured and the code parts are shown as {P.length} so the prose around them
# can be rewritten without losing the value.
BADGE = re.compile(r'ach\("(\w+)","([^"]*)","(' + STR + r')",(.*?),\(\)=>', re.S)
PIECE = re.compile(r'"(' + STR + r')"|([^+]+)')

def expr_to_text(e):
    out = []
    for lit, code in PIECE.findall(e.strip()):
        out.append(unesc(lit) if lit or code == "" else "{%s}" % code.strip())
    return "".join(out)

def text_to_expr(t):
    parts, buf, i = [], "", 0
    while i < len(t):
        if t[i] == "{":
            j = t.find("}", i)
            if j < 0:
                raise SystemExit("! unclosed { in badge text: " + t[:60])
            if buf:
                parts.append('"%s"' % esc_keep(buf)); buf = ""
            parts.append(t[i + 1:j])
            i = j + 1
        else:
            buf += t[i]; i += 1
    if buf:
        parts.append('"%s"' % esc_keep(buf))
    return "+".join(parts) if parts else '""'

RANK  = re.compile(r'\{n:"(' + STR + r')",xp:(\d+)\}')


def esc(t):
    return t.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()

def esc_keep(t):
    """Like esc, but keeps leading and trailing spaces, which carry meaning
    where a literal is concatenated either side of a live value."""
    return t.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

def unesc(b):
    return b.replace('\\"', '"').replace("\\\\", "\\")

def src():
    return io.open(SRC, encoding="utf-8").read()


def regions(s):
    """[(id, name, start, end)] — each region's slice of the file."""
    hits = [(m.group(1), m.group(2), m.start())
            for m in re.finditer(r'id:"(\w+)",name:"([^"]+)",short:"', s)]
    out = []
    for i, (rid, name, start) in enumerate(hits):
        end = hits[i + 1][2] if i + 1 < len(hits) else len(s)
        out.append((rid, name, start, end))
    return out

def region_at(regs, pos):
    for rid, _, a, b in regs:
        if a <= pos < b:
            return rid
    return None


# ── extract ──────────────────────────────────────────────────────────────────
HEAD = ("<!-- Edit the text under each heading. Leave the headings alone:\n"
        "     the id in each one is how the text finds its way home.\n"
        "     Then run: python3 tools/writing.py apply -->\n")

def write_md(path, title, entries, note=""):
    b = ["# " + title, "", HEAD]
    if note:
        b += [note, ""]
    for key, label, text in entries:
        b += ["### %s · %s" % (key, label), text, ""]
    io.open(path, "w", encoding="utf-8").write("\n".join(b) + "\n")
    return len(entries)

def read_md(path):
    """-> {key: text}, preserving nothing but the prose."""
    if not os.path.exists(path):
        return {}
    out, cur, buf = {}, None, []
    for line in io.open(path, encoding="utf-8"):
        h = re.match(r'^### (\S+) · ', line)
        if h:
            if cur:
                out[cur] = " ".join(" ".join(buf).split())
            cur, buf = h.group(1), []
        elif cur is not None and not line.startswith(("<!--", "#", "     ")):
            buf.append(line.strip())
    if cur:
        out[cur] = " ".join(" ".join(buf).split())
    return {k: v for k, v in out.items() if v}


def extract():
    os.makedirs(OUT, exist_ok=True)
    s = src(); regs = regions(s); names = {r[0]: r[1] for r in regs}

    n = write_md(os.path.join(OUT, "badges.md"), "Badges",
                 [(m.group(1), unesc(m.group(3)), expr_to_text(m.group(4))) for m in BADGE.finditer(s)],
                 "The line under each badge is what the player reads when it is earned. Most of "
                 "these still describe the mechanic rather than the achievement.\n\n"
                 "A few contain a live number written as {P.length} or {cnt(\"water\")}. "
                 "Keep those tokens exactly as they are and write around them.")
    print("badges.md         %3d" % n)

    rows = []
    for m in BOSS.finditer(s):
        rid = region_at(regs, m.start())
        if rid:
            rows.append(("%s.%s" % (rid, m.group(1)), unesc(m.group(2)), unesc(m.group(4))))
    n = write_md(os.path.join(OUT, "bosses.md"), "Boss intros", rows,
                 "One line, spoken as the boss appears. The name is in the heading and "
                 "is not editable here.")
    print("bosses.md         %3d" % n)

    b = ["# Ranks", "", HEAD,
         "Each line is one rank, lowest first. Edit the names; keep the order and the "
         "count, because the XP thresholds are tied to position.", ""]
    ladders = 0
    for rid, name, a, bnd in regs:
        j = s.find("levels:[", a)
        if j < 0 or j > bnd:
            continue
        names_in = [unesc(x) for x, _ in RANK.findall(s[j:s.find("]", j)])]
        b.append("### %s · %s" % (rid, name))
        b += ["%d. %s" % (i + 1, x) for i, x in enumerate(names_in)]
        b.append("")
        ladders += 1
    io.open(os.path.join(OUT, "ranks.md"), "w", encoding="utf-8").write("\n".join(b) + "\n")
    print("ranks.md          %3d ladders" % ladders)

    total = 0
    for rid, name, a, bnd in regs:
        rows = [("%s.%s" % (rid, m.group(1)), unesc(m.group(2)), unesc(m.group(4)))
                for m in QUEST.finditer(s[a:bnd])]
        if rows:
            write_md(os.path.join(OUT, "quests-%s.md" % rid), "%s — destinations" % name, rows)
            print("quests-%-11s %3d" % (rid + ".md", len(rows)))
            total += len(rows)
    print("\n%d quests, %d bosses, %d badges" % (total, len(BOSS.findall(s)), len(BADGE.findall(s))))


# ── apply ────────────────────────────────────────────────────────────────────
def pass_over(s, rx, key_of, edits, group, used):
    """One ordered pass: rewrite capture `group` wherever an edit exists."""
    out, last, n = [], 0, 0
    regs = regions(s)
    for m in rx.finditer(s):
        key = key_of(m, regs)
        if key is None or key not in edits:
            continue
        used.add(key)
        new = esc(edits[key])
        if new == m.group(group):
            continue
        out.append(s[last:m.start(group)]); out.append(new)
        last = m.end(group); n += 1
    out.append(s[last:])
    return "".join(out), n


def apply():
    s = src()
    changed, missing = 0, []

    edits = read_md(os.path.join(OUT, "badges.md"))
    used, out, last, n = set(), [], 0, 0
    for m in BADGE.finditer(s):
        k = m.group(1)
        if k not in edits:
            continue
        used.add(k)
        new = text_to_expr(edits[k])
        if new == m.group(4).strip():
            continue
        out.append(s[last:m.start(4)]); out.append(new); last = m.end(4); n += 1
    out.append(s[last:]); s = "".join(out); changed += n
    missing += [("badges.md", k) for k in edits if k not in used]

    edits = read_md(os.path.join(OUT, "bosses.md"))
    used = set()
    s, n = pass_over(s, BOSS,
                     lambda m, r: (lambda rid: "%s.%s" % (rid, m.group(1)) if rid else None)(region_at(r, m.start())),
                     edits, 4, used); changed += n
    missing += [("bosses.md", k) for k in edits if k not in used]

    for f in sorted(os.listdir(OUT)) if os.path.isdir(OUT) else []:
        if not f.startswith("quests-"):
            continue
        edits = read_md(os.path.join(OUT, f))
        used = set()
        s, n = pass_over(s, QUEST,
                         lambda m, r: (lambda rid: "%s.%s" % (rid, m.group(1)) if rid else None)(region_at(r, m.start())),
                         edits, 4, used); changed += n
        missing += [(f, k) for k in edits if k not in used]

    # ranks are positional, so a ladder is rewritten whole or not at all
    rp = os.path.join(OUT, "ranks.md")
    if os.path.exists(rp):
        want, block = {}, None
        for line in io.open(rp, encoding="utf-8"):
            h = re.match(r'^### (\w+) · ', line)
            if h:
                block = h.group(1); want[block] = []
            elif block and re.match(r'^\d+\.\s', line):
                want[block].append(line.split(".", 1)[1].strip())
        for rid, names in want.items():
            spans = [(a, b) for i, _, a, b in regions(s) if i == rid]
            if not spans or not names:
                continue
            a, b = spans[0]
            j = s.find("levels:[", a)
            if j < 0 or j > b:
                continue
            k = s.find("]", j)
            cur = RANK.findall(s[j:k])
            if len(names) != len(cur):
                raise SystemExit("! %s has %d ranks, the game has %d — the count must match"
                                 % (rid, len(names), len(cur)))
            if [unesc(x) for x, _ in cur] == names:
                continue
            it = iter(names)
            seg = RANK.sub(lambda m: '{n:"%s",xp:%s}' % (esc(next(it)), m.group(2)), s[j:k])
            s = s[:j] + seg + s[k:]
            changed += 1

    for f, k in missing:
        print("! %s: heading '%s' matches nothing in the game — not applied" % (f, k))

    if not changed:
        print("no changes")
        return
    io.open(SRC, "w", encoding="utf-8").write(s)
    print("applied %d edit(s)" % changed)


def check():
    orig = src()
    extract()
    apply()
    if src() != orig:
        io.open(SRC, "w", encoding="utf-8").write(orig)
        raise SystemExit("\n! round trip changed the file — reverted. Do not use apply.")
    print("\nround trip clean: extract + apply left index.html byte-identical")


if __name__ == "__main__":
    {"extract": extract, "apply": apply, "check": check}[sys.argv[1] if len(sys.argv) > 1 else "extract"]()
