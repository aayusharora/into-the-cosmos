# The cloud half

Google Cloud is not a product tour in this talk. Each service shows up as the
answer to a problem the audience has already watched happen.

## Why each piece is here

| Problem you hit on stage | Why the laptop can't fix it | Google Cloud |
|---|---|---|
| The transit search takes minutes | A tool that slow cannot sit inside an agent loop — the model calls it three times and the demo dies | **Cloud Run Job** does the heavy search once; the agent's *tool* reads a precomputed row and returns in milliseconds |
| The Exoplanet Archive throws 403s and 525s | You don't control their Cloudflare | Snapshot ground truth into **BigQuery** and read your own copy |
| You can't tell if any of it works | Scoring 500 stars is three days on a laptop | **Cloud Run Jobs**, 500 tasks in parallel via `CLOUD_RUN_TASK_INDEX`, results to **BigQuery**, one SQL query gives recall |
| The API key is in your shell history | — | **Secret Manager**, mounted as an env var at deploy time |
| It only runs when you're watching | — | **Cloud Scheduler** pokes a **Cloud Run** service each morning |

The honest framing for the room: **your agent is only as good as its tools,
and past a certain point your tools are an infrastructure problem, not a
prompting problem.**

## The shape

```
  Cloud Scheduler ──06:00──▶ Cloud Run (service)  ──▶ Gemini + MCP ──▶ inbox
                                     │
                                     └── reads ──▶ BigQuery
                                                      ▲
  Cloud Run Job ×500 tasks ───── writes ──────────────┘
    (the slow BLS search)
```

One image, two entry points. The *job* does minutes of work per star. The
*service* answers in seconds because it only ever reads a table.

That split is the lesson. An agent tool must return fast; anything slow has to
happen somewhere else, earlier.

## Files

| | |
|---|---|
| `search_worker.py` | one task = one star. Reads `CLOUD_RUN_TASK_INDEX`, writes rows to BigQuery |
| `Dockerfile` | one image, two entry points |
| `schema.sql` | the tables, and **the scoring query** — the one artifact worth a slide |
| `deploy.sh` | every `gcloud` command, in order |

## ⚠️ What is and isn't verified

**Verified, run on a real machine:**

- `demo/agent.py --tools-only` — 5/5 tools, live NASA data
- `demo/find_planets.py` — real Kepler photometry, real scoreboard
- `demo/sky_report.py --raw` — today's real sky data
- `demo/worlds.html` — real Mars and Moon tiles, flown into Olympus Mons

**Not verified — written from docs, never executed:**

- Everything in this directory. There was no Google Cloud billing account
  available, so no `gcloud` command here has ever run.
- The BigQuery schema and scoring query are untested SQL.
- Expect at least one flag to have moved. **Dry run it before you present.**

## Naming, as of November 2026

Vertex AI was renamed the **Gemini Enterprise Agent Platform** at Cloud Next
in April 2026, and its Agent Engine may now be called Agent Runtime (one
secondary source; unconfirmed in Google's docs). Existing docs and samples
still say "Vertex AI" everywhere.

Say the new name once, note the rename, then build on Cloud Run, Cloud Run
Jobs, Scheduler, Secret Manager and BigQuery — those names are stable, they
are the right fit for this problem, and a student can reach all of them.

The managed agent platforms are real but enterprise-shaped: a project, IAM
roles, an admin. For one person with one script, a container and a cron job is
the honest answer.
