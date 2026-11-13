"""The agent. Real tools, real NASA data, a real tool-call transcript.

Written against the Interactions API, which is what Google documents as of
5 Nov 2026 — NOT `models.generate_content` with Python callables. There is no
automatic function calling. Verbatim from the docs: "The model doesn't execute
the function itself." So the loop is yours:

    create → walk the steps → run the function → send the result back

See `converse()` below; that is the whole thing, and it is about twenty lines.

Three modes:

    python demo/agent.py --tools-only   # no key — proves the five tools work
    python demo/agent.py                # the agent, needs GEMINI_API_KEY
    python demo/agent.py --lesson1      # the docstring experiment, needs a key

⚠️ STATUS: `--tools-only` has been run and passes 5/5 against live endpoints.
The two modes that call Gemini have NEVER been run — there was no API key on
this machine. The API shape comes from Google's documentation, not from a
successful call. Run them before putting their output on a slide.

Transcripts are written to demo/out/ so slides can quote them verbatim
instead of anyone inventing terminal output.
"""

import argparse
import csv
import io
import json
import os
import sys
import urllib.parse
import urllib.request

MODEL = "gemini-3.8-flash"          # free tier
AU_KM = 149_597_870.7
MOON_KM = 384_400.0

C_TOOL, C_OK, C_DIM, C_WARN, C_OFF = "\033[36m", "\033[32m", "\033[90m", "\033[33m", "\033[0m"


def _get(url, timeout=60, tries=3):
    """GET with a short retry.

    The Exoplanet Archive sits behind Cloudflare and intermittently returns
    403 or 525 for requests that succeed moments later, so one attempt is not
    enough to call a tool broken.
    """
    import time

    req = urllib.request.Request(url, headers={"User-Agent": "into-the-cosmos/1.0"})
    last = None
    for n in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode()
        except Exception as exc:
            last = exc
            if n < tries - 1:
                time.sleep(1.5 * (n + 1))
    raise last


def _trace(name, **kw):
    args = ", ".join(f"{k}={v!r}" for k, v in kw.items())
    print(f"  {C_DIM}↳{C_OFF} {C_TOOL}{name}{C_OFF}({args})", flush=True)


# ----------------------------------------------------------------- the tools

def closest_approach_this_week() -> dict:
    """Find the asteroid passing closest to Earth in the next seven days.

    Returns its name, the date and time of closest approach, how far away it
    gets in kilometres, how that compares to the Moon's distance, and how fast
    it is moving.
    """
    _trace("closest_approach_this_week")
    url = ("https://ssd-api.jpl.nasa.gov/cad.api"
           "?date-min=now&date-max=%2B7&dist-max=0.05&sort=dist")
    d = json.loads(_get(url))
    if not d.get("data"):
        return {"found": False, "reason": "nothing inside 0.05 AU this week"}
    g = dict(zip(d["fields"], d["data"][0]))
    km = float(g["dist"]) * AU_KM
    return {
        "found": True,
        "object": g["des"],
        "closest_approach_utc": g["cd"],
        "distance_km": round(km),
        "distance_in_moon_distances": round(km / MOON_KM, 2),
        "relative_speed_kms": round(float(g["v_rel"]), 2),
        "absolute_magnitude_H": float(g["h"]),
    }


def latest_earth_image() -> dict:
    """Get the most recent full-disc photograph of Earth taken from space.

    Returns the image identifier, when it was taken, which point on Earth was
    facing the camera, and a direct link to the PNG.
    """
    _trace("latest_earth_image")
    d = json.loads(_get("https://epic.gsfc.nasa.gov/api/natural"))
    if not d:
        return {"found": False}
    f = d[-1]
    c = f["centroid_coordinates"]
    day = f["date"][:10].replace("-", "/")
    return {
        "found": True,
        "identifier": f["image"],
        "taken_utc": f["date"],
        "sub_satellite_lat": round(c["lat"], 2),
        "sub_satellite_lon": round(c["lon"], 2),
        "png_url": f"https://epic.gsfc.nasa.gov/archive/natural/{day}/png/{f['image']}.png",
    }


def exoplanet_count(where: str = "") -> dict:
    """Count confirmed exoplanets in the NASA Exoplanet Archive.

    Args:
        where: optional SQL condition, e.g. "discoverymethod='Transit'" or
            "disc_facility='Kepler'". Leave empty to count all of them.
    """
    _trace("exoplanet_count", where=where)
    q = "select count(*) as n from pscomppars"
    if where:
        q += f" where {where}"
    url = ("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
           + urllib.parse.urlencode({"query": q, "format": "csv"}))
    rows = list(csv.DictReader(io.StringIO(_get(url, timeout=120))))
    return {"condition": where or "all", "count": int(rows[0]["n"])}


