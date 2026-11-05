import numpy as np
import pytest

from reusetwin.estimator import days_to_threshold, fit_rate
from reusetwin.model import Params, feed_index, simulate
from reusetwin.policies import interval_policy, optimise, threshold_policy


def run(policy, seed=0, days=365, scale=1.0, meas_sd=0.0):
    p = Params()
    rng = np.random.default_rng(seed)
    return simulate(days, policy, p, feed_index(days, rng, p, scale), rng, meas_sd)


def test_no_cleaning_lets_permeability_decay():
    r = run(lambda d, k, s: False)
    assert r["min_k"] < 0.4 and r["cleanings"] == 0


def test_cleaning_restores_permeability_and_costs_money():
    never, often = run(lambda d, k, s: False), run(interval_policy(30))
    assert often["min_k"] > never["min_k"] and often["cleanings"] == 365 // 30


def test_irreversible_loss_accumulates():
    r = run(interval_policy(40))                       # 9 cleanings, no replacement
    assert r["replacements"] == 0
    assert r["final_clean_level"] == pytest.approx((1 - Params().irreversible) ** r["cleanings"])


def test_replacement_resets_clean_level():
    r = run(interval_policy(2), days=730)
    assert r["replacements"] >= 1 and r["final_clean_level"] > Params().replace_level


def test_threshold_policy_keeps_k_above_threshold():
    r = run(threshold_policy(0.8))
    assert r["min_k"] > 0.75


def test_fouling_scale_raises_cost():
    assert run(threshold_policy(0.8), scale=2.0)["cost_per_m3"] > \
        run(threshold_policy(0.8), scale=1.0)["cost_per_m3"]


def test_optimum_is_interior():
    thr, _ = optimise(Params(), 365, 4, "threshold", np.array([0.5, 0.7, 0.8, 0.9, 0.97]))
    assert 0.5 < thr < 0.97


def test_rate_estimator_recovers_known_rate():
    t = np.arange(30)
    k = np.exp(-0.01 * t)
    rate, sd = fit_rate(k)
    assert rate == pytest.approx(0.01, rel=1e-6) and sd < 1e-9
    assert days_to_threshold(k[-1], rate, 0.5) == pytest.approx(np.log(k[-1] / 0.5) / 0.01)


def test_days_to_threshold_edge_cases():
    assert days_to_threshold(0.4, 0.01, 0.5) == 0.0
    assert days_to_threshold(0.9, 0.0, 0.5) == float("inf")
