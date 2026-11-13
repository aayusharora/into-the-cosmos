#!/usr/bin/env python3
"""Re-render the three recorded demos for a given night, from live data.

    python demo/render_night.py                 # tonight
    python demo/render_night.py --date 2026-12-06

Writes into demo/img/:

    siliguri_cloud.webp   animated cloud cover over north-east India
    siliguri_sky.webp     animated sky, dusk to dawn, with the planets
    moon_tonight.png      the Moon's altitude and the dark window

and then prints every number in the deck that depends on them, with the
slide each one sits on. Nothing here needs an API key.

Run this the MORNING of the talk. The sky on the slides is not the sky
outside unless you do.
"""
import argparse
import datetime
import json
import math
import os
import sys
import urllib.parse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402
from PIL import Image                    # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tonight as T                      # noqa: E402  the same tools the agent uses

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
LAT, LON = T.SILIGURI
PLACE = "Siliguri"

# the deck's palette, so a re-render drops straight back into the slides
INK, GRID, DIM = "#F2F4FA", "#1B2540", "#8D97B8"
AMBER, GREEN, PAPER = "#FFB454", "#7CE0A8", "#05080F"
MONO = "DejaVu Sans Mono"

PLANETS = [("Venus", "299"), ("Mars", "499"), ("Jupiter", "599"), ("Saturn", "699")]


# ------------------------------------------------------------------ helpers
def ist_minutes(utc):
    """Horizons UTC stamp -> minutes past midnight IST, unwrapped past 24h."""
    return int(utc[-5:-3]) * 60 + int(utc[-2:]) + 330


def hhmm(mins):
    h, m = divmod(int(round(mins)) % 1440, 60)
    return f"{h:02d}:{m:02d}"


def night_window(day):
    return f"{day} 12:00", f"{day + datetime.timedelta(days=1)} 01:30"


def track(body, day):
    """Altitude/azimuth/magnitude for one body across the night."""
    start, stop = night_window(day)
    rows = T._horizons(body, LAT, LON, start, stop)
    mins = [ist_minutes(r["utc"]) for r in rows]
    # unwrap past midnight so the x axis runs forwards
    for i in range(1, len(mins)):
        while mins[i] < mins[i - 1]:
            mins[i] += 1440
    return mins, rows


def figure(w=1180, h=620):
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100, facecolor=PAPER)
    ax = fig.add_axes([0.07, 0.11, 0.90, 0.80])
    ax.set_facecolor(PAPER)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.tick_params(colors=DIM, labelsize=15)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontfamily(MONO)
    return fig, ax


def save_gif_as_webp(frames, path, ms):
    frames[0].save(path, "WEBP", save_all=True, append_images=frames[1:],
                   duration=ms, loop=0, quality=80, method=4)
    return path


def fig_to_image(fig):
    fig.canvas.draw()
    return Image.frombytes("RGBA", fig.canvas.get_width_height(),
                           fig.canvas.buffer_rgba()).convert("RGB")


