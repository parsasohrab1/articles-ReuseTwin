"""Reverse-osmosis membrane fouling twin (daily steps; synthetic parameters).

State: normalised permeability K (1 = clean new membrane). Fouling: dK/dt = -kf * F(t) * K, where
F(t) is a feed fouling index (lognormal AR(1)). A cleaning (CIP) restores K to the current
"clean level", which itself falls by `irreversible` at each cleaning. Pump energy per m3 is
proportional to 1/K (more pressure is needed to hold the flux).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Params:
    kf: float = 0.004                # fouling rate per day at F = 1
    irreversible: float = 0.015      # loss of clean level per cleaning
    energy_kwh_per_m3: float = 1.0   # at K = 1
    energy_price: float = 0.08       # currency per kWh
    cip_cost: float = 150.0          # chemicals and labour per cleaning
    cip_days: float = 1.0            # downtime per cleaning
    water_value: float = 0.5         # currency per m3 not produced during downtime
    flow_m3_per_day: float = 2000.0
    feed_ar1: float = 0.9
    feed_sd: float = 0.35
    replace_level: float = 0.6       # membrane is replaced when the clean level reaches this
    replace_cost: float = 25000.0    # membrane replacement (elements and labour)


def feed_index(days: int, rng: np.random.Generator, p: Params, scale: float = 1.0) -> np.ndarray:
    z, out = 0.0, np.empty(days)
    for i in range(days):
        z = p.feed_ar1 * z + np.sqrt(1 - p.feed_ar1**2) * rng.normal()
        out[i] = scale * np.exp(p.feed_sd * z - 0.5 * p.feed_sd**2)
    return out


def simulate(days: int, policy, p: Params, feed: np.ndarray, rng: np.random.Generator,
             meas_sd: float = 0.0) -> dict:
    """`policy(day, k_measured, days_since_cip) -> bool` decides a cleaning at the end of a day."""
    k, clean_level, since, n_cip = 1.0, 1.0, 0, 0
    energy_kwh, down_days, n_repl = 0.0, 0.0, 0
    ks = np.empty(days)
    for d in range(days):
        ks[d] = k
        energy_kwh += p.energy_kwh_per_m3 / k * p.flow_m3_per_day
        k *= float(np.exp(-p.kf * feed[d]))
        since += 1
        k_meas = k * float(np.exp(rng.normal(0.0, meas_sd))) if meas_sd else k
        if policy(d, k_meas, since):
            n_cip += 1
            down_days += p.cip_days
            clean_level *= 1.0 - p.irreversible
            if clean_level < p.replace_level:
                n_repl += 1
                clean_level = 1.0
            k = clean_level
            since = 0
    produced = max((days - down_days) * p.flow_m3_per_day, 1.0)
    cost = (energy_kwh * p.energy_price + n_cip * p.cip_cost + n_repl * p.replace_cost
            + down_days * p.flow_m3_per_day * p.water_value)
    return {"cost_per_m3": cost / produced, "replacements": n_repl, "cleanings": n_cip, "min_k": float(ks.min()),
            "mean_k": float(ks.mean()), "final_clean_level": clean_level,
            "energy_kwh_per_m3": energy_kwh / produced, "k_series": ks}
