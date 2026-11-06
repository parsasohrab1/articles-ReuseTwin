"""Fit the existing fouling equation to a public SWRO indicator series.

The permeability proxy is specific flux over net driving pressure, built from the
deposited fractional deviations. It is not a plant-measured normalised permeability.
Cleaning chemistry is not modelled.
"""

from __future__ import annotations

import csv
from itertools import pairwise
from pathlib import Path

import numpy as np

from .estimator import fit_rate
from .model import Params, simulate
from .policies import interval_policy, optimise_on_feed, threshold_policy

MIN_POINTS = 8
MIN_SPAN_DAYS = 21.0
TRAIN_FRACTION = 0.8

NOT_USED = (
    {
        "name": "EPA membrane malathion workbook",
        "doi": "10.23719/1529271",
        "license": "US public domain (17 USC 105)",
        "url": "https://doi.org/10.23719/1529271",
        "used_for_fit": False,
        "reason": "pre-cleaning and post-cleaning snapshots, not a daily permeability series",
    },
    {
        "name": "Orange County RO membrane fouling data",
        "doi": "10.7910/DVN/PVY3QD",
        "license": "CC BY-NC-ND 4.0",
        "url": "https://doi.org/10.7910/DVN/PVY3QD",
        "used_for_fit": False,
        "reason": "non-commercial no-derivatives license; not redistributed and not fitted",
    },
    {
        "name": "Hazen RO facility CIP data",
        "doi": "10.7910/DVN/VURALX",
        "license": "CC BY-NC-ND 4.0",
        "url": "https://doi.org/10.7910/DVN/VURALX",
        "used_for_fit": False,
        "reason": "non-commercial no-derivatives license; not redistributed and not fitted",
    },
)


def permeability_proxy(flux_pct: float, ndp_pct: float) -> float:
    """Specific-flux proxy. Both inputs are fractional deviations from one baseline."""
    return (1.0 + flux_pct) / (1.0 + ndp_pct)


def split_cutoff(day_min: float, day_max: float, train_fraction: float = TRAIN_FRACTION) -> float:
    if not 0.0 < train_fraction < 1.0:
        raise ValueError("train_fraction must be between 0 and 1")
    return float(day_min + train_fraction * (day_max - day_min))


def _role(left: float, right: float, t_start: float, t_end: float, cutoff: float) -> str:
    if np.isfinite(right) and right <= cutoff:
        return "train"
    if np.isfinite(left) and left >= cutoff:
        return "test"
    if not np.isfinite(right) and t_end <= cutoff:
        return "train"
    if not np.isfinite(left) and t_start > cutoff:
        return "test"
    return "crossed"


def segment_table(days: np.ndarray, k: np.ndarray, cip_days: np.ndarray, cutoff: float,
                  min_points: int = MIN_POINTS, min_span: float = MIN_SPAN_DAYS) -> list[dict]:
    """Inter-cleaning windows. A window that contains the cutoff is `crossed` and unused."""
    days = np.asarray(days, dtype=float)
    k = np.asarray(k, dtype=float)
    cips = np.asarray(sorted(float(c) for c in cip_days), dtype=float)
    bounds = np.concatenate(([-np.inf], cips, [np.inf]))
    rows = []
    for left, right in pairwise(bounds):
        mask = (days > left) & (days < right) & np.isfinite(k) & (k > 0)
        if int(mask.sum()) == 0:
            continue
        t = days[mask]
        kk = k[mask]
        order = np.argsort(t)
        t, kk = t[order], kk[order]
        span = float(t[-1] - t[0])
        eligible = bool(len(t) >= min_points and span >= min_span)
        rate, resid = (None, None)
        if eligible:
            rate, resid = fit_rate(kk, t)
        rows.append({
            "role": _role(float(left), float(right), float(t[0]), float(t[-1]), cutoff),
            "t_start": float(t[0]),
            "t_end": float(t[-1]),
            "n": len(t),
            "span_days": span,
            "eligible": eligible,
            "rate_per_day": rate,
            "resid_sd": resid,
            "k_start": float(kk[0]),
            "k_end": float(kk[-1]),
        })
    return rows


