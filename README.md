# Into the Cosmos with Gemini

**Open one file: [PRESENTATION-GUIDE.md](PRESENTATION-GUIDE.md).** Every slide,
what's on it, and what to say. Everything else here is backup.

Hosted: **https://aayusharora.github.io/into-the-cosmos/**
(← → or click · **N** notes · **F** fullscreen · `#17` jumps to a slide)

---

## The talk in one sentence

> You ask *"is it worth going outside tonight?"* The model cannot answer it.
> **Ten things are missing.** We add them one at a time — and then everything
> you just watched breaks.

Asked on slide 2. Answered on slide 31. Every number on screen came from a
live endpoint, today.

## The rhythm

Act one runs the same three beats, seven times:

| | | |
|---|---|---|
| 🔴 **gap** | deep red, one line | *what it still cannot do* |
| ⌨️ **code** | navy, one function | *the fix, in a few lines* |
| ▶️ **output** | a recorded demo, or real output typeset | *what actually came back* |

The red slides are the ones to leave room for. Each is about fifteen seconds
of silence while the room gets ahead of you.

## The system

Four tools, all keyless, all real — `demo/tonight.py`:

```
sky_conditions    cloud cover tonight         open-meteo
planets_tonight   what is above the horizon   JPL Horizons
moon_tonight      when the Moon spoils it     JPL Horizons
space_weather     aurora chance               NOAA SWPC
```

```bash
python demo/tonight.py --tools-only
```

No API key. About seven seconds. Expect **4/4**.

## The 48 slides

| # | Slide | Time | In a few words |
|---|---|---|---|
| 1 | cover | 30 sec | Title, orbiting planets |
| 2 | the-question | 1.5 min | 🎯 **"Is it worth going outside tonight?"** |
| 3 | cant-answer | 1 min | Why it *cannot* know |
| 4 | ten-things | 1 min | **The spine** — ten things it needs |
| 5 | what-were-building | 1.25 min | The four tools, end to end |
| 6 | fifteen-lines | 1 min | You own the loop |
| 7 | the-declaration | 1 min | ⌨️ The model never sees your code |
| 8 | the-loop | 1.25 min | ⌨️ Four moves |
| 9 | cloud-code | 30 sec | ⌨️ Will it be clear? |
| 10 | endpoint-to-tool | 1.25 min | ⚡ **1,285 bytes in, 133 out** — you are the filter |
| 11 | cloud-tonight | 1 min | ▶️ Cloud over Siliguri, animated |
| 12 | gap-eyes | 15 sec | 🔴 It has no idea what is *in* the sky |
| 13 | sky-code | 30 sec | ⌨️ What is up there tonight? |
| 14 | sky-tonight | 1.25 min | ▶️ **Tonight's sky, dusk to dawn** |
| 15 | gap-moon | 15 sec | 🔴 Clear is not the same as dark |
| 16 | moon-code | 30 sec | ⌨️ The docstring that says "go now" |
| 17 | moon-tonight | 1 min | 📈 **The Moon is not invited until three** |
| 18 | gap-memory | 15 sec | 🔴 Every night it asks where you live |
| 19 | memory-code | 30 sec | ⌨️ recall() and remember() |
| 20 | where-state-lives | 1.25 min | **Three places state can live.** Pick on purpose |
| 21 | memory-night-one | 45 sec | 📈 It knows nothing, so it asks |
| 22 | memory-night-two | 45 sec | 📈 A week later — no questions |
| 23 | gap-chain | 15 sec | 🔴 **A script, not an agent** |
| 24 | the-chain | 1.5 min | Each call chosen by the last |
| 25 | gap-silence | 15 sec | 🔴 It reports the nothing too |
| 26 | the-silence | 1 min | The fifth call: say nothing |
| 27 | gap-mcp | 15 sec | 🔴 You will not write every tool |
| 28 | mcp | 1.5 min | ⌨️ Somebody else's tools, plugged in |
| 29 | gap-right | 15 sec | 🔴 **It sounds right. Is it?** |
| 30 | real-transcript | 1 min | ⚡ 4/4, no key, seven seconds |
| 31 | the-answer | 1.5 min | 🎯 **"Yes. Go outside."** |
| 32 | what-it-cost | 30 sec | 🔀 **The hinge** — now everything breaks |
| 33 | the-six | 1 min | Six ways the tools broke |
| 34 | l1-docstring | 2 min | ⚡ Ask for Mars, get a spacecraft |
| 35 | l2-returns | 45 sec | Empty is an answer |
| 36 | l3-errors | 1.25 min | Write the error for the model |
| 37 | the-traps | 45 sec | ⌨️ Three silent failures |
| 38 | l4-latency | 1.25 min | ⚡ Measured: 6.99s of tools |
| 39 | l5-retries | 45 sec | Retry inside the tool |
| 40 | l6-scoring | 1.25 min | ⚡ I thought all four worked |
| 41 | architecture | 1.75 min | Answers lesson 4 — move the slow part off the loop |
| 42 | scoreboard-sql | 1.25 min | Answers lesson 6 — was it right? |
| 43 | worlds-live | 1 min | ▶️ **Descent to Olympus Mons** |
| 44 | earth-live | 1 min | ▶️ **A day of Earth** |
| 45 | worlds-found | 1.25 min | ▶️ **6,050 worlds fill the sky** |
| 46 | recap-six | 1 min | The six rules. Photo slide |
| 47 | tonight | 1 min | Three things to build |
| 48 | close | 45 sec | Links, QR, thank you |

