#!/usr/bin/env python3
"""Generate PRESENTATION-GUIDE.md from the deck itself.

    python3 build-guide.py

Everything here is derived from project/deck.json and the <aside> on each
slide, so the guide cannot drift from what you will actually present. The
only hand-maintained thing is TIME: how long each slide runs. Anything not
listed gets DEFAULT.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.join(ROOT, "project", "slides")

DEFAULT = 0.75          # minutes, for any slide not named below

TIME = {
    # act 0, slow on purpose
    "title": 0.4, "kid": 1.0, "terrace": 1.3, "milky-way": 0.5,
    # act 1
    "asked-again": 0.5, "the-question": 0.4, "what-it-said": 1.6,
    "then-i-checked": 2.0, "diagnosis": 0.8, "flash-forward": 0.8,
    # act 2
    "first-problem": 0.5, "setup": 1.1, "cloud-map": 1.2, "the-url": 0.8,
    "byte-grid": 1.0, "whole-tool": 2.0, "the-note": 1.1, "the-decl": 0.8,
    "wiring": 1.6,
    # act 3, the spine
    "three-boxes": 1.4, "the-mistake": 1.5, "the-recipe": 1.2,
    "step-ask": 1.5, "step-run": 1.6, "step-loop": 1.5, "whole-agent": 0.6,
    # act 4
    "whats-in-it": 0.4, "sky-chart": 1.1, "horizons": 0.8,
    "clear-not-dark": 0.7, "moon-chart": 1.0, "one-number": 0.6,
    # act 5
    "it-keeps-asking": 0.9, "two-forgettings": 1.3, "memory-file": 1.1,
    "memory-code": 1.6,
    "night-one": 0.5, "night-seven": 1.2,
    # act 6
    "the-wall": 0.7, "mcp": 1.2, "mcp-code": 1.7, "mcp-output": 0.8,
    "tools-nine": 1.1,
    # act 7
    "just-a-script": 0.7, "watch-it-choose": 1.6, "left-out": 0.8,
    # act 8
    "the-answer": 1.4, "is-it-right": 0.8, "fails-quietly": 1.3,
    # act 9
    "first-thing": 0.4, "iss": 1.0, "olympus": 0.9, "earth-day": 0.7,
    "worlds": 0.6, "the-arsenal": 1.6,
    # act 10
    "go-build": 1.0, "the-point": 1.2, "repo": 0.6,
}


def notes_of(sid):
    path = os.path.join(SLIDES, f"{sid}.html")
    m = re.search(r"<aside>([\s\S]*?)</aside>", open(path, encoding="utf-8").read())
    return html.unescape(m.group(1)).strip() if m else ""


def headline(sid):
    """The biggest piece of text on the slide, for the contents table."""
    src = open(os.path.join(SLIDES, f"{sid}.html"), encoding="utf-8").read()
    src = re.sub(r"<aside>[\s\S]*?</aside>", "", src)
    for pat in (r"<h2[^>]*>([\s\S]*?)</h2>", r"<h1[^>]*>([\s\S]*?)</h1>",
                r'<p style="[^"]*font-size:(?:8|9|1\d\d)\d*px[^"]*">([\s\S]*?)</p>'):
        m = re.search(pat, src)
        if m:
            txt = re.sub(r"<[^>]+>", " ", m.group(1))
            txt = html.unescape(re.sub(r"\s+", " ", txt)).strip()
            if txt:
                return txt
    return sid.replace("-", " ")


def build():
    deck = json.load(open(os.path.join(ROOT, "project", "deck.json")))
    order = deck["order"]
    acts = [(s["start"], s["description"]) for s in deck["sections"].values()]
    starts = {sid: desc for sid, desc in acts}

    total = sum(TIME.get(s, DEFAULT) for s in order)
    L = []
    w = L.append

    w("# Into the Cosmos with Gemini")
    w("## Your presentation, explained\n")
    w(f"**{len(order)} slides. About {total:.0f} minutes as written.** "
      "This is the only file you need on the day.\n")
    w("> Generated from the deck. Every word below is the speaker note on "
      "the slide itself, so this file cannot drift from what you present. "
      "Edit `build-slides.py`, not this.\n")
    w("---\n")

    w("## The talk in one sentence\n")
    w("> **A kid who could not see the sky, an AI that could not answer "
      "him, and the agent he built until it could.**\n")
    w("Every capability arrives because the story breaks without it, not "
      "because a list says it is next.\n")

    w("## The five things to get right\n")
    w("1. **Slide 3, the Delhi joke.** Stop talking. Let the laugh finish. "
      "It buys you the next three minutes.")
    w("2. **Slide 7, praise the answer.** Gemini did well. Say so and mean "
      "it. If you mock it, the room stops trusting you.")
    w(f"3. **Slide {order.index('wiring') + 1}, DECLS and IMPL.** This is the "
      "bridge from an endpoint to a tool, and it is the thing developers "
      "came for. Do not rush it.")
    w(f"4. **Slide {order.index('the-mistake') + 1}, the red X.** Gemini never "
      "calls your function. This is the one fact most of the room has wrong.")
    w(f"5. **Slide {order.index('the-arsenal') + 1}, the arsenal.** Stand "
      "still and stop talking. That is the slide they photograph.\n")

    w("## The shape\n")
    w("| Slides | Act | Runs |")
    w("|---|---|---|")
    bounds = []
    for i, (sid, desc) in enumerate(acts):
        a = order.index(sid) + 1
        b = (order.index(acts[i + 1][0]) if i + 1 < len(acts) else len(order))
        bounds.append((a, b, desc))
    for a, b, desc in bounds:
        mins = sum(TIME.get(s, DEFAULT) for s in order[a - 1:b])
        w(f"| **{a}&ndash;{b}** | {desc} | {mins:.0f} min |")
    w("")

    w("## If you are running long\n")
    w(f"As written this is **{total:.0f} minutes**. Cut in this order; none "
      "of these breaks the story:\n")
    CUTS = (
        ("byte-grid", "the filter is annotated on the whole-tool slide now"),
        ("the-decl", "the docstring is already visible in the real function"),
        ("clear-not-dark", "the point survives on the moon chart"),
        ("night-one", "night seven implies it"),
        ("the-wall", "the MCP slide carries the idea alone"),
        ("just-a-script", "the decision trace makes the contrast itself"),
        ("whats-in-it", "a pure link slide"),
        ("first-thing", "a pure link slide"),
        ("whole-agent", "a victory lap, lovely, not load bearing"),
        ("mcp-output", "the diagram already made the point"),
        ("worlds", "pure spectacle, not load bearing"),
        ("earth-day", "same"),
    )
    for sid, why in CUTS:
        if sid in order:
            w(f"- **Slide {order.index(sid) + 1}**, {headline(sid)} &mdash; "
              f"{why}  `-{TIME.get(sid, DEFAULT):g} min`")
    trim = sum(TIME.get(s, DEFAULT) for s, _ in CUTS if s in order)
    w(f"\nAll twelve come to **{trim:.0f} minutes**, which lands the talk at "
      f"about **{total - trim:.0f}**.")
    lo, hi = order.index("whole-tool") + 1, order.index("whole-agent") + 1
    w(f"\nNever cut slides {lo} to {hi}. That stretch is the talk: the "
      "function, the wiring, and the loop that runs it.\n")

    w("## On the morning\n")
    w("```bash\n./refresh-live-data.sh\n```\n")
    w("It redraws the three charts from live data, re-renders the ISS "
      "ground track, checks all six tools and rebuilds. Then read the "
      "numbers it prints and fix any slide that names one.\n")
    w("Slides that quote tonight's sky: "
      + ", ".join(str(order.index(s) + 1) for s in
                  ("cloud-map", "sky-chart", "moon-chart", "watch-it-choose",
                   "the-answer", "iss") if s in order)
      + ".\n")
    w("---\n")

    w("## Every slide, in order\n")
    for i, sid in enumerate(order, 1):
        if sid in starts:
            w(f"\n### {starts[sid]}\n")
        mins = TIME.get(sid, DEFAULT)
        w(f"**{i}. {headline(sid)}**  &nbsp;&nbsp;`{mins:g} min`  "
          f"&nbsp;&nbsp;<sub>{sid}</sub>\n")
        n = notes_of(sid)
        w("\n".join("> " + ln if ln.strip() else ">" for ln in n.split("\n"))
          if n else "> *(no notes)*")
        w("")

    out = os.path.join(ROOT, "PRESENTATION-GUIDE.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    missing = [s for s in order if s not in TIME]
    print(f"PRESENTATION-GUIDE.md  {len(order)} slides  {total:.0f} min")
    if missing:
        print(f"no TIME entry (using {DEFAULT}): {missing}")


if __name__ == "__main__":
    build()
