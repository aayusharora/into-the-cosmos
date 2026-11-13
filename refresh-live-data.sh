#!/usr/bin/env bash
# Re-fetch every live number in the deck. Run this the MORNING of the talk.
#
#   ./refresh-live-data.sh
#
# Then paste the values into the slides it names. Nothing here needs an API key.

set -uo pipefail

AU=149597870.7
LD=384400.0

say() { printf '\n\033[1;33m%s\033[0m\n' "$1"; }
tap() {
  curl -sS --max-time 120 -G "https://exoplanetarchive.ipac.caltech.edu/TAP/sync" \
    --data-urlencode "query=$1" --data-urlencode "format=csv"
}

say "1. EXOPLANET TOTALS   → slides: d6-planet, scale"
echo "confirmed:   $(tap 'select count(*) from pscomppars' | tail -1)"
echo "by Kepler:   $(tap "select count(*) from pscomppars where disc_facility='Kepler'" | tail -1)"
echo "by transit:  $(tap "select count(*) from pscomppars where discoverymethod='Transit'" | tail -1)"
echo "   → d6-planet reads: \"N of M known planets were found exactly this way\""

say "2. KEPLER-90 SYSTEM   → slide: scale  (hostname is KOI-351, not Kepler-90)"
tap "select pl_name,pl_orbper,pl_rade,pl_orbsmax from pscomppars where hostname='KOI-351' order by pl_orbsmax"
echo "   → scale reads: outermost at 0.97 AU vs Earth at 1.00"

say "3. CLOSEST ASTEROID, next 7 days   → slide: d4-asteroid"
curl -sS --max-time 60 \
  "https://ssd-api.jpl.nasa.gov/cad.api?date-min=now&date-max=%2B7&dist-max=0.05&sort=dist" \
| python3 -c "
import sys, json, math
AU=$AU; LD=$LD
d=json.load(sys.stdin)
if not d.get('data'):
    print('  nothing inside 0.05 AU this week — widen dist-max'); raise SystemExit
f=d['fields']; r=d['data'][0]; g=dict(zip(f,r))
km=float(g['dist'])*AU
print(f\"  object:    {g['des']}\")
print(f\"  closest:   {g['cd']} UTC\")
print(f\"  distance:  {km:,.0f} km   =  {km/LD:.1f}x the Moon   ({float(g['dist']):.4f} AU)\")
print(f\"  speed:     {float(g['v_rel']):.2f} km/s  =  {float(g['v_rel'])*3600:,.0f} km/h\")
H=float(g['h'])
lo=1329/math.sqrt(0.25)*10**(-H/5)*1000
hi=1329/math.sqrt(0.05)*10**(-H/5)*1000
print(f\"  size:      roughly {lo:.0f}-{hi:.0f} m across (H={H}, albedo 0.25-0.05)\")
print(f\"  → update the green line AND the orange bar on the diagram if the\")
print(f\"     lunar-distance multiple changed much\")
"

say "4. LATEST EARTH IMAGE   → slide: d3-earth"
curl -sS --max-time 60 "https://epic.gsfc.nasa.gov/api/natural" \
| python3 -c "
import sys, json
d=json.load(sys.stdin)
if not d: print('  no frames returned'); raise SystemExit
f=d[-1]; c=f['centroid_coordinates']
ns='N' if c['lat']>=0 else 'S'; ew='E' if c['lon']>=0 else 'W'
print(f\"  identifier: {f['image']}\")
print(f\"  taken:      {f['date']} UTC\")
print(f\"  centred:    {abs(c['lat']):.1f}°{ns} {abs(c['lon']):.1f}°{ew}\")
print(f\"  png:        https://epic.gsfc.nasa.gov/archive/natural/\"
      + f['date'][:10].replace('-','/') + f\"/png/{f['image']}.png\")
print('  → download that PNG and show the REAL image in your recording')
"

say "5. SOLAR FLARES, last 2 weeks   → slide: d5-storm"
echo "   DONKI is frequently slow or down — if this hangs, Ctrl-C and present"
echo "   d5-storm's chart as illustrative. It is the only slide whose numbers"
echo "   are not live."
curl -sS --max-time 30 \
  "https://api.nasa.gov/DONKI/FLR?startDate=$(date -u -v-14d +%Y-%m-%d 2>/dev/null || date -u -d '14 days ago' +%Y-%m-%d)&endDate=$(date -u +%Y-%m-%d)&api_key=DEMO_KEY" \
| python3 -c "
import sys, json
try: d=json.load(sys.stdin)
except Exception: print('  DONKI returned nothing usable'); raise SystemExit
print(f'  flares: {len(d)}')
for x in d[-6:]:
    print(f\"    {x.get('beginTime')}  class {x.get('classType')}  region {x.get('activeRegionNum')}\")
cls=[x.get('classType','') for x in d if x.get('classType')]
big=[c for c in cls if c.startswith('X')] or [c for c in cls if c.startswith('M')]
if big: print(f'  strongest: {sorted(big)[-1]}  → name this one on the slide')
" 2>/dev/null || echo "  (skipped — DONKI unreachable)"

say "DONE"
cat <<'EOF'
Checklist before you present:
  [ ] d6-planet  — transit-method count updated
  [ ] scale      — Kepler-90 figures still match
  [ ] d4-asteroid— object, date, distance, lunar multiple, speed, size
  [ ] d3-earth   — identifier, date, centre; real PNG downloaded
  [ ] d5-storm   — strongest flare class, or say the chart is illustrative
  [ ] FACTS.md   — update the dated header
EOF