def planets_of_star(hostname: str) -> dict:
    """List the confirmed planets around one star, with their orbits.

    Args:
        hostname: the star as the archive names it, e.g. "KOI-351" for
            Kepler-90. If a lookup comes back empty the archive may file the
            star under a different name.
    """
    _trace("planets_of_star", hostname=hostname)
    q = ("select pl_name,pl_orbper,pl_rade,pl_orbsmax from pscomppars "
         f"where hostname='{hostname}' order by pl_orbsmax")
    url = ("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
           + urllib.parse.urlencode({"query": q, "format": "csv"}))
    rows = list(csv.DictReader(io.StringIO(_get(url, timeout=120))))
    if not rows:
        return {"hostname": hostname, "found": 0,
                "hint": "no rows — the archive may list this star under another name"}
    return {
        "hostname": hostname,
        "found": len(rows),
        "planets": [{"name": r["pl_name"],
                     "period_days": float(r["pl_orbper"]),
                     "radius_earth": float(r["pl_rade"]) if r["pl_rade"] else None,
                     "distance_au": float(r["pl_orbsmax"]) if r["pl_orbsmax"] else None}
                    for r in rows],
    }


def planet_image(query: str) -> dict:
    """Find a real NASA photograph of a planet or planetary system.

    Returns real telescope and spacecraft imagery, not illustrations. Good
    queries name a target: "HR 8799" (four exoplanets photographed around
    another star), "Jupiter Juno", "Saturn Cassini", "Olympus Mons". Check
    the returned title for the word "illustration" or "artist" — the library
    contains both, and only the photographs are evidence.

    Args:
        query: what to look for, e.g. "HR 8799".
    """
    _trace("planet_image", query=query)
    url = ("https://images-api.nasa.gov/search?"
           + urllib.parse.urlencode({"q": query, "media_type": "image"}))
    items = json.loads(_get(url))["collection"]["items"]
    if not items:
        return {"found": 0, "hint": "no match — try the mission name too, "
                                    "e.g. 'Jupiter Juno' rather than 'Jupiter'"}
    out = []
    for it in items[:5]:
        d = it["data"][0]
        out.append({
            "nasa_id": d["nasa_id"],
            "title": d["title"],
            "date": d.get("date_created", "")[:10],
            "description": (d.get("description") or "")[:240],
            # ~orig is the only variant guaranteed to exist; the ~medium URL
            # the search result advertises 403s for plenty of assets.
            "image_url": f"https://images-assets.nasa.gov/image/{d['nasa_id']}"
                         f"/{d['nasa_id']}~orig.jpg",
        })
    return {"found": len(out), "results": out}


TOOLS = [closest_approach_this_week, latest_earth_image, exoplanet_count,
         planets_of_star, planet_image]

IMPL = {fn.__name__: fn for fn in TOOLS}


# --------------------------------------------------------- tool declarations
#
# Interactions does NOT accept Python callables. You hand it plain dicts and
# it hands you back the name and arguments it wants; running the function is
# your job. These descriptions are the entire interface the model ever sees —
# it never reads the code below them. That is lesson 1, in the type system.

def _decl(name, description, properties=None, required=None):
    return {
        "type": "function",
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties or {},
            "required": required or [],
        },
    }


# The hostname description is the whole of lesson 1. `--lesson1` swaps it for
# the version without the KOI-351 hint and runs the same question again.
HOSTNAME_FIXED = {
    "type": "string",
    "description": ('the star as the archive names it, e.g. "KOI-351" for '
                    "Kepler-90. If a lookup comes back empty the archive may "
                    "file the star under a different name."),
}
HOSTNAME_VAGUE = {"type": "string"}


def declarations(hostname_param=HOSTNAME_FIXED, star_desc=None):
    return [
        _decl("closest_approach_this_week",
              "Find the asteroid passing closest to Earth in the next seven "
              "days. Returns its name, the date and time of closest approach, "
              "how far away it gets in kilometres, how that compares to the "
              "Moon's distance, and how fast it is moving."),
        _decl("latest_earth_image",
              "Get the most recent full-disc photograph of Earth taken from "
              "space. Returns the image identifier, when it was taken, which "
              "point on Earth was facing the camera, and a link to the PNG."),
        _decl("exoplanet_count",
              "Count confirmed exoplanets in the NASA Exoplanet Archive.",
              {"where": {"type": "string",
                         "description": "optional SQL condition, e.g. "
                                        "\"discoverymethod='Transit'\". "
                                        "Leave empty to count all of them."}}),
        _decl("planets_of_star",
              star_desc or "List the confirmed planets around one star, with "
                           "their orbits.",
              {"hostname": hostname_param}, ["hostname"]),
        _decl("planet_image",
              "Find a real NASA photograph of a planet or planetary system. "
              "Returns telescope and spacecraft imagery, not illustrations. "
              'Good queries name a target: "HR 8799", "Jupiter Juno". Check '
              'the returned title for "illustration" or "artist" — the '
              "library holds renders alongside real photographs.",
              {"query": {"type": "string",
                         "description": "the target to photograph"}},
              ["query"]),
    ]


