#!/usr/bin/env python3
"""Build PRESENTATION-GUIDE.md from the slides themselves.

    python3 build-guide.py

The per-slide notes are the <aside> in each slide file, so the guide cannot
drift from the deck. Only the timings and the front matter live here.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(ROOT, "project", "slides")

# minutes per slide — the only numbers in this file that are a judgement call
TIME = {
    "cover": 0.5, "the-question": 1.5, "cant-answer": 1.0, "ten-things": 1.0,
    "what-were-building": 1.25, "fifteen-lines": 1.0, "the-declaration": 1.0,
    "the-loop": 1.25,
    "cloud-code": 0.5, "endpoint-to-tool": 1.25, "cloud-tonight": 1.0,
    "gap-eyes": 0.25, "sky-code": 0.5, "sky-tonight": 1.25,
    "gap-moon": 0.25, "moon-code": 0.5, "moon-tonight": 1.0,
    "gap-memory": 0.25, "memory-code": 0.5, "where-state-lives": 1.25,
    "memory-night-one": 0.75, "memory-night-two": 0.75,
    "gap-chain": 0.25, "the-chain": 1.5,
    "gap-silence": 0.25, "the-silence": 1.0,
    "gap-mcp": 0.25, "mcp": 1.5,
    "gap-right": 0.25, "real-transcript": 1.0,
    "the-answer": 1.5,
    "what-it-cost": 0.5, "the-six": 1.0, "l1-docstring": 2.0,
    "l2-returns": 0.75, "l3-errors": 1.25, "the-traps": 0.75,
    "l4-latency": 1.25, "l5-retries": 0.75, "l6-scoring": 1.25,
    "architecture": 1.75, "scoreboard-sql": 1.25,
    "worlds-live": 1.0, "earth-live": 1.0, "worlds-found": 1.25,
    "recap-six": 1.0, "tonight": 1.0, "close": 0.75,
}

ACTS = [
    ("ACT ONE — the question, and the system that answers it", "cover", "the-answer"),
    ("ACT TWO — everything you just watched broke", "what-it-cost", "scoreboard-sql"),
    ("CODA — point the same four moves somewhere else", "worlds-live", "worlds-found"),
    ("CLOSE — the six rules, and what to build on Monday", "recap-six", "close"),
]


def text_of(markup):
    markup = re.sub(r"<br\s*/?>", " ", markup)
    flat = html.unescape(re.sub(r"<[^>]+>", "", markup))
    return re.sub(r"\s+", " ", flat).strip()


def mins(x):
    if x < 1:
        return f"{int(x * 60)} sec"
    if x == int(x):
        return f"{int(x)} min"
    return f"{x:g} min"


def read(sid):
    raw = open(os.path.join(SLIDES, f"{sid}.html"), encoding="utf-8").read()
    aside = re.search(r"<aside>([\s\S]*?)</aside>", raw)
    body = re.sub(r"<aside>[\s\S]*?</aside>", "", raw)

    head = re.search(r"<h[12][^>]*>([\s\S]*?)</h[12]>", body)
    eyebrow = re.search(
        r"<p[^>]*text-transform:uppercase[^>]*>([\s\S]*?)</p>", body
    )
    kinds = []
    moves = False
    if "<x-embed" in body:
        kinds.append("animated panel")
        moves = True
    if '<img src="/_blob' in body:
        # one of the five recorded demos; four of them are animated WebP
        still = "c799ba003b2ef5371111b837f6448d87" in body  # the moon chart
        kinds.append("chart from live data" if still else "recorded demo, animated")
        moves = not still
    if re.search(r"\$ (python|curl)", body):
        kinds.append("terminal output")

    return {
        "id": sid,
        "head": text_of(head.group(1)).replace("\n", " ") if head else sid,
        "eyebrow": text_of(eyebrow.group(1)) if eyebrow else "",
        "kinds": kinds,
        "moves": moves,
        "notes": html.unescape(aside.group(1)).strip() if aside else "",
    }


def build():
    deck = json.load(open(os.path.join(ROOT, "project", "deck.json")))
    order = deck["order"]
    slides = [read(s) for s in order]
    at = {s: i + 1 for i, s in enumerate(order)}
    total = sum(TIME.get(s, 1.0) for s in order)

    L = []
    w = L.append

    w("# Your presentation, explained\n")
    w(f"**{len(order)} slides. {total:g} minutes as written.** "
      "This is the only file you need on the day.\n")
    w("---\n")
    w("## The talk in one sentence\n")
    w("> **You ask \"is it worth going outside tonight?\" The model cannot")
    w("> answer it. Ten things are missing. We add them one at a time —")
    w("> and then everything you just watched breaks.**\n")
    w(f"Asked on slide {at['the-question']}, answered on slide "
      f"{at['the-answer']}. Slide {at['what-it-cost']} turns the talk over.\n")

    w("## The rhythm\n")
    w("Seven times in act one, the deck runs the same three beats:\n")
    w("| | | |")
    w("|---|---|---|")
    w("| **gap** | deep red, one line | *what it still cannot do* |")
    w("| **code** | navy, one function | *the fix, in a few lines* |")
    w("| **output** | a real recorded demo | *what actually came back* |\n")
    w("The red slides are the ones people forget to leave room for. Each is")
    w("about fifteen seconds of silence while the room gets ahead of you —")
    w("that anticipation is the reason they exist. Do not read them twice.\n")

    w("## The shape\n")
    w("| Slides | | Runs |")
    w("|---|---|---|")
    for title, a, b in ACTS:
        span = order[at[a] - 1: at[b]]
        t = sum(TIME.get(s, 1.0) for s in span)
        label = title.split("—")[0].strip().title()
        rest = title.split("—")[1].strip() if "—" in title else ""
        rest = rest[:1].upper() + rest[1:]
        w(f"| {at[a]}–{at[b]} | **{label}.** {rest} | {t:g} min |")
    w("")
    w(f"**Slide {at['what-it-cost']} is the hinge.** Stop there. The question")
    w("is answered and the room has had its payoff — if you simply carry on")
    w("they will feel the talk should have ended. Say you are starting the")
    w("second half on purpose, then speed up.\n")

    w("## The ten things\n")
    w("| | Needs | Gap | Code | Output |")
    w("|---|---|---|---|---|")
    rungs = [
        ("1–3", "Eyes, a loop, a first tool", "—", "cloud-code", "cloud-tonight"),
        ("4", "Something to look at", "gap-eyes", "sky-code", "sky-tonight"),
        ("5", "A sense of when", "gap-moon", "moon-code", "moon-tonight"),
        ("6", "Memory", "gap-memory", "memory-code", "memory-night-two"),
        ("7", "Judgement to chain", "gap-chain", "the-chain", "the-chain"),
        ("8", "The nerve to say nothing", "gap-silence", "the-silence", "the-silence"),
        ("9", "Somebody else's tools", "gap-mcp", "mcp", "mcp"),
        ("10", "A way to know it was right", "gap-right", "real-transcript", "real-transcript"),
    ]
    for n, need, g, c, o in rungs:
        cell = lambda s: "—" if s == "—" else f"{at[s]}"
        w(f"| {n} | {need} | {cell(g)} | {cell(c)} | {cell(o)} |")
    w("")

    w("## Cutting to fit\n")
    cuts = [
        ("the coda", ["worlds-live", "earth-live", "worlds-found"]),
        ("`l2-returns` + `the-traps`", ["l2-returns", "the-traps"]),
        ("MCP", ["gap-mcp", "mcp"]),
        ("Google Cloud", ["architecture", "scoreboard-sql"]),
        ("`l3-errors` + `l5-retries`", ["l3-errors", "l5-retries"]),
    ]
    w("| Cut | Slides | Saves | Leaves |")
    w("|---|---|---|---|")
    left = total
    for i, (label, ids) in enumerate(cuts, 1):
        saved = sum(TIME.get(s, 1.0) for s in ids)
        left -= saved
        nums = ", ".join(str(at[s]) for s in ids)
        w(f"| {i} | {label} — {nums} | {saved:g} | **{left:g}** |")
    w("")
    w("Cut evidence last. `l2-returns` and `the-traps` are the only two")
    w("lessons with no measured number behind them.\n")
    never = ["the-question", "cant-answer", "ten-things", "endpoint-to-tool",
             "cloud-tonight", "sky-tonight", "where-state-lives", "the-chain",
             "the-silence", "the-answer", "what-it-cost", "l1-docstring"]
    w("**Never cut:** " + ", ".join(str(at[s]) for s in never) +
      " — and never cut a gap slide without cutting its code and output too.\n")

    w("## Three things to say honestly\n")
    w("1. **The tools are real and ran today.** `python demo/tonight.py")
    w("   --tools-only` hits four live endpoints with no API key in about")
    w(f"   seven seconds. Every number on slides {at['cloud-tonight']}, "
      f"{at['sky-tonight']}, {at['moon-tonight']}, {at['real-transcript']} "
      f"and {at['the-answer']} came out of it.")
    w("2. **There is no recorded agent transcript in this deck, deliberately.**")
    w("   The Gemini free tier hung on every attempt — including past a hard")
    w("   100-second deadline, with the SDK's own timeout failing to fire.")
    w("   Rather than fake one, the deck shows the real tool results and says")
    w("   who chose what. If you get a clean run before the talk, add it after")
    w(f"   slide {at['the-loop']}.")
    w("3. **The sky on slides 11, 14 and 17 is rendered for one night.**")
    w("   `./refresh-live-data.sh` redraws them for the real date and prints")
    w("   every number that moves. **`cloud/` has never been executed.**\n")

    w("## Before you present\n")
    w("- [ ] Re-render the sky, cloud and moon charts for the actual date")
    w("- [ ] `python demo/tonight.py --tools-only` — expect 4/4")
    demos = sum(1 for s in slides if s["moves"])
    w(f"- [ ] Present from the web view, not a PDF — {demos} slides move")
    w("- [ ] Screenshot Gemini failing the question from your phone; it beats")
    w(f"      slide {at['cant-answer']}")
    w(f"- [ ] QR code on slide {at['close']}\n")
    w("---\n")

    act_start = {a: title for title, a, _ in ACTS}
    for i, s in enumerate(slides, 1):
        if s["id"] in act_start:
            w(f"\n# {act_start[s['id']]}\n")
        w(f"## {i} · `{s['id']}` · {mins(TIME.get(s['id'], 1.0))}\n")
        line = f"**{s['head']}**"
        if s["eyebrow"]:
            line += f" — *{s['eyebrow']}*"
        w(line + ("  " if s["kinds"] else "") )
        if s["kinds"]:
            w("*" + ", ".join(s["kinds"]) + "*")
        w("")
        w(s["notes"] if s["notes"] else "*(no notes on this slide)*")
        w("")

    out = "\n".join(L).rstrip() + "\n"
    open(os.path.join(ROOT, "PRESENTATION-GUIDE.md"), "w", encoding="utf-8").write(out)
    print(f"{len(order)} slides, {total:g} min  ->  PRESENTATION-GUIDE.md "
          f"({len(out):,} bytes)")
    gaps = [s for s in order if s not in TIME]
    if gaps:
        print("no timing for:", gaps)


if __name__ == "__main__":
    build()
