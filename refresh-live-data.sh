#!/usr/bin/env bash
# Run this the MORNING of the talk.
#
#   ./refresh-live-data.sh
#
# Redraws the three recorded demos from live data and prints every number
# in the deck that depends on them, with the slide each one sits on. Then
# it runs the tool check. Nothing here needs an API key.
#
# The previous version of this script named slides that no longer exist
# (d4-asteroid, d5-storm, scale). It was from the exoplanet version of the
# talk. demo/render_night.py replaced it.

set -uo pipefail
cd "$(dirname "$0")"

say() { printf '\n\033[1;33m%s\033[0m\n' "$1"; }

say "1. RE-RENDER THE THREE CHARTS"
python3 demo/render_night.py "$@" || {
  echo "  render failed. The slides still hold the previous night."
  exit 1
}

say "2. RE-RENDER THE ISS GROUND TRACK"
# needs the venv: sgp4 is not in the system Python. A TLE goes stale in
# days, and the slide claims a pass time for tonight, so this is not
# optional.
if [ -x .venv/bin/python ]; then
  .venv/bin/python demo/render_iss.py || echo "  ISS render failed. Slide 64 still shows the previous orbit."
else
  echo "  no .venv. Run: python3 -m venv .venv &&"
  echo "    .venv/bin/pip install --only-binary=:all: sgp4 matplotlib pillow"
fi

say "3. CHECK EVERY TOOL STILL WORKS"
python3 demo/tonight.py --tools-only
TOOLS=$?

say "4. REBUILD THE DECK AND THE GUIDE"
python3 build-dist.py && python3 build-guide.py

say "DONE"
cat <<'EOF'
Then:
  [ ] paste the numbers above into the slides they name
  [ ] update the dated header in FACTS.md
  [ ] copy dist/index.html and dist/img/ to the repo root and push
  [ ] open the deck and look at slides 11, 14, 17 and 64 before you trust them
  [ ] slide 64 names a pass time for tonight. Check it re-rendered.
EOF
exit $TOOLS
