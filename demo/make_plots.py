"""Make the two slide images: raw starlight, and the same data folded.

The pair is the whole argument of the talk. On the left, four years of real
Kepler photometry in which four planets are invisible. On the right, the same
points folded at a period the search found — and a planet appears.

Run find_planets.py first; this reads its JSON for the period.
MAST downloads are cached, so this is fast the second time.

    python demo/make_plots.py
"""

import json
import os
import sys
import warnings

import numpy as np

warnings.filterwarnings("ignore")

OUT = os.path.dirname(os.path.abspath(__file__))
TARGET = "KIC 11442793"
BG = "#070C18"
CYAN = "#5AC8E8"
AMBER = "#FFB454"
GREY = "#8D97B8"


CACHE = os.path.join(OUT, "lightcurve_cache.npz")


def load_curve(lk, tries=3):
    """Cached cleaned curve, or fetch it once and cache it.

    MAST drops connections often enough that a single attempt is not a real
    answer — the first version of this function failed with a bare
    RemoteDisconnected. Same lesson as every flaky upstream: retry inside the
    thing that fetches, and keep a local copy.
    """
    import time

    if os.path.exists(CACHE):
        d = np.load(CACHE)
        print(f"using cached curve: {len(d['flux'])} cadences", flush=True)
        return lk.LightCurve(time=d["time"], flux=d["flux"])

    last = None
    for n in range(tries):
        try:
            print(f"downloading from MAST (attempt {n + 1}/{tries}) …", flush=True)
            lc = (lk.search_lightcurve(TARGET, author="Kepler", cadence="long")
                  .download_all().stitch()
                  .remove_nans()
                  .remove_outliers(sigma_upper=4, sigma_lower=20)
                  .flatten(window_length=901))
            np.savez_compressed(CACHE, time=lc.time.value,
                                flux=np.asarray(lc.flux.value))
            print(f"cached {len(lc.flux)} cadences to {os.path.basename(CACHE)}",
                  flush=True)
            return lc
        except Exception as exc:
            last = exc
            print(f"  failed: {type(exc).__name__}: {exc}", flush=True)
            if n < tries - 1:
                time.sleep(5 * (n + 1))
    raise last


def style(ax):
    ax.set_facecolor(BG)
    for s in ("bottom", "left"):
        ax.spines[s].set_color("#3A4A7A")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=GREY, labelsize=11)
    ax.xaxis.label.set_color("#A8B2CC")
    ax.yaxis.label.set_color("#A8B2CC")


def main():
    import lightkurve as lk
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with open(os.path.join(OUT, "find_planets.json")) as fh:
        res = json.load(fh)

    # Fold at the STRONGEST confirmed match, not the shortest period.
    #
    # Tempting logic: a 60-day planet transits 24 times in Kepler's baseline
    # and a 331-day one only 4, so stack the 60-day one. Wrong — this plot is
    # made from the UNMASKED curve, where the 331-day giant is 17x deeper and
    # dominates everything. An epoch probe near 60 days gets pulled onto the
    # giant and the fold comes out flat. Fold what the data actually contains.
    hits = [s for s in res["signals"] if s.get("matches")]
    hit = max(hits, key=lambda s: s["power"]) if hits else res["signals"][0]
    period = hit["period_days"]
    label = hit.get("matches") or "strongest signal"
    print(f"folding at {period} d  ({label})", flush=True)

    lc = load_curve(lk)

    # ---- 1. raw: the planets are in here and you cannot see them ----
    fig, ax = plt.subplots(figsize=(13, 4.0), facecolor=BG)
    style(ax)
    ax.plot(lc.time.value, lc.flux.value, ".", ms=0.7, color=CYAN, alpha=0.45)
    ax.set_xlabel("time (days)")
    ax.set_ylabel("brightness")
    fig.tight_layout()
    p1 = os.path.join(OUT, "slide_raw.png")
    fig.savefig(p1, dpi=160, facecolor=BG)
    plt.close(fig)
    print(f"wrote {p1}", flush=True)

    # ---- 2. folded: the same points, stacked on the period ----
    # Folding needs a mid-transit time as well as a period. Without one,
    # phase 0 is just t=0 and the dip lands at some arbitrary phase — which
    # is exactly how the first version of this plot came out flat.
    probe = lc.to_periodogram(
        method="bls",
        period=np.linspace(period * 0.999, period * 1.001, 400),
        duration=[0.08, 0.15, 0.25],
    )
    t0 = probe.transit_time_at_max_power
    print(f"mid-transit at BKJD {float(t0.value):.4f}", flush=True)

    folded = lc.fold(period=period, epoch_time=t0)
    t = folded.time.value
    f = folded.flux.value

    # Bin INSIDE the plotted window, not across the whole 60-day fold.
    # Binning the full range at 220 bins gives ~9 bins across +/-1.2 days,
    # which smears a five-hour transit into a single point — that is exactly
    # how the second version of this plot came out flat.
    span = 1.2
    win = np.abs(t) <= span
    t, f = t[win], f[win]

    # Bin count has to follow the data. A 60-day period puts ~2,200 points in
    # this window; a 331-day one puts ~370. Fixing nbins at 120 leaves the
    # long-period case with 3 points per bin and the whole plot empty.
    nbins = int(max(24, min(140, win.sum() // 12)))
    edges = np.linspace(-span, span, nbins + 1)
    idx = np.digitize(t, edges) - 1
    bx, by = [], []
    for i in range(nbins):
        m = idx == i
        if m.sum() >= 3:
            bx.append(0.5 * (edges[i] + edges[i + 1]))
            by.append(np.median(f[m]))
    bx, by = np.array(bx), np.array(by)
    if len(bx) == 0:
        sys.exit("no populated bins — widen the window or lower the threshold")
    print(f"{len(bx)} bins from {win.sum()} points "
          f"(~{win.sum() // max(nbins, 1)} per bin)", flush=True)

    fig, ax = plt.subplots(figsize=(13, 4.6), facecolor=BG)
    style(ax)
    ax.plot(t, f, ".", ms=0.6, color="#2A4A6E", alpha=0.30)
    ax.plot(bx, by, "-", lw=2.6, color=CYAN)
    ax.plot(bx, by, ".", ms=7, color=AMBER)
    ax.set_xlim(-span, span)
    lo = float(np.nanmin(by)) if len(by) else 0.999
    ax.set_ylim(lo - 0.00035, 1.00025)
    ax.axhline(1.0, color="#3A4A7A", lw=1.2, ls="--")
    ax.set_xlabel(f"days from mid-transit  (folded at {period:.3f} d)")
    ax.set_ylabel("brightness")
    fig.tight_layout()
    p2 = os.path.join(OUT, "slide_folded.png")
    fig.savefig(p2, dpi=160, facecolor=BG)
    plt.close(fig)
    print(f"wrote {p2}", flush=True)

    depth_ppm = (1.0 - float(np.nanmin(by))) * 1e6
    print(f"folded depth ≈ {depth_ppm:.0f} ppm  "
          f"= {depth_ppm/1e4:.3f}% of the star's light", flush=True)


if __name__ == "__main__":
    main()