SYSTEM = ("You are an observational astronomer. Answer only from tool "
          "results — never from memory. Always give units. If a tool returns "
          "nothing useful, say so and try a different approach rather than "
          "guessing.")

QUESTION = (
    "Is it worth going outside tonight? I'm in Delhi with 10x50 binoculars. "
    "Also tell me what's passing closest to Earth this week and how that "
    "compares to the Moon's distance."
)


# ----------------------------------------------------------------- the modes

def tools_only():
    print(f"{C_WARN}tools-only mode — no Gemini, no API key. "
          f"Proving the instruments work.{C_OFF}\n")
    checks = [
        ("closest asteroid", closest_approach_this_week, {}),
        ("latest Earth image", latest_earth_image, {}),
        ("all confirmed planets", exoplanet_count, {}),
        ("found by transit", exoplanet_count, {"where": "discoverymethod='Transit'"}),
        ("Kepler-90's system", planets_of_star, {"hostname": "KOI-351"}),
    ]
    ok = 0
    for label, fn, kw in checks:
        print(f"{label}:")
        try:
            out = fn(**kw)
            print(f"  {C_OK}✓{C_OFF} {json.dumps(out)[:220]}\n")
            ok += 1
        except Exception as exc:
            print(f"  \033[31m✗ {type(exc).__name__}: {exc}{C_OFF}\n")
    print(f"{ok}/{len(checks)} tools working")
    return 0 if ok == len(checks) else 1


KEY_FILE = os.path.expanduser("~/.config/gemini/api_key")


def _need_key():
    """Env var first, then a key file outside this project.

    The file keeps the key out of the repo, out of your shell history and out
    of anything that gets published with these slides.
    """
    if os.environ.get("GEMINI_API_KEY"):
        return None
    if os.path.exists(KEY_FILE):
        key = open(KEY_FILE).read().strip()
        if key:
            os.environ["GEMINI_API_KEY"] = key
            return None
    print(f"{C_WARN}No Gemini API key.{C_OFF}\n"
          f"Get a free one at aistudio.google.com (free tier covers {MODEL}),\n"
          f"then either:\n"
          f"  mkdir -p ~/.config/gemini && pbpaste > {KEY_FILE} && chmod 600 {KEY_FILE}\n"
          f"or:\n"
          f"  export GEMINI_API_KEY=...\n\n"
          f"To check the tools without a key: python demo/agent.py --tools-only")
    return 2


def _arguments(step):
    """step.arguments is a dict on some SDK builds and a JSON string on others."""
    args = getattr(step, "arguments", None)
    if args is None:
        args = getattr(step, "args", None) or {}
    if isinstance(args, str):
        args = json.loads(args or "{}")
    return dict(args)


def _walk(interaction, log):
    """Run every function the model asked for; return the results to send back.

    Verified step shapes on google-genai 2.34.0 (5 Nov 2026):
      type="thought"        — its reasoning, no text field exposed
      type="model_output"   — the prose answer lives on interaction.output_text,
                              NOT on the step
      type="function_call"  — .name, .arguments (a dict), .id

    interaction.status is "requires_action" while it is still waiting on you.
    """
    results, seen = [], []
    for step in getattr(interaction, "steps", None) or []:
        kind = getattr(step, "type", None)
        seen.append(kind)
        if kind != "function_call":
            continue
        name = getattr(step, "name", None)
        args = _arguments(step)
        fn = IMPL.get(name)          # each tool traces itself on the way in
        if fn is None:
            out = {"error": f"no such tool: {name}"}
        else:
            try:
                out = fn(**args)
            except Exception as exc:                      # lesson 2, live
                out = {"error": f"{type(exc).__name__}: {exc}"}
        log.append({"call": name, "arguments": args, "result": out})
        results.append({
            "type": "function_result",
            "name": name,
            "call_id": step.id,
            "result": [{"type": "text", "text": json.dumps(out)}],
        })
    if not results and not (getattr(interaction, "output_text", "") or "").strip():
        print(f"{C_WARN}no calls and no text. step types seen: "
              f"{seen or 'NONE'}, status={getattr(interaction, 'status', None)}"
              f"{C_OFF}", flush=True)
    return results


