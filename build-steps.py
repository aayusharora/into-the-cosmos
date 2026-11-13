#!/usr/bin/env python3
"""Turn a slide you'd stand on for 90 seconds into four you move through.

    python3 build-steps.py

A slide with four rows becomes four slides. The layout never moves: the
rows that have not arrived yet are dimmed, not missing, so nothing jumps
and the audience's eye stays where you put it. The speaker notes are
dealt out across the steps in order, so each slide carries only the
sentence you say on it.

Reads project/slides/*.html and project/deck.json, writes the step files
and rewrites the order. Re-running it is safe: the original lives on as
.src.html and is the source every time.
"""
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(ROOT, "project", "slides")
DECK = os.path.join(ROOT, "project", "deck.json")

# slide -> (how many beats, a string from the container's opening tag)
SPLITS = {
    "cant-answer":      (3, "top:306px"),
    "the-loop":         (4, "left:1270px"),
    "endpoint-to-tool": (4, "top:250px"),
    "where-state-lives":(3, "top:262px"),
    "the-chain":        (4, "top:280px"),
    "mcp":              (3, "left:1076px"),
    "the-answer":       (4, "flex-direction:row"),
    "the-traps":        (3, "top:300px"),
    "tonight":          (3, "gap:30px;align-items:stretch"),
    "worlds-live":      (3, "left:1340px"),
    "earth-live":       (3, "top:300px;width:900px"),
    # architecture and the-six are not built from sibling divs: one is a
    # drawn diagram, the other a table. They keep their own pace.
}

DIM = "opacity:0.09;"


# Slides whose code block should light up the line you are on and dim the
# rest. Without this, four beats all carry the same fourteen lines of Python.
CODE = {"the-loop": ("top:296px", r'color:#FFB454;font-weight:700">([1-4])<')}

# Slides built from table rows rather than sibling divs.
TABLES = {"the-six": 2}


def children(html, after, tag="div"):
    """Spans of the direct <tag> children of a container."""
    out, depth, start, i = [], 0, None, after
    while i < len(html):
        m = re.compile(r"</?" + tag + r"\b").search(html, i)
        if not m:
            break
        if html[m.start():m.start() + 2] == "</":
            depth -= 1
            if depth == 0 and start is not None:
                out.append((start, html.index(">", m.start()) + 1))
                start = None
            if depth < 0:
                break
            i = m.end()
        else:
            if depth == 0:
                start = m.start()
            depth += 1
            i = m.end()
    return out


def dim(block):
    m = re.search(r'style="', block)
    if not m:
        return block
    return block[:m.end()] + DIM + block[m.end():]


def notes_for(aside, step, total):
    """Deal the note paragraphs out across the steps, in order.

    Never returns nothing: a beat with no note of its own is a beat the
    presenter is standing on with no idea what to say.
    """
    paras = [p.strip() for p in aside.split("\n\n") if p.strip()]
    if not paras:
        return ""
    if len(paras) >= total:
        per = len(paras) / total
        lo, hi = round(step * per), round((step + 1) * per)
        return "\n\n".join(paras[lo:hi]) or paras[min(step, len(paras) - 1)]
    # fewer paragraphs than beats: first beat opens, last beat closes,
    # the middle ones get whatever is left over in order
    if step == 0:
        return paras[0]
    if step == total - 1:
        return paras[-1]
    spare = paras[1:-1]
    return spare[(step - 1) % len(spare)] if spare else ""


def row_cue(block):
    """A one-line reminder of the row this beat reveals."""
    txt = re.sub(r"<[^>]+>", " ", block)
    txt = re.sub(r"\s+", " ", __import__("html").unescape(txt)).strip()
    return f"This beat reveals: {txt[:150]}" if txt else ""


