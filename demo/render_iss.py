#!/usr/bin/env python3
"""Where the ISS actually is, from a two-line element set and eight lines of maths.

    .venv/bin/python demo/render_iss.py

Needs the venv: sgp4 is not in the system Python.

Fetches the current TLE from Celestrak, propagates one full orbit, and
draws the ground track over a NASA Blue Marble basemap. Then it works out
when the station next comes over Siliguri, which is the line that makes a
room look up.

Writes demo/img/iss_track.webp and prints the numbers for the slide.
Keyless, both ends.
"""
import argparse
import datetime as dt
import math
import os
import sys
import urllib.request

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt            # noqa: E402
import numpy as np                         # noqa: E402
from PIL import Image                      # noqa: E402
from sgp4.api import Satrec, jday          # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "img")
CACHE = os.path.join(OUT, "iss")
SILIGURI = (26.73, 88.40)

TLE_URL = "https://celestrak.org/NORAD/elements/gp.php?CATNR=25544&FORMAT=TLE"
# One WMS request for the whole world, rather than a tile grid. GIBS's
# EPSG:4326 tile matrix is not the power-of-two layout you would expect
# (level 2 is 5x3, not 8x4) and getting it wrong just returns 400s.
GIBS = ("https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi"
        "?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0"
        "&LAYERS=BlueMarble_ShadedRelief_Bathymetry&CRS=EPSG:4326"
        "&BBOX=-90,-180,90,180&WIDTH=2048&HEIGHT=1024"
        "&FORMAT=image/jpeg&TIME=2004-01-01")

INK, DIM, AMBER, GREEN = "#F2F4FA", "#8D97B8", "#FFB454", "#7CE0A8"
MONO = "DejaVu Sans Mono"
R_E = 6378.137


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "into-the-cosmos talk demo"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# ------------------------------------------------------------------ basemap
def basemap():
    """Blue Marble from NASA GIBS, 2048x1024. Cached after the first run."""
    path = os.path.join(CACHE, "bluemarble_z2.png")
    if not os.path.exists(path):
        os.makedirs(CACHE, exist_ok=True)
        open(path, "wb").write(get(GIBS, 90))
    return Image.open(path)


# -------------------------------------------------------------------- orbit
def gmst(jd):
    """Greenwich mean sidereal time, radians."""
    d = jd - 2451545.0
    return math.radians((280.46061837 + 360.98564736629 * d) % 360.0)


def ground_point(sat, when):
    """Sub-satellite latitude, longitude and altitude for a UTC instant."""
    jd, fr = jday(when.year, when.month, when.day,
                  when.hour, when.minute, when.second + when.microsecond / 1e6)
    e, r, v = sat.sgp4(jd, fr)
    if e:
        return None
    th = gmst(jd + fr)
    x = r[0] * math.cos(th) + r[1] * math.sin(th)
    y = -r[0] * math.sin(th) + r[1] * math.cos(th)
    z = r[2]
    lon = math.degrees(math.atan2(y, x))
    lat = math.degrees(math.atan2(z, math.hypot(x, y)))
    alt = math.sqrt(x * x + y * y + z * z) - R_E
    speed = math.sqrt(sum(c * c for c in v)) * 3600
    return lat, lon, alt, speed, (x, y, z)


def elevation(ecef, lat, lon):
    """Elevation of a satellite above an observer's horizon, degrees."""
    la, lo = math.radians(lat), math.radians(lon)
    ox = R_E * math.cos(la) * math.cos(lo)
    oy = R_E * math.cos(la) * math.sin(lo)
    oz = R_E * math.sin(la)
    dx, dy, dz = ecef[0] - ox, ecef[1] - oy, ecef[2] - oz
    rng = math.sqrt(dx * dx + dy * dy + dz * dz)
    up = (dx * ox + dy * oy + dz * oz) / (R_E * rng)
    return math.degrees(math.asin(max(-1, min(1, up))))


def next_pass(sat, start, lat, lon, hours=24, step=20, floor=10.0):
    """When the station next clears `floor` degrees over a place."""
    best, cur = None, None
    for i in range(int(hours * 3600 / step)):
        t = start + dt.timedelta(seconds=i * step)
        g = ground_point(sat, t)
        if not g:
            continue
        el = elevation(g[4], lat, lon)
        if el >= floor:
            if cur is None or el > cur[1]:
                cur = (t, el)
        elif cur is not None:
            best = cur
            break
    return best or cur


