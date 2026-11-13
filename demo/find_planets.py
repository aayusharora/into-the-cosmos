"""Really find the planets around Kepler-90, from real Kepler photometry.

No Gemini, no API key — this is the instrument layer the agent calls. Run it
and you get genuine numbers and genuine plots you can put on a slide.

    python demo/find_planets.py

Writes find_planets.json and two PNGs next to itself.
"""

import argparse
import json
import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")

CACHE = None  # set in main(); a cleaned copy of the curve, so stage runs are fast

TARGET = "KIC 11442793"          # Kepler-90, as MAST knows it
MIN_POWER = 8.0                  # below this a BLS peak isn't worth reporting
MAX_SIGNALS = 8
OUT = os.path.dirname(os.path.abspath(__file__))

# The published answers, used only to score ourselves at the end.
KNOWN = {
    "b": 7.008151, "c": 8.719375, "i": 14.44912, "d": 59.73667,
    "e": 91.93913, "f": 124.91440, "g": 210.73514, "h": 331.60296,
}


def load():
    import lightkurve as lk

    print(f"searching MAST for {TARGET} …", flush=True)
    sr = lk.search_lightcurve(TARGET, author="Kepler", cadence="long")
    print(f"  {len(sr)} quarters found", flush=True)
    if len(sr) == 0:
        sys.exit("no Kepler light curves published for this target")

    print("downloading (this is the slow part) …", flush=True)
    lc = sr.download_all().stitch()
    print(f"  {len(lc.flux)} cadences, "
          f"{float(lc.time.value.max() - lc.time.value.min()):.0f} day baseline",
          flush=True)

    # Clip bright outliers hard, but barely touch dips. The obvious
    # remove_outliers(sigma=6) is symmetric, and a gas giant's transit IS a
    # big negative outlier — the first version of this script threw away the
    # two deepest planets in the system before it started looking.
    lc = lc.remove_nans().remove_outliers(sigma_upper=4, sigma_lower=20)
    lc = lc.flatten(window_length=901)
    print(f"  {len(lc.flux)} cadences after cleaning", flush=True)
    np.savez_compressed(CACHE, time=lc.time.value, flux=np.asarray(lc.flux.value))
    print(f"  cached to {os.path.basename(CACHE)} — next run can use --fast",
          flush=True)
    return lc


def load_cached():
    """Reload the cleaned curve from disk. Seconds, not minutes."""
    import lightkurve as lk

    if not os.path.exists(CACHE):
        sys.exit(f"no cache at {CACHE} — run once without --fast first")
    d = np.load(CACHE)
    print(f"loaded {len(d['flux'])} cleaned cadences from cache", flush=True)
    return lk.LightCurve(time=d["time"], flux=d["flux"])


def search(lc):
    """Walk down from the deepest transit to the faintest, masking as we go."""
    found = []

    for n in range(1, MAX_SIGNALS + 1):
        if len(lc.flux) < 2000:
            print("  too little data left, stopping", flush=True)
            break

        bls = lc.to_periodogram(
            method="bls",
            minimum_period=5.0,
            maximum_period=400.0,
            frequency_factor=1.5,
            # Giants sit in transit for many hours; the default trial
            # durations are too short to catch them cleanly.
            duration=[0.08, 0.15, 0.25, 0.4],
        )
        power = float(bls.max_power.value)
        period = bls.period_at_max_power
        t0 = bls.transit_time_at_max_power
        dur = bls.duration_at_max_power

        if power < MIN_POWER:
            print(f"  round {n}: best peak power {power:.1f} "
                  f"< {MIN_POWER}, stopping", flush=True)
            break

        depth = float(bls.depth_at_max_power)
        sig = {
            "round": n,
            "period_days": round(float(period.value), 5),
            "depth_ppm": round(depth * 1e6, 1),
            "duration_hours": round(float(dur.value) * 24, 3),
            "power": round(power, 1),
            "radius_earth": round(float(np.sqrt(max(depth, 0)) * 1.2 * 109.2), 2),
        }
        found.append(sig)
        print(f"  round {n}: P = {sig['period_days']:>9.5f} d   "
              f"depth {sig['depth_ppm']:>8.1f} ppm   "
              f"power {sig['power']:>6.1f}   "
              f"~{sig['radius_earth']:.2f} R_earth", flush=True)

        mask = bls.get_transit_mask(period=period, transit_time=t0, duration=dur)
        lc = lc[~mask]

    return found, lc


def score(found):
    """Match what we found against the published periods."""
    out, used = [], set()
    for s in found:
        p = s["period_days"]
        best, best_err = None, 1e9
        for name, kp in KNOWN.items():
            if name in used:
                continue
            for mult, label in ((1, ""), (2, " (2x alias)"), (0.5, " (1/2 alias)")):
                err = abs(p - kp * mult) / (kp * mult)
                if err < best_err:
                    best, best_err, best_label = name, err, label
        if best and best_err < 0.02:
            used.add(best)
            out.append({**s, "matches": f"Kepler-90 {best}{best_label}",
                        "period_error_pct": round(best_err * 100, 3)})
        else:
            out.append({**s, "matches": None, "period_error_pct": None})
    return out, sorted(set(KNOWN) - used)


def plots(lc_raw):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    t = lc_raw.time.value
    f = lc_raw.flux.value
    fig, ax = plt.subplots(figsize=(14, 4.2), facecolor="#070C18")
    ax.set_facecolor("#070C18")
    ax.plot(t, f, ".", ms=0.6, color="#5AC8E8", alpha=0.5)
    for s in ("bottom", "left"):
        ax.spines[s].set_color("#3A4A7A")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors="#8D97B8", labelsize=9)
    ax.set_xlabel("time (BKJD)", color="#A8B2CC")
    ax.set_ylabel("normalised flux", color="#A8B2CC")
    fig.tight_layout()
    p = os.path.join(OUT, "kepler90_lightcurve.png")
    fig.savefig(p, dpi=150, facecolor="#070C18")
    print(f"wrote {p}", flush=True)
    return p


def main():
    global CACHE
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true",
                    help="reuse the cached cleaned curve (use this on stage)")
    args = ap.parse_args()
    CACHE = os.path.join(OUT, "lightcurve_cache.npz")

    lc = load_cached() if args.fast else load()
    lc_for_plot = lc.copy()
    found, _ = search(lc)
    scored, missed = score(found)

    print("\n--- scoreboard ---", flush=True)
    hits = [s for s in scored if s["matches"]]
    print(f"signals reported : {len(scored)}")
    print(f"matched a known planet : {len(hits)} of 8")
    for s in scored:
        tag = s["matches"] or "no match in the catalogue"
        print(f"  P={s['period_days']:>9.5f} d  →  {tag}")
    if missed:
        print(f"missed : {', '.join('Kepler-90 ' + m for m in missed)}")

    png = plots(lc_for_plot)
    res = {
        "target": TARGET,
        "signals": scored,
        "matched": len(hits),
        "of_known": len(KNOWN),
        "missed": [f"Kepler-90 {m}" for m in missed],
        "lightcurve_png": os.path.basename(png),
    }
    with open(os.path.join(OUT, "find_planets.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.join(OUT, 'find_planets.json')}", flush=True)


if __name__ == "__main__":
    main()