def _load_series(indicator_csv: Path) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    buckets: dict[tuple[str, int], list[float]] = {}
    with indicator_csv.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["basis"] != "n3" or row["flux_pct"] == "" or row["ndp_pct"] == "":
                continue
            key = (row["train"], int(row["day_index"]))
            buckets.setdefault(key, []).append(
                permeability_proxy(float(row["flux_pct"]), float(row["ndp_pct"])))
    by_train: dict[str, list[tuple[int, float]]] = {}
    for (train, day), values in buckets.items():
        by_train.setdefault(train, []).append((day, float(np.median(values))))
    out = {}
    for train, pairs in by_train.items():
        pairs.sort()
        out[train] = (np.array([d for d, _ in pairs], dtype=float),
                      np.array([v for _, v in pairs], dtype=float))
    return out


def _load_cips(ledger_csv: Path) -> dict[str, np.ndarray]:
    by_train: dict[str, list[float]] = {}
    with ledger_csv.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            by_train.setdefault(row["train"], []).append(float(row["day_index"]))
    return {train: np.array(sorted(days), dtype=float) for train, days in by_train.items()}


def screen_nrel_steady_state(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or [])
        runtime = [float(row["Runtime (min)"]) for row in reader]
    rt = np.asarray(runtime, dtype=float)
    cleaning = any("clean" in name.lower() or name.lower() == "cip" for name in fields)
    return {
        "citation": "Sitterley, Binger, and Jenne, NREL, MHKDR submission 649",
        "url": "https://mhkdr.openei.org/submissions/649",
        "license": "CC-BY-4.0",
        "n_rows": int(rt.size),
        "runtime_minutes_max": float(rt.max()) if rt.size else None,
        "has_cleaning_column": cleaning,
        "used_for_fit": False,
        "reason": "steady-state transport test lasting minutes, with no cleaning events",
    }


def _policy_metrics(policy, days: int, p: Params) -> dict:
    rng = np.random.default_rng(0)
    result = simulate(days, policy, p, np.ones(days), rng, 0.0)
    return {"cost_per_m3": result["cost_per_m3"], "cleanings": int(result["cleanings"]),
            "min_k": result["min_k"]}


def _at_edge(value: float, grid: np.ndarray) -> bool:
    return bool(np.isclose(value, grid[0]) or np.isclose(value, grid[-1]))


def _holdout_errors(segments: list[dict], kf: float) -> dict:
    errors = []
    rates = []
    for seg in segments:
        if seg["role"] != "test" or not seg["eligible"]:
            continue
        dt = seg["t_end"] - seg["t_start"]
        predicted = seg["k_start"] * float(np.exp(-kf * dt))
        errors.append(predicted - seg["k_end"])
        rates.append(seg["rate_per_day"])
    if not errors:
        return {"n": 0, "mae_k": None, "mean_error_k": None, "test_rates_per_day": []}
    err = np.asarray(errors, dtype=float)
    return {"n": int(err.size), "mae_k": float(np.mean(np.abs(err))),
            "mean_error_k": float(err.mean()), "test_rates_per_day": [float(r) for r in rates]}


