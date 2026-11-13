# Into the Cosmos with Gemini — the plan

**The problem with the current deck, stated plainly:** it opens with *"Is it
worth going outside tonight?"* and then never answers it. By slide 10 the talk
is about finding planets in Kepler photometry — a different question, with
different tools, that nobody in the room asked. The hook is abandoned.

This plan builds the system that actually answers the opening question, and
makes everything else serve it.

---

## 1. What answering that question actually requires

Say it out loud and the system designs itself:

> *"Is it worth going outside tonight?"*

| To answer it you need | Where it comes from | Verified |
|---|---|---|
| Where you are | **Memory**, not a tool | — |
| Will it be clear? | open-meteo hourly cloud cover | ✅ keyless |
| Will the Moon wash it out? | computed, no network | ✅ offline |
| What is above the horizon? | JPL Horizons, alt/az per body | ✅ keyless |
| Anything unusual tonight? | NOAA SWPC Kp + aurora oval | ✅ keyless |
| Will the ISS go over? | Celestrak TLE, propagated locally | ✅ keyless |
| What can *you* see with what you own? | **Memory** | — |

All five endpoints tested on 13 Nov 2026. None needs a key.

**Tonight in Delhi, really:** cloud cover 0% at 20:00–22:00, Kp 0.67 (quiet).
The honest answer is *yes, go outside* — and the agent can say so with
evidence. That is the ending the talk has never had.

---

## 2. The tools

Six functions. This is the orange box from slide 3.

```
sky_conditions(lat, lon)   → hourly cloud %, visibility, for tonight
moon_tonight(lat, lon)     → phase, illumination, rise/set       (computed)
planets_tonight(lat, lon)  → which planets are up, altitude, magnitude
space_weather()            → Kp index, aurora probability
iss_passes(lat, lon)       → next visible passes                 (from TLE)
remember(key, value)       → location, kit, what you have seen
```

Note what is *not* a tool: knowing where you live. That is memory, and the
distinction is one of the talk's best teaching moments.

## 3. Why this question needs memory

A one-shot agent asks "where are you?" every single night. That is not an
assistant, it is a form.

- **Night one:** it asks for location and kit, then answers. It stores both.
- **Night two:** no questions. It already knows you are in Delhi with 10×50s,
  and that you saw Jupiter last week — so it leads with something new.

Memory is `previous_interaction_id` for the conversation, plus a small store
for the facts that outlive it. Two slides, and it is the difference between a
demo and something you would actually use.

## 4. Why this question needs a loop

A single tool call cannot answer it. Watch the chain:

1. `sky_conditions` → cloudy at 20:00, clear from 23:00
2. agent decides to look later, not to give up
3. `moon_tonight` → moon sets 01:10, so after that it is properly dark
4. `planets_tonight` → Saturn up until 02:00
5. `space_weather` → Kp 0.67, no aurora, do not mention it

Five calls, each one chosen because of what the last one returned. That is
agency, and it is the same four-move loop from slide 5 — now doing something
worth watching.

## 5. Where MCP earns its place

You will not own every tool. The honest framing: your six functions are
yours; a remote MCP server is somebody else's, plugged in without you writing
it. Verified constraints: **remote servers only, Streamable HTTP, no SSE, and
no hyphen in the server name.**

Do not promise a specific public server on stage without testing it that
morning.

---

## 6. The visuals — all recordable, all real

Recorded, not live, because the embedded panels in these slides cannot reach
the network at all (tested: 8 tile requests, 0 loaded).

| # | Visual | Source | Status |
|---|---|---|---|
| 1 | **Tonight's sky over Delhi**, hour by hour | Horizons alt/az | to build — *the money shot* |
| 2 | **Cloud cover over India** through the evening | open-meteo grid | to build |
| 3 | **The aurora oval right now** | NOAA ovation (919 KB grid) | to build |
| 4 | **ISS ground track** | Celestrak TLE | to build |
| 5 | **Moon phase tonight** | computed | to build |
| 6 | Earth turning through a day | DSCOVR EPIC | ✅ built |
| 7 | Descent to Olympus Mons | Viking tiles | ✅ built |
| 8 | **The agent answering, recorded** | real run | to record |

Numbers 1 and 3 are the two that make the question feel answered.

---

## 7. The deck, re-planned

| Act | Slides | What happens |
|---|---|---|
| 0 | 1–2 | The question |
| 1 | 3–4 | Ask Gemini cold. It cannot answer — no senses, no memory, no location |
| 2 | 5–6 | **The loop**, four moves. Code → recorded output |
| 3 | 7–8 | One sense: clouds. Code → cloud map over India tonight |
| 4 | 9–10 | Eyes: what is actually up. Code → the sky over Delhi tonight |
| 5 | 11–12 | Memory: it should not ask where you live twice. Night one vs night two |
| 6 | 13–14 | The chain: cloudy at 8, clear at 11 — the agent decides to wait |
| 7 | 15 | Somebody else's tools: MCP |
| 8 | 16 | **The answer.** Recorded run, real data, tonight |
| 9 | 17–24 | It broke six times — the lessons, now about *this* system |
| 10 | 25–26 | Scale it: Cloud Run, BigQuery, the scoring query |
| 11 | 27–29 | Recap, go build, close |

## 8. What this costs

Honest accounting of what gets retired:

- **Kept as-is:** the question, what-we're-building, the loop + its output,
  the six lessons, architecture, the scoring query, recap, close.
- **Kept but moved later:** Earth turning, Mars descent — they become "point
  the same thing somewhere else," not the main event.
- **Retired or demoted:** Kepler-90 orrery, the transit animation, 6,050
  worlds, the fold, the gallery, HR 8799, the BLS transcript. All real and
  all good — but they answer a question nobody asked.

That is roughly eight slides of built work stepping aside. Worth it: the talk
currently has no ending, and this gives it one.

**The exoplanet material has a home if you want it:** one slide at the end —
*"the same four moves, pointed at a harder problem"* — showing the 6,050
worlds and saying the loop did not change. That keeps the best visual and
costs ninety seconds.