🎯 question and answer · 🔀 the hinge · 🔴 gap · ⌨️ code · ▶️ recorded motion ·
📈 real output, drawn · ⚡ measured

**Ten slides actually animate** — six drawn panels (1, 2, 5, 41, 45, 46) and
four recorded WebP demos (11, 14, 43, 44). Slide 17 and the two memory nights
are real output rendered as stills.

**44.5 minutes as written.** Act one (1–31) is a complete talk on its own in
about 26. The guide has an ordered cut table down to 33.

## Building

```bash
python3 build-dist.py    # project/ -> dist/index.html + dist/img  (hostable)
python3 build-guide.py   # slide <aside>s -> PRESENTATION-GUIDE.md
```

`build-guide.py` reads the speaker notes out of the slides themselves, so the
guide cannot drift from the deck. The only judgement calls in it are the
per-slide timings, which live in one dict at the top.

To publish: copy `dist/index.html` and `dist/img/` to the root of
`aayusharora/into-the-cosmos` on `main`, and GitHub Pages does the rest.

## Before you present

1. Re-render for the actual date. One command, no key:
   ```bash
   ./refresh-live-data.sh
   ```
   It redraws slides 11, 14 and 17 from live data and prints every number
   that depends on them. The deck ships rendered for **13 Nov 2026**
2. `python demo/tonight.py --tools-only` — expect 4/4
3. Present from the web view, not a PDF — **10 slides move**
4. Screenshot Gemini failing the question from your phone; it beats slide 3
5. QR code on slide 48

## The files

| File | What it's for |
|---|---|
| **PRESENTATION-GUIDE.md** | **The one you use.** Every slide + what to say |
| TALK-PLAN.md | Why the talk is shaped this way |
| FACTS.md | Every number, with the query behind it |
| CFP.md | The submitted abstract |
| `build-dist.py` | project/ → the standalone hosted deck |
| `build-guide.py` | slides → PRESENTATION-GUIDE.md |
| `project/` | `deck.json` + one HTML file per slide |
| `demo/tonight.py` | The four tools and the agent loop |
| `demo/` | Live pages, and the renderers for the recorded demos |
| `cloud/` | Google Cloud config. **Written, never run** |
| `index.html`, `img/` | The built deck. This is what GitHub Pages serves |

`build-dist.py` writes into `dist/`, which is gitignored. To publish, copy
`dist/index.html` and `dist/img/` over the two at the repo root and push.

You will need a virtualenv for `demo/agent.py`. `client.interactions` does
not exist in google-genai 1.x, and the `AttributeError` reads exactly like
the API not existing:

```bash
python3 -m venv .venv
.venv/bin/pip install --only-binary=:all: 'google-genai>=2.34'
```

`--only-binary=:all:` matters: a plain install tries to build `cryptography`
from source and fails without a Rust toolchain. The four tools in
`demo/tonight.py` need none of this and no API key.

## Honest warnings

- **The tools are real and ran today.** The agent runs are **recorded** — the
  Gemini free tier stalled on five consecutive attempts while this was built.
- **There is no agent transcript in the deck.** The free tier hung on every
  attempt, including past a hard 100-second deadline with the SDK timeout
  failing to fire. Nothing was faked; the deck shows real tool output instead.
- **`cloud/` has never been executed.** No billing account.
- Needs `google-genai>=2.34`; `client.interactions` is absent in 1.x and the
  `AttributeError` looks exactly like the API not existing. See `FACTS.md`.