# ------------------------------------------------------------------- render
def render(frames=96, orbit_min=93.0):
    os.makedirs(CACHE, exist_ok=True)
    tle = get(TLE_URL).decode().strip().splitlines()
    name, l1, l2 = (x.strip() for x in tle[:3])
    sat = Satrec.twoline2rv(l1, l2)
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)

    # one orbit of ground track, plus the tail before "now"
    span = np.linspace(-orbit_min, orbit_min * 0.15, 420)
    pts = []
    for m in span:
        g = ground_point(sat, now + dt.timedelta(minutes=float(m)))
        if g:
            pts.append((m, g[0], g[1], g[2], g[3]))

    bm = basemap().convert("RGB")
    arr = (np.asarray(bm).astype(float) * 0.42).astype(np.uint8)   # darken

    imgs = []
    for k in range(frames):
        t_now = -orbit_min + (orbit_min * 1.15) * k / (frames - 1)
        fig = plt.figure(figsize=(15.4, 8.3), dpi=100, facecolor="#05080F")
        ax = fig.add_axes([0.0, 0.0, 1.0, 0.93])
        ax.imshow(arr, extent=[-180, 180, -90, 90], aspect="auto")

        # split the track at the dateline so it does not draw across the map
        seg, segs = [], []
        for m, la, lo, _, _ in pts:
            if seg and abs(lo - seg[-1][1]) > 180:
                segs.append(seg); seg = []
            seg.append((la, lo, m))
        segs.append(seg)
        for s in segs:
            past = [(la, lo) for la, lo, m in s if m <= t_now]
            fut = [(la, lo) for la, lo, m in s if m > t_now]
            if len(fut) > 1:
                ax.plot([p[1] for p in fut], [p[0] for p in fut],
                        color="#3A4A7A", lw=1.6, ls=(0, (4, 4)), zorder=3)
            if len(past) > 1:
                ax.plot([p[1] for p in past], [p[0] for p in past],
                        color=AMBER, lw=2.6, alpha=0.95, zorder=4)

        cur = min(pts, key=lambda p: abs(p[0] - t_now))
        ax.plot([cur[2]], [cur[1]], "o", ms=22, color=AMBER, alpha=0.25, zorder=5)
        ax.plot([cur[2]], [cur[1]], "o", ms=11, color="#FFF3DC", zorder=6)
        ax.plot([SILIGURI[1]], [SILIGURI[0]], "o", ms=15, mfc="none",
                mec=GREEN, mew=2.5, zorder=6)
        ax.annotate(" Siliguri", SILIGURI[::-1], color=GREEN, fontsize=17,
                    fontfamily=MONO, zorder=6)

        ax.set_xlim(-180, 180); ax.set_ylim(-90, 90)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#1B2540")

        when = now + dt.timedelta(minutes=float(cur[0]))
        ns = "N" if cur[1] >= 0 else "S"
        ew = "E" if cur[2] >= 0 else "W"
        fig.text(0.012, 0.955, f"{when:%H:%M:%S} UTC", color=INK,
                 fontsize=26, fontfamily=MONO)
        fig.text(0.30, 0.955, f"{abs(cur[1]):5.1f}°{ns}  {abs(cur[2]):6.1f}°{ew}",
                 color=DIM, fontsize=26, fontfamily=MONO)
        fig.text(0.625, 0.955, f"{cur[3]:.0f} km", color=DIM, fontsize=26, fontfamily=MONO)
        fig.text(0.80, 0.955, f"{cur[4]:,.0f} km/h", color=AMBER,
                 fontsize=26, fontfamily=MONO)

        fig.canvas.draw()
        imgs.append(Image.frombytes("RGBA", fig.canvas.get_width_height(),
                                    fig.canvas.buffer_rgba()).convert("RGB"))
        plt.close(fig)

    path = os.path.join(OUT, "iss_track.webp")
    imgs[0].save(path, "WEBP", save_all=True, append_images=imgs[1:],
                 duration=85, loop=0, quality=76, method=4)

    g = ground_point(sat, now)
    nxt = next_pass(sat, now, *SILIGURI)
    return path, name, l1, l2, now, g, nxt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", type=int, default=96)
    a = ap.parse_args()
    path, name, l1, l2, now, g, nxt = render(a.frames)

    print(f"\n  {path}  ({os.path.getsize(path)/1e6:.2f} MB)\n")
    print("=" * 62)
    print("FOR THE SLIDE")
    print("=" * 62)
    print(f"\n  satellite      {name}")
    print(f"  TLE epoch      {l1[18:32].strip()}  (fetched {now:%d %b %Y %H:%M} UTC)")
    print(f"  right now      {abs(g[0]):.1f}°{'N' if g[0]>=0 else 'S'}  "
          f"{abs(g[1]):.1f}°{'E' if g[1]>=0 else 'W'}")
    print(f"  altitude       {g[2]:.0f} km")
    print(f"  speed          {g[3]:,.0f} km/h")
    print(f"  orbit          92.9 minutes")
    if nxt:
        t, el = nxt
        ist = t + dt.timedelta(hours=5, minutes=30)
        print(f"\n  next pass over Siliguri   {ist:%H:%M} IST on {ist:%d %b}, "
              f"{el:.0f}° above the horizon")
    print()


if __name__ == "__main__":
    main()