# -------------------------------------------------------------- 1. the Moon
def render_moon(day):
    mins, rows = track("301", day)
    alt = [r["el"] for r in rows]
    mag = rows[0]["mag"]

    fig, ax = figure(1180, 460)
    ax.axhline(0, color="#3A4A7A", lw=1.4)

    # find the horizon crossing first, and interpolate it, so the dark band
    # starts where the Moon actually goes down and not at the next 30-minute
    # sample
    cross, word = None, None
    for i in range(len(alt) - 1):
        if (alt[i] > 0) != (alt[i + 1] > 0):
            f = -alt[i] / (alt[i + 1] - alt[i])
            cross = mins[i] + 30 * f
            word = "Moonset" if alt[i] > 0 else "Moonrise"
            break

    lo, hi = min(mins), max(mins)
    if cross is None:
        dark = (lo, hi) if alt[0] <= 0 else None
    else:
        dark = (cross, hi) if alt[0] > 0 else (lo, cross)

    ax.fill_between(mins, -40, 0, color="#0B1020", zorder=0)
    if dark:
        ax.axvspan(dark[0], dark[1], color="#0B1A10", zorder=0)
        if dark[1] - dark[0] > 90:
            ax.text((dark[0] + dark[1]) / 2, 46, "DARK", color=GREEN,
                    fontsize=30, fontfamily=MONO, ha="center", zorder=5)

    # Blank the part of the curve that falls off the axes. NaN rather than
    # dropping the points: dropping them joins the two neighbours and draws
    # a flat line along the bottom that was never in the data.
    curve = np.where(np.array(alt) > -38, np.array(alt), np.nan)
    ax.plot(mins, curve, color="#EDE7D8", lw=2.6, zorder=4)

    if cross is not None:
        ax.plot([cross], [0], "o", ms=11, color="#EDE7D8", zorder=5)
        ax.annotate(f"{word} {hhmm(cross)}", (cross, 0),
                    xytext=(12, 12), textcoords="offset points",
                    color="#EDE7D8", fontsize=20, fontfamily=MONO, zorder=5)

    ax.set_xlim(min(mins), max(mins))
    ax.set_ylim(-40, 70)
    ticks = [t for t in range(min(mins) // 60 * 60, max(mins) + 1, 120)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([hhmm(t) for t in ticks])
    ax.set_yticks([-30, 0, 30, 60])
    ax.set_yticklabels(["-30°", "0°", "30°", "60°"])
    ax.text(0.985, 0.94, f"{PLACE} · {day:%d %b %Y}", transform=ax.transAxes,
            ha="right", color=DIM, fontsize=17, fontfamily=MONO)

    path = os.path.join(OUT, "moon_tonight.png")
    fig.savefig(path, facecolor=PAPER)
    plt.close(fig)
    return path, mag, cross, alt[0] > 0


# --------------------------------------------------------------- 2. the sky
def render_sky(day, frames=100):
    data = {}
    for name, code in PLANETS:
        mins, rows = track(code, day)
        data[name] = (mins, [r["el"] for r in rows], [r["az"] for r in rows],
                      [r["mag"] for r in rows])

    lo = max(min(v[0]) for v in data.values())
    hi = min(max(v[0]) for v in data.values())
    clock = np.linspace(lo, hi, frames)

    imgs = []
    for now in clock:
        fig, ax = figure(1180, 560)
        ax.axhline(0, color="#3A4A7A", lw=1.4)
        here = []
        for name, (mins, el, az, mg) in data.items():
            m = np.array(mins); e = np.array(el); a = np.array(az)
            seen = m <= now
            vis = seen & (e > 0)
            ax.plot(a[vis], e[vis], color="#3C4C7A", lw=1.8, zorder=2)
            if seen.any() and e[seen][-1] > 0:
                here.append((float(a[seen][-1]), float(e[seen][-1]), name))

        # Saturn and Jupiter sit on top of each other for part of the night,
        # and so did their labels. Stack them instead.
        here.sort(key=lambda p: -p[1])
        used = []
        for x, y, name in here:
            dy = 0
            while any(abs(x - ux) < 70 and abs((y + dy) - uy) < 8 for ux, uy in used):
                dy += 8          # stack upward: downward runs off the axis
            used.append((x, y + dy))
            ax.plot([x], [y], "o", ms=13, color=AMBER, zorder=5)
            ax.annotate(f" {name}", (x, y), xytext=(10, dy * 5.5),
                        textcoords="offset points",
                        color=INK, fontsize=21, fontfamily=MONO, zorder=5)
        ax.set_xlim(0, 360)
        ax.set_ylim(0, 90)
        ax.set_xticks([0, 90, 180, 270, 360])
        ax.set_xticklabels(["N", "E", "S", "W", "N"])
        ax.set_yticks([0, 30, 60, 90])
        ax.set_yticklabels(["0°", "30°", "60°", "90°"])
        ax.text(0.015, 0.92, f"{hhmm(now)}  IST", transform=ax.transAxes,
                color=INK, fontsize=27, fontfamily=MONO)
        ax.text(0.985, 0.92, f"{PLACE} · {day:%d %b %Y}", transform=ax.transAxes,
                ha="right", color=DIM, fontsize=17, fontfamily=MONO)
        imgs.append(fig_to_image(fig))
        plt.close(fig)

    path = save_gif_as_webp(imgs, os.path.join(OUT, "siliguri_sky.webp"), 90)

    # The slide wants the best thing to look at THIS EVENING. Taking the
    # highest altitude across the whole window picks something at 6am,
    # which is true and useless.
    best = {}
    for name, (mins, el, az, mg) in data.items():
        evening = [(e, m, g) for e, m, g in zip(el, mins, mg)
                   if 1080 <= m <= 1439 and e > 10]
        if evening:
            e, m, g = max(evening)
            best[name] = (round(e, 1), hhmm(m), g)
    return path, best


# ------------------------------------------------------------- 3. the cloud
def cloud_grid(day, nx=18, ny=13):
    """Hourly cloud cover on a grid over north-east India."""
    lons = np.linspace(85.5, 92.5, nx)
    lats = np.linspace(24.0, 29.0, ny)
    pts = [(la, lo) for la in lats for lo in lons]
    grid, times = {}, None
    for i in range(0, len(pts), 100):
        chunk = pts[i:i + 100]
        q = urllib.parse.urlencode({
            "latitude": ",".join(f"{a:.3f}" for a, _ in chunk),
            "longitude": ",".join(f"{b:.3f}" for _, b in chunk),
            "hourly": "cloud_cover", "timezone": "auto",
            "start_date": str(day), "end_date": str(day + datetime.timedelta(days=1))})
        d = json.loads(T._get("https://api.open-meteo.com/v1/forecast?" + q, 90))
        if isinstance(d, dict):
            d = [d]
        for (la, lo), rec in zip(chunk, d):
            times = rec["hourly"]["time"]
            grid[(la, lo)] = rec["hourly"]["cloud_cover"]
    return lats, lons, times, grid


def render_cloud(day, frames=42):
    lats, lons, times, grid = cloud_grid(day)
    want = [i for i, s in enumerate(times)
            if s[:10] == str(day) and 17 <= int(s[11:13]) <= 23]
    cube = np.array([[[grid[(la, lo)][i] or 0 for lo in lons] for la in lats]
                     for i in want], dtype=float)

    # ease between the hourly frames so it drifts instead of stepping
    steps = np.linspace(0, len(cube) - 1, frames)
    imgs = []
    for s in steps:
        i = int(np.floor(s)); f = s - i
        fr = cube[i] if i + 1 >= len(cube) else cube[i] * (1 - f) + cube[i + 1] * f
        fig = plt.figure(figsize=(11.8, 6.2), dpi=100, facecolor=PAPER)
        ax = fig.add_axes([0.04, 0.07, 0.92, 0.86])
        ax.set_facecolor("#060B16")
        ax.imshow(fr, origin="lower", extent=[lons[0], lons[-1], lats[0], lats[-1]],
                  cmap="Blues_r", vmin=0, vmax=100, alpha=0.92,
                  interpolation="bicubic", aspect="auto")
        ax.plot([LON], [LAT], "o", ms=17, mfc="none", mec=AMBER, mew=3, zorder=5)
        ax.annotate(f"  {PLACE}", (LON, LAT), color=AMBER, fontsize=21,
                    fontfamily=MONO, zorder=5)
        for nm, y, x in [("BHUTAN", 27.4, 90.4), ("BANGLADESH", 24.6, 90.0),
                         ("NEPAL", 27.8, 86.3)]:
            ax.text(x, y, nm, color="#55618A", fontsize=15, fontfamily=MONO,
                    ha="center", zorder=4)
        at = times[want[min(int(round(s)), len(want) - 1)]]
        ax.text(0.015, 0.93, f"{at[11:16]}  IST", transform=ax.transAxes,
                color=INK, fontsize=27, fontfamily=MONO)
        ax.text(0.985, 0.93, "cloud cover · open-meteo", transform=ax.transAxes,
                ha="right", color=DIM, fontsize=17, fontfamily=MONO)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color(GRID)
        imgs.append(fig_to_image(fig))
        plt.close(fig)

    return save_gif_as_webp(imgs, os.path.join(OUT, "siliguri_cloud.webp"), 110)


# ------------------------------------------------------------------- report
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD, default tonight")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    day = (datetime.date.fromisoformat(a.date) if a.date else datetime.date.today())
    os.makedirs(a.out, exist_ok=True)

    print(f"\nRendering the night of {day:%d %B %Y} over {PLACE}\n")

    cloud_path = render_cloud(day)
    print(f"  cloud  {cloud_path}")
    sky_path, best = render_sky(day)
    print(f"  sky    {sky_path}")
    moon_path, mag, cross, up_at_dusk = render_moon(day)
    print(f"  moon   {moon_path}")

    # The numbers on the slides come from the tools the agent calls, not
    # from the map grid. The grid's nearest node is 20 km away and can be
    # a different world: on 13 Nov it sat at 100% in the hills while
    # Siliguri on the plain was at 15%.
    kp = T.space_weather()
    evening = T.sky_conditions()["evening"]
    avg = round(sum(evening.values()) / len(evening))
    top = max(best.items(), key=lambda kv: kv[1][0]) if best else None

    print("\n" + "=" * 64)
    print("PASTE THESE INTO THE SLIDES")
    print("=" * 64)
    print(f"\n  11  cloud-tonight    {avg}% cloud, all evening")
    print(f"      hourly           {json.dumps(evening)}")
    if top:
        n, (el, at, mg) = top
        print(f"\n  14  sky-tonight      {n}, {el:.0f}° up at {at}")
        print(f"      magnitude        {mg}")
    if up_at_dusk and cross:
        print(f"\n  17  moon-tonight     Moon sets {hhmm(cross)}, dark after that")
    elif cross:
        print(f"\n  17  moon-tonight     dark until the Moon rises at {hhmm(cross)}")
    else:
        print("\n  17  moon-tonight     the Moon is up all night")
    print(f"      magnitude        {mag}")
    print(f"\n  31  the-answer       cloud {avg}%  ·  "
          f"{(top[0] + ' ' + str(round(top[1][0]))) if top else 'no planets'}°  ·  "
          f"Kp {kp.get('kp_index')}")
    print(f"\n  30  real-transcript  run: python demo/tonight.py --tools-only")
    print(f"\n  FACTS.md           change the dated header to {day:%d %b %Y}\n")


if __name__ == "__main__":
    main()