def split_table(sid, n):
    """the-six is a table, not sibling divs. Beat 1 gets rows 1-3."""
    src = os.path.join(SLIDES, f"{sid}.src.html")
    if not os.path.exists(src):
        shutil.copy2(os.path.join(SLIDES, f"{sid}.html"), src)
    raw = open(src, encoding="utf-8").read()
    am = re.search(r"<aside>([\s\S]*?)</aside>", raw)
    aside = am.group(1).strip() if am else ""
    body = re.sub(r"<aside>[\s\S]*?</aside>\s*", "", raw)

    rows = [m.span() for m in re.finditer(r"<tr[\s\S]*?</tr>", body)][1:]   # skip header
    if len(rows) < n:
        return f"  {sid}: only {len(rows)} data rows"
    per = len(rows) / n
    tail = list(re.finditer(
        r'<p style="position:absolute;[^"]*bottom:[^"]*"[^>]*>[\s\S]*?</p>', body))
    tail = tail[-1].span() if tail else None

    made = []
    for step in range(n):
        hi = round((step + 1) * per)
        spans = rows[hi:]
        if tail and step < n - 1:
            spans = spans + [tail]
        out = body
        for a_, b_ in sorted(spans, key=lambda s: -s[0]):
            out = out[:a_] + dim(out[a_:b_]) + out[b_:]
        nid = f"{sid}-{step + 1}"
        out = out.replace(f'<section id="{sid}"', f'<section id="{nid}"', 1)
        note = notes_for(aside, step, n)
        out = out.rstrip()
        if out.endswith("</section>"):
            out = out[:-len("</section>")] + (f"<aside>{note}</aside>\n" if note else "") + "</section>\n"
        open(os.path.join(SLIDES, f"{nid}.html"), "w", encoding="utf-8").write(out)
        made.append(nid)
    return made


def split(sid, n, anchor):
    src = os.path.join(SLIDES, f"{sid}.src.html")
    if not os.path.exists(src):
        shutil.copy2(os.path.join(SLIDES, f"{sid}.html"), src)
    raw = open(src, encoding="utf-8").read()

    am = re.search(r"<aside>([\s\S]*?)</aside>", raw)
    aside = am.group(1).strip() if am else ""
    body = re.sub(r"<aside>[\s\S]*?</aside>\s*", "", raw)

    cm = re.search(r"<div[^>]*" + re.escape(anchor) + r"[^>]*>", body)
    if not cm:
        return f"  {sid}: anchor {anchor!r} not found"
    kids = children(body, cm.end())
    if len(kids) < n:
        return f"  {sid}: wanted {n} rows, found {len(kids)}"
    kids = kids[:n]

    # the closing line only belongs on the last step
    tail = list(re.finditer(
        r'<p style="position:absolute;[^"]*bottom:[^"]*"[^>]*>[\s\S]*?</p>', body))
    tail = tail[-1].span() if tail else None

    # code lines, grouped by the step marker that most recently appeared
    groups = []
    if sid in CODE:
        canchor, marker = CODE[sid]
        km = re.search(r"<div[^>]*" + re.escape(canchor) + r"[^>]*>", body)
        if km:
            g = -1
            for a, b in children(body, km.end(), "p"):
                mk = re.search(marker, body[a:b])
                if mk:
                    g = int(mk.group(1)) - 1
                groups.append((g, a, b))

    made = []
    for step in range(n):
        # Collect every span to dim, then apply them back to front in one
        # pass. Dimming front to back would shift the offsets of everything
        # after it, because dim() inserts characters.
        spans = [(a, b) for g, a, b in groups if g > step]
        spans += [kids[j] for j in range(n) if j > step]
        if tail and step < n - 1:
            spans.append(tail)

        out = body
        for a, b in sorted(spans, key=lambda s: -s[0]):
            out = out[:a] + dim(out[a:b]) + out[b:]
        nid = f"{sid}-{step + 1}"
        out = out.replace(f'<section id="{sid}"', f'<section id="{nid}"', 1)
        note = notes_for(aside, step, n)
        if not note:
            a, b = kids[step]
            note = row_cue(body[a:b])
        out = out.rstrip()
        if out.endswith("</section>"):
            out = out[:-len("</section>")] + (f"<aside>{note}</aside>\n" if note else "") + "</section>\n"
        open(os.path.join(SLIDES, f"{nid}.html"), "w", encoding="utf-8").write(out)
        made.append(nid)
    return made


def main():
    deck = json.load(open(DECK))
    order, report = [], []
    for sid in deck["order"]:
        if sid in TABLES or sid in SPLITS:
            if sid in TABLES:
                n = TABLES[sid]
                res = split_table(sid, n)
            else:
                n, anchor = SPLITS[sid]
                res = split(sid, n, anchor)
            if isinstance(res, str):
                report.append(res)
                order.append(sid)
            else:
                order.extend(res)
                report.append(f"  {sid}  ->  {n} beats")
        else:
            order.append(sid)
    deck["order"] = order
    json.dump(deck, open(DECK, "w"), indent=2, ensure_ascii=False)
    print("\n".join(report))
    print(f"\n{len(deck['order'])} slides in the order now.")


if __name__ == "__main__":
    main()
