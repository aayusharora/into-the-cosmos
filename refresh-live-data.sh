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

say "2. CHECK EVERY TOOL STILL WORKS"
python3 demo/tonight.py --tools-only
TOOLS=$?

say "3. REBUILD THE DECK AND THE GUIDE"
python3 build-dist.py && python3 build-guide.py

say "DONE"
cat <<'EOF'
Then:
  [ ] paste the numbers above into the slides they name
  [ ] update the dated header in FACTS.md
  [ ] copy dist/index.html and dist/img/ to the repo root and push
  [ ] open the deck and look at slides 11, 14 and 17 before you trust them
EOF
exit $TOOLS