# Lesson 5 again, one layer up: the MODEL is a flaky upstream too. A free-tier
# flash model returns 503 "high demand" often enough that a live demo without
# this will embarrass you on stage. Same fix as the tools — retry here, so
# nothing above this function ever has to reason about HTTP.
FALLBACKS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash"]


def make_client():
    """A client that gives up on a hung request instead of waiting forever.

    Without the timeout an overloaded free-tier model can leave the call
    open for minutes with nothing printed — which looks exactly like your
    own code hanging. Learned the hard way.
    """
    from google import genai
    from google.genai import types

    return genai.Client(http_options=types.HttpOptions(timeout=60_000))


def _create(client, **kw):
    import time

    last = None
    for model in FALLBACKS:
        for attempt in range(2):
            try:
                return client.interactions.create(model=model, **kw), model
            except Exception as exc:
                last = exc
                msg = str(exc)
                retryable = any(s in msg for s in
                                ("503", "429", "high demand", "UNAVAILABLE",
                                 "RESOURCE_EXHAUSTED", "overloaded"))
                if not retryable and "timeout" not in msg.lower():
                    raise
                if attempt < 1:
                    time.sleep(2)
        print(f"  {C_WARN}{model} unavailable — falling back{C_OFF}", flush=True)
    raise last


def converse(client, question, decls, max_turns=8):
    """create → walk → run → send back, until the model stops asking."""
    log = []
    inter, used = _create(client, input=question, tools=decls,
                          system_instruction=SYSTEM)
    if used != FALLBACKS[0]:
        print(f"  {C_WARN}running on {used}{C_OFF}", flush=True)
    answer = ""
    for _ in range(max_turns):
        results = _walk(inter, log)
        if (getattr(inter, "output_text", "") or "").strip():
            answer = inter.output_text
        if not results:
            break
        inter, used = _create(client, input=results,
                              previous_interaction_id=inter.id, tools=decls)
    return answer, log


def run_agent():
    rc = _need_key()
    if rc:
        return rc
    client = make_client()
    decls = declarations()
    print(f"{C_DIM}model {MODEL} · {len(decls)} tools · "
          f"you run every call yourself{C_OFF}")
    print(f"\n> {QUESTION}\n")

    answer, log = converse(client, QUESTION, decls)
    print(f"\n{C_OK}{answer}{C_OFF}\n")
    print(f"{C_DIM}{len(log)} tool calls{C_OFF}")

    out = os.path.join(os.path.dirname(__file__), "out", "agent_transcript.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump({"question": QUESTION, "calls": log, "answer": answer}, f, indent=2)
    print(f"{C_DIM}transcript → {out}{C_OFF}")
    return 0


LESSON1_Q = ("How many confirmed planets does Kepler-90 have, and what are "
             "their orbital periods?")


def lesson1():
    """The slide's claim, run twice. Only the docstring changes."""
    rc = _need_key()
    if rc:
        return rc
    client = make_client()
    runs = {}
    for label, param, desc in [
        ("vague", HOSTNAME_VAGUE, "List the planets around a star."),
        ("fixed", HOSTNAME_FIXED, None),
    ]:
        print(f"\n{C_WARN}── {label} docstring ──{C_OFF}")
        print(f"> {LESSON1_Q}")
        answer, log = converse(client, LESSON1_Q,
                               declarations(hostname_param=param, star_desc=desc))
        print(f"\n{C_OK}{answer}{C_OFF}")
        runs[label] = {"calls": log, "answer": answer}

    print(f"\n{C_DIM}── what changed ──{C_OFF}")
    for label in ("vague", "fixed"):
        for c in runs[label]["calls"]:
            if c["call"] == "planets_of_star":
                found = c["result"].get("found")
                print(f"  {label:<5} hostname={c['arguments'].get('hostname')!r:<12} "
                      f"→ found {found}")

    out = os.path.join(os.path.dirname(__file__), "out", "lesson1.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(runs, f, indent=2)
    print(f"{C_DIM}transcript → {out}{C_OFF}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools-only", action="store_true",
                    help="exercise every tool without calling Gemini")
    ap.add_argument("--lesson1", action="store_true",
                    help="run the same question with a vague and a fixed docstring")
    ap.add_argument("--model", help="pin one model instead of the fallback chain "
                                    "(use when the free tier is congested)")
    a = ap.parse_args()
    if a.model:
        FALLBACKS[:] = [a.model]
        MODEL = a.model
    if a.tools_only:
        sys.exit(tools_only())
    sys.exit(lesson1() if a.lesson1 else run_agent())