def build_real_report(root: Path) -> dict:
    """Fit, hold out later windows, and compare cleaning rules on the fitted rate."""
    root = Path(root)
    series = _load_series(root / "data" / "swro_su2026" / "derived_daily_indicator_table.csv")
    cips = _load_cips(root / "data" / "swro_su2026" / "cip_campaign_ledger.csv")
    all_days = np.concatenate([days for days, _ in series.values()])
    day_min, day_max = float(all_days.min()), float(all_days.max())
    cutoff = split_cutoff(day_min, day_max)

    segments: list[dict] = []
    gaps: list[float] = []
    for train in sorted(series):
        days, k = series[train]
        train_cips = cips.get(train, np.array([], dtype=float))
        for seg in segment_table(days, k, train_cips, cutoff):
            seg["train"] = train
            segments.append(seg)
        ordered = np.sort(train_cips)
        for earlier, later in pairwise(ordered):
            if later <= cutoff:
                gaps.append(float(later - earlier))

    train_segs = [s for s in segments if s["role"] == "train" and s["eligible"]]
    if not train_segs:
        raise RuntimeError("no eligible training segments")
    train_rates = [float(s["rate_per_day"]) for s in train_segs]
    kf = float(np.median(train_rates))
    plant_median = float(np.median(gaps)) if gaps else None

    schedule = None
    if kf > 0 and plant_median is not None:
        tune_days = max(30, int(np.floor(cutoff - day_min)))
        holdout_days = max(1, int(np.floor(day_max - cutoff)))
        p = Params(kf=kf, irreversible=0.0)
        interval_grid = np.arange(10, min(tune_days, 400) + 1, 10, dtype=float)
        threshold_grid = np.array([round(0.70 + 0.02 * i, 2) for i in range(15)])
        interval, _ = optimise_on_feed(p, np.ones(tune_days), "interval", interval_grid)
        threshold, _ = optimise_on_feed(p, np.ones(tune_days), "threshold", threshold_grid)
        every = max(1, round(plant_median))
        frozen = {
            "never": lambda d, k, s: False,
            "interval_30d": interval_policy(30),
            "interval_plant_median": interval_policy(every),
            "interval_tuned": interval_policy(int(interval)),
            "threshold_tuned": threshold_policy(threshold),
        }

        def evaluate(days: int) -> dict:
            return {name: _policy_metrics(policy, days, p) for name, policy in frozen.items()}

        schedule = {
            "cost_basis": "assumed Params prices; feed index fixed at 1; not plant invoices",
            "irreversible_used": 0.0,
            "irreversible_identified": False,
            "tuned_on_days": tune_days,
            "plant_median_interval_days": plant_median,
            "plant_median_interval_rounded": every,
            "interval_days_tuned": interval,
            "interval_at_grid_edge": _at_edge(interval, interval_grid),
            "threshold_k_tuned": threshold,
            "threshold_at_grid_edge": _at_edge(threshold, threshold_grid),
            "tuning": {"horizon_days": tune_days, "policies": evaluate(tune_days)},
            "holdout": {"horizon_days": holdout_days, "policies": evaluate(holdout_days)},
            "year": {"horizon_days": 365, "policies": evaluate(365)},
        }

    n_by_role = {role: sum(1 for s in segments if s["role"] == role and s["eligible"])
                 for role in ("train", "test", "crossed")}
    return {
        "dataset": {
            "name": "Su 2026 de-identified SWRO daily indicators and CIP ledger",
            "doi": "10.5281/zenodo.21055948",
            "license": "CC-BY-4.0",
            "citation": "Su, Yi Hsiang (2026). Zenodo. https://doi.org/10.5281/zenodo.21055948",
            "proxy": (
                "(1 + flux_pct) / (1 + ndp_pct) on the n3 basis. "
                "Non-negative deviations bias this proxy high."
            ),
        },
        "screened_out": {
            "nrel_wave_ro_steady_state": screen_nrel_steady_state(
                root / "data" / "nrel_wave_ro" / "steady_state.csv"),
            "others": list(NOT_USED),
        },
        "split": {
            "rule": (
                "eligible inter-CIP segments wholly before the 80% day cutoff are train; "
                "wholly after are test; segments that contain the cutoff are unused"
            ),
            "day_min": day_min,
            "day_max": day_max,
            "cutoff": cutoff,
            "n_eligible": n_by_role,
        },
        "fit": {
            "kf_per_day": kf,
            "train_rates_per_day": train_rates,
            "fraction_train_rates_positive": float(np.mean(np.asarray(train_rates) > 0)),
            "median_residual_sd": float(np.median([s["resid_sd"] for s in train_segs])),
            "feed_index_assumed": 1.0,
        },
        "holdout_prediction": _holdout_errors(segments, kf),
        "schedule_scenario": schedule,
    }
