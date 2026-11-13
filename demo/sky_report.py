"""The thing you containerise in step 8.

Gathers tonight's sky from keyless NASA endpoints, then — if GEMINI_API_KEY is
set — asks Gemini to turn it into a short report in the voice your GEMINI.md
asks for. Without a key it prints the raw findings, so the data half is
testable on its own.

    python demo/sky_report.py            # report (or raw, if no key)
    python demo/sky_report.py --raw      # never call Gemini

Deployed: Cloud Run runs this, Cloud Scheduler pokes it each morning.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import (  # noqa: E402  — the verified, keyless tools
    closest_approach_this_week,
    exoplanet_count,
    latest_earth_image,
)

MODEL = "gemini-3.8-flash"

CONTEXT = """I'm in Delhi, 28.6N 77.2E.
Binoculars only - 10x50. No telescope.
Always give altitude and compass direction.
Never recommend anything below 20 degrees above the horizon.
Metric. No emoji."""


def gather() -> dict:
    """Everything tonight's report is built from. No model involved."""
    out = {}
    for name, fn in (("asteroid", closest_approach_this_week),
                     ("earth", latest_earth_image)):
        try:
            out[name] = fn()
        except Exception as exc:
            out[name] = {"error": f"{type(exc).__name__}: {exc}"}
    try:
        out["exoplanets"] = exoplanet_count()
    except Exception as exc:
        out["exoplanets"] = {"error": f"{type(exc).__name__}: {exc}"}
    return out


def narrate(facts: dict) -> str:
    from google import genai

    client = genai.Client()
    resp = client.models.generate_content(
        model=MODEL,
        contents=(
            f"Standing facts about me:\n{CONTEXT}\n\n"
            f"Today's data:\n{json.dumps(facts, indent=2)}\n\n"
            "Write me a short morning sky report — six sentences at most. "
            "Lead with whether tonight is worth going outside for. Use only "
            "the data above; if something is missing, say so rather than "
            "filling it in."
        ),
    )
    return resp.text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", action="store_true", help="skip Gemini entirely")
    args = ap.parse_args()

    facts = gather()

    if args.raw or not os.environ.get("GEMINI_API_KEY"):
        if not args.raw:
            print("(GEMINI_API_KEY not set — printing raw findings)\n")
        print(json.dumps(facts, indent=2))
        return 0

    print(narrate(facts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
