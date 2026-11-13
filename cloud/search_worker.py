"""One Cloud Run Job task = one star.

Cloud Run Jobs sets CLOUD_RUN_TASK_INDEX (0-based) and CLOUD_RUN_TASK_COUNT
on every task. The task picks its own star out of the list and writes one row
per detected signal to BigQuery. Five hundred tasks, five hundred stars, no
coordinator.

Locally:
    CLOUD_RUN_TASK_INDEX=0 python cloud/search_worker.py --dry-run
"""

import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "demo"))

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
DATASET = os.environ.get("BQ_DATASET", "cosmos")
TABLE = os.environ.get("BQ_TABLE", "transit_signals")

# In the real job this comes from a BigQuery table of targets. Kept inline so
# the file runs on a laptop without any cloud set up at all.
TARGETS = [
    "KIC 11442793",  # Kepler-90
    "KIC 11853905",  # Kepler-20
    "KIC 10593626",  # Kepler-22
    "KIC 8478994",   # Kepler-42
    "KIC 6922244",   # Kepler-8
]


def task_slice():
    """Which targets is this task responsible for?"""
    idx = int(os.environ.get("CLOUD_RUN_TASK_INDEX", "0"))
    total = int(os.environ.get("CLOUD_RUN_TASK_COUNT", "1"))
    mine = TARGETS[idx::total]
    print(f"task {idx}/{total} → {len(mine)} target(s): {', '.join(mine)}", flush=True)
    return idx, mine


def search(target: str) -> list[dict]:
    """The same BLS walk as demo/find_planets.py, one star."""
    import warnings
    warnings.filterwarnings("ignore")
    import lightkurve as lk
    import numpy as np

    sr = lk.search_lightcurve(target, author="Kepler", cadence="long")
    if len(sr) == 0:
        return []

    lc = (sr.download_all().stitch()
          .remove_nans()
          # asymmetric on purpose: a deep transit IS a negative outlier
          .remove_outliers(sigma_upper=4, sigma_lower=20)
          .flatten(window_length=901))

    out = []
    for n in range(1, 9):
        if len(lc.flux) < 2000:
            break
        bls = lc.to_periodogram(method="bls", minimum_period=5.0,
                                maximum_period=400.0, frequency_factor=2.0,
                                duration=[0.08, 0.15, 0.25, 0.4])
        power = float(bls.max_power.value)
        if power < 8.0:
            break
        depth = float(bls.depth_at_max_power)
        out.append({
            "target": target,
            "rank": n,
            "period_days": round(float(bls.period_at_max_power.value), 5),
            "depth_ppm": round(depth * 1e6, 1),
            "duration_hours": round(float(bls.duration_at_max_power.value) * 24, 3),
            "power": round(power, 2),
            "radius_earth": round(float(np.sqrt(max(depth, 0)) * 1.2 * 109.2), 3),
            "found_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        })
        lc = lc[~bls.get_transit_mask(period=bls.period_at_max_power,
                                      transit_time=bls.transit_time_at_max_power,
                                      duration=bls.duration_at_max_power)]
    return out


def write(rows: list[dict], dry: bool):
    if not rows:
        print("no signals", flush=True)
        return
    if dry or not PROJECT:
        print(json.dumps(rows, indent=2), flush=True)
        return

    from google.cloud import bigquery

    client = bigquery.Client(project=PROJECT)
    table = f"{PROJECT}.{DATASET}.{TABLE}"
    errs = client.insert_rows_json(table, rows)
    if errs:
        # Fail the task loudly — Cloud Run Jobs will retry it.
        sys.exit(f"BigQuery insert failed: {errs}")
    print(f"wrote {len(rows)} row(s) to {table}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print rows instead of writing to BigQuery")
    args = ap.parse_args()

    _, mine = task_slice()
    allrows = []
    for t in mine:
        try:
            rows = search(t)
            print(f"  {t}: {len(rows)} signal(s)", flush=True)
            allrows += rows
        except Exception as exc:
            # One bad star must not fail the other 499.
            print(f"  {t}: FAILED {type(exc).__name__}: {exc}", flush=True)
    write(allrows, args.dry_run)


if __name__ == "__main__":
    main()
