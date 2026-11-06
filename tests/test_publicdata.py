import json
from pathlib import Path

import numpy as np
import pytest

from reusetwin.estimator import fit_rate
from reusetwin.publicdata import (
    build_real_report,
    permeability_proxy,
    segment_table,
    split_cutoff,
)

ROOT = Path(__file__).resolve().parents[1]


def test_fit_rate_uses_the_time_axis_not_the_sample_index():
    t = np.arange(0, 40, 2)
    k = np.exp(-0.01 * t)
    rate, sd = fit_rate(k, t)
    assert rate == pytest.approx(0.01, rel=1e-6)
    assert sd < 1e-9


def test_permeability_proxy_falls_when_pressure_deviation_rises():
    assert permeability_proxy(0.0, 0.0) == 1.0
    assert permeability_proxy(0.0, 0.25) == pytest.approx(0.8)


def test_segments_respect_the_time_cutoff():
    days = np.arange(0, 241)
    k = np.exp(-0.001 * days)
    rows = segment_table(days, k, np.array([80, 160]), cutoff=100)
    by_role = {row["role"]: row for row in rows if row["eligible"]}
    assert by_role["train"]["rate_per_day"] == pytest.approx(0.001, rel=1e-3)
    assert "test" in by_role
    assert any(row["role"] == "crossed" for row in rows)


def test_split_cutoff_is_eighty_percent_of_the_span():
    assert split_cutoff(6, 106) == pytest.approx(86)


def _same_report(saved, fresh, path=""):
    """Floats may differ in the last bits across BLAS/NumPy builds. Decisions may not."""
    if isinstance(saved, dict):
        assert set(saved) == set(fresh), path
        for key in saved:
            _same_report(saved[key], fresh[key], f"{path}.{key}")
        return
    if isinstance(saved, list):
        assert len(saved) == len(fresh), path
        for i, item in enumerate(saved):
            _same_report(item, fresh[i], f"{path}[{i}]")
        return
    if isinstance(saved, float):
        assert fresh == pytest.approx(saved, rel=1e-9, abs=1e-12), path
        return
    assert saved == fresh, path


def test_results_json_matches_a_fresh_real_run():
    fresh = json.loads(json.dumps(build_real_report(ROOT)))
    saved = json.loads((ROOT / "research" / "results.json").read_text(encoding="utf-8"))
    _same_report(saved["real"], fresh)
    text = (ROOT / "docs" / "TRL.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    kf = f"{fresh['fit']['kf_per_day']:.6g}"
    mae = f"{fresh['holdout_prediction']['mae_k']:.6g}"
    assert kf in text and kf in readme
    assert mae in text and mae in readme
    scenario = fresh["schedule_scenario"]
    for horizon in ("tuning", "year", "holdout"):
        for metrics in scenario[horizon]["policies"].values():
            assert f"{metrics['cost_per_m3']:.6g}" in text
            assert f"{metrics['min_k']:.6g}" in text
    assert fresh["dataset"]["license"] == "CC-BY-4.0"
    nrel = fresh["screened_out"]["nrel_wave_ro_steady_state"]
    assert nrel["used_for_fit"] is False
    assert nrel["runtime_minutes_max"] < 24 * 60
    assert nrel["has_cleaning_column"] is False
