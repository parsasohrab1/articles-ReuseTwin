"""Cleaning policies and the threshold optimiser."""

from __future__ import annotations

import numpy as np

from .model import Params, feed_index, simulate


def interval_policy(every_days: int):
    return lambda day, k, since: since >= every_days


def threshold_policy(k_threshold: float):
    return lambda day, k, since: k <= k_threshold


def optimise(p: Params, days: int, seeds: int, kind: str, grid: np.ndarray, meas_sd: float = 0.0,
             feed_scale: float = 1.0, seed0: int = 100) -> tuple[float, float]:
    """Pick the grid value with the lowest mean cost over training seeds. Returns (value, cost)."""
    best, best_cost = None, np.inf
    for g in grid:
        pol = interval_policy(int(g)) if kind == "interval" else threshold_policy(float(g))
        costs = []
        for s in range(seeds):
            rng = np.random.default_rng(seed0 + s)
            feed = feed_index(days, rng, p, feed_scale)
            costs.append(simulate(days, pol, p, feed, rng, meas_sd)["cost_per_m3"])
        c = float(np.mean(costs))
        if c < best_cost:
            best, best_cost = float(g), c
    return best, best_cost


def optimise_on_feed(p: Params, feed: np.ndarray, kind: str, grid: np.ndarray,
                     meas_sd: float = 0.0, seed: int = 0) -> tuple[float, float]:
    """Lowest-cost grid value on one feed path. Returns (value, cost per m3)."""
    best, best_cost = None, np.inf
    rng = np.random.default_rng(seed)
    for g in grid:
        pol = interval_policy(int(g)) if kind == "interval" else threshold_policy(float(g))
        cost = simulate(len(feed), pol, p, feed, rng, meas_sd)["cost_per_m3"]
        if cost < best_cost:
            best, best_cost = float(g), float(cost)
    return best, best_cost
