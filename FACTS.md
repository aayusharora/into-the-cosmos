# Facts sheet — every number in the deck

> **Re-render the sky and cloud map on the morning of the talk.** Slides 13
> and 20 are computed for the night of 5 November 2026 over Siliguri
> (26.73 N, 88.40 E). A different date means a different sky.

## Tonight over Siliguri — 5 Nov 2026, all keyless

| | | Source |
|---|---|---|
| Cloud, 19:00–23:00 | **3%**, falling to 1% by 23:00 | open-meteo |
| Saturn | **64.2° at 21:00 IST**, magnitude +0.48 | JPL Horizons |
| Moon | rises **03:00**, magnitude −7.49 | JPL Horizons |
| Kp index | **0.67** — quiet, no aurora | NOAA SWPC |

All four fetched by `demo/tonight.py --tools-only`, no API key, ~7 seconds.

## Tool latency — measured 5 Nov 2026

| Tool | Time |
|---|---|
| `sky_conditions` | 1.12s |
| `planets_tonight` | **4.31s** — four serial Horizons calls, one per planet |
| `moon_tonight` | 1.08s |
| `space_weather` | 0.48s |
| **total** | **6.99s** |

This is lesson 4 on slide 25.

## JPL Horizons takes codes, not names — verified

`COMMAND='Mars'` returns no ephemeris. It returns a disambiguation list:

```
4    Mars Barycenter
499  Mars
-3   Mars Orbiter Mission   (spacecraft)
-41  Mars Express           (spacecraft)
```

`COMMAND='499'` works. **Ask for Mars, get a spacecraft** — this is lesson 1
on slide 22, and the failure is a successful HTTP response, not an error.

## Every world we know — 6,451 confirmed exoplanets

One TAP query to the NASA Exoplanet Archive, keyless, 445 KB:

```sql
select pl_name, disc_year, pl_orbper, pl_rade from pscomppars
```

6,050 of them have both a size and a period — those are the dots on the coda
slide. 2 in 1992, 498 in 2010, **+1,504 in 2016 alone**, 6,451 today.

## Gemini facts to re-check before you present

| Claim | Status on 4 Nov 2026 |
|---|---|
| Free tier model | `gemini-3.8-flash` — free input and output |
| `gemini-4-argon` | **Paid only** — not on the free tier |
| Image models (`gemini-nano-banana-2.1` etc.) | **Paid only** — demo 07 costs money |
| Gemini CLI personal Google login | **Stopped 18 June 2026**; API keys unaffected |
| Google Search grounding | 5,000 free search requests/month on Gemini 3+ |

### The SDK version trap — verified by running into it, 5 Nov 2026

`client.interactions` **does not exist before google-genai 2.x.** This machine
had **1.41.0** installed, where the client exposes only `models`, `chats`,
`files`, `caches`, `tunings`, `batches` and `operations` — calling
`client.interactions.create(...)` raises:

```
AttributeError: 'Client' object has no attribute 'interactions'
```

which reads exactly like "this API doesn't exist" and is why so much writing
online still teaches `models.generate_content`. Latest on PyPI is **2.34.0**.

```bash
python3 -m venv .venv
.venv/bin/pip install --only-binary=:all: 'google-genai>=2.34'
```

`--only-binary=:all:` matters: a plain install tries to build `cryptography`
from source and fails without a Rust toolchain.

Confirmed on 2.34.0, the client exposes: `agents`, `environments`,
`interactions`, `triggers`, `webhooks`, `file_search_stores`, `voices`,
`auth_tokens` — none of which exist in 1.x. **Worth one line on stage:** if
`interactions` is missing, your SDK is a major version behind, not wrong.

### Lesson 1, actually measured — 5 Nov 2026

`demo/agent.py --lesson1 --model gemini-3.5-flash`, three runs of each. Same
question, same function, same model. The only difference is whether the
`hostname` parameter carries a description.

| | vague (`{"type":"string"}`) | fixed (with the KOI-351 hint) |
|---|---|---|
| First hostname tried | `Kepler-90` → **0 rows**, all 3 runs | `KOI-351` → **8 planets** |
| Calls to reach the answer | **2, 5, 5** | **1, 1, 1** |
| Other guesses it made | `Kepler 90`, `K00351`, a `LIKE '%Kepler-90%'` via another tool | none |

**The slide used to claim "0 rows. Every time." That is wrong** — the model
does recover. The honest and better result is that it costs 2–5× the calls,
varies run to run, and *only works because Kepler-90 is famous enough to be in
the training data*. There is no such recovery path for a private schema.

Raw transcripts: `demo/out/lesson1.json`, `lesson1_run2.json`, `lesson1_run3.json`.


### The client timeout does not fire — verified 6 Nov 2026

`http_options=HttpOptions(timeout=25_000)` on `interactions.create` did **not**
abort a hung call. Wrapped in a process-level `signal.alarm(100)`, the call was
still open at 100 seconds.

Two separate facts, both tested:

- On a *simple* call the timeout works — `timeout=5` raised `APITimeoutError`
  in 0.52s, which is how we know the unit is **milliseconds**.
- On a call that hangs, it does not fire at all.

**So do not rely on the SDK timeout as your only guard.** Put the agent behind
your own deadline — a thread, a subprocess, or a supervisor that can kill it.
This is lesson 5 one layer above where the talk teaches it.

The free tier was also intermittent all day: plain calls answered in 5.7s
while calls that hung were unrelated to tool count. Treat a live agent demo on
the free tier as something that will fail in front of an audience.

### `gemini-3.8-flash` returns 503 under load

Verified live: `503 service_unavailable — "gemini-3.8-flash is currently
experiencing high demand"`. The free tier is genuinely oversubscribed at
times. `demo/agent.py` retries three times with backoff and then falls back
to `gemini-3.7-flash`, then `gemini-3.5-flash`. **Do not demo a free-tier
model live without a fallback chain.** All three were visible on the key's
model list, alongside `gemini-flash-latest`.

## Gotcha if you script your own queries

The archive sits behind Cloudflare and returns **403 on large result sets**
from some networks. Small and aggregated queries are fine. If you need many
rows, aggregate first (`group by hostname`) or filter hard. Also: `python3 -I`
broke TLS for these requests in testing — run plain `python3`.
