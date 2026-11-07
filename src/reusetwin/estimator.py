"""Online estimate of the fouling rate and of the days until a permeability threshold."""

from __future__ import annotations

import numpy as np


def fit_rate(k_meas: np.ndarray, t: np.ndarray | None = None) -> tuple[float, float]:
    """Least-squares slope of log K on time. Returns (rate per unit of t, residual sd).

    `t` defaults to 0, 1, ..., n-1. Pass the real day index when samples are not daily.
    """
    k_meas = np.asarray(k_meas, dtype=float)
    if t is None:
        t = np.arange(len(k_meas), dtype=float)
    else:
        t = np.asarray(t, dtype=float)
    if len(k_meas) != len(t):
        raise ValueError("k_meas and t must have the same length")
    y = np.log(k_meas)
    slope, intercept = np.polyfit(t, y, 1)
    resid = y - (slope * t + intercept)
    return float(-slope), float(resid.std(ddof=2)) if len(t) > 2 else 0.0


def days_to_threshold(k_now: float, rate: float, k_threshold: float) -> float:
    if rate <= 0 or k_now <= k_threshold:
        return 0.0 if k_now <= k_threshold else float("inf")
    return float(np.log(k_now / k_threshold) / rate)
