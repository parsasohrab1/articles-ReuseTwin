"""Cleaning-schedule study on a synthetic RO fouling twin (not plant data).

Usage: python research/run_study.py --out research/results.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from reusetwin.model import Params, feed_index, simulate
from reusetwin.policies import interval_policy, optimise, threshold_policy

DAYS, MEAS_SD = 365, 0.03


def evaluate(policy, scale, meas_sd, seeds=100, p=None):
    p = p or Params()
    rows = []
    for s in range(seeds):
        rng = np.random.default_rng(5000 + s)
        feed = feed_index(DAYS, rng, p, scale)
        r = simulate(DAYS, policy, p, feed, rng, meas_sd)
        rows.append((r["cost_per_m3"], r["cleanings"], r["min_k"]))
    a = np.array(rows)
    return {"cost_per_m3": float(a[:, 0].mean()), "cleanings": float(a[:, 1].mean()),
            "min_k": float(a[:, 2].mean())}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="research/results.json")
    a = ap.parse_args()
    p = Params()
    iv, _ = optimise(p, DAYS, 20, "interval", np.arange(10, 130, 10))
    th, _ = optimise(p, DAYS, 20, "threshold", np.arange(0.5, 0.99, 0.04))
    thn, _ = optimise(p, DAYS, 20, "threshold", np.arange(0.5, 0.99, 0.04), meas_sd=MEAS_SD)
    out = {"note": "synthetic RO twin; policies tuned at fouling scale 1.0 on 20 training years",
           "tuned": {"interval_days": iv, "threshold_true_k": th, "threshold_noisy_k": thn}}
    for scale in (1.0, 1.5, 0.6):
        out[f"fouling_x{scale}"] = {
            "interval_tuned": evaluate(interval_policy(int(iv)), scale, 0.0),
            "threshold_true_k": evaluate(threshold_policy(th), scale, 0.0),
            "threshold_noisy_k": evaluate(threshold_policy(thn), scale, MEAS_SD),
            "interval_30d_practice": evaluate(interval_policy(30), scale, 0.0)}
    Path(a.out).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
