"""Online estimate of the fouling rate and of the days until a permeability threshold."""

from __future__ import annotations

import numpy as np


def fit_rate(k_meas: np.ndarray) -> tuple[float, float]:
    """Least-squares slope of log K on time over the window; returns (rate per day, residual sd)."""
    t = np.arange(len(k_meas))
    y = np.log(k_meas)
    slope, intercept = np.polyfit(t, y, 1)
    resid = y - (slope * t + intercept)
    return float(-slope), float(resid.std(ddof=2)) if len(t) > 2 else 0.0


def days_to_threshold(k_now: float, rate: float, k_threshold: float) -> float:
    if rate <= 0 or k_now <= k_threshold:
        return 0.0 if k_now <= k_threshold else float("inf")
    return float(np.log(k_now / k_threshold) / rate)
