# articles-ReuseTwin

Reverse-osmosis fouling digital twin and cleaning-schedule comparison for industrial water reuse.
Product for the water special issue "AI in Water and Wastewater Treatment" (Water, MDPI).

**Maturity: TRL 4.** A public seawater-RO series was fitted. It does not confirm the fouling equation on later windows, and the scenario costs do not show a saving for cleaning under the assumed prices. See [docs/TRL.md](docs/TRL.md) and [data/DATA_LICENSE.md](data/DATA_LICENSE.md).

## Public series (Su 2026, CC-BY-4.0)

Derived daily indicators and a CIP ledger, https://doi.org/10.5281/zenodo.21055948. Permeability proxy `(1 + flux_pct) / (1 + ndp_pct)` on the `n3` basis. Deviations in the deposit are non-negative, so the proxy is biased high. No plant prices are in the deposit. Cleaning chemistry is not in this repository.

Time-ordered 80% cutoff at day 618 (days 6 to 771). Median training rate `kf` = 0.000146867 per day (6 of 9 eligible segments positive; median residual sd 0.0534777). All 4 held-out segments have a rising proxy. Hold-out mean absolute error of terminal proxy K is 0.0546853, and the decay forecast sits below the observed end point (mean error -0.0516526).

Scenario costs use `Params` prices, a feed index of 1, and irreversible loss 0 (that loss is not identified here). Rules are tuned on the 612-day training span. On that span a 310-day interval costs 0.0828942 per m3 against 0.0836993 for never cleaning. On a 365-day replay the same rules do not beat never cleaning (0.0821771): the 0.94 threshold never fires, one clean at 310 days costs 0.0834172, the plant's 40-day median costs 0.0967915, and a 30-day calendar costs 0.102441. On the 153-day hold-out window the tuned rules do not fire, and both fixed calendars cost more than not cleaning (30-day 0.102302, 40-day 0.0933251, never 0.0808997). These are scenario costs, not plant invoices, and the hold-out permeability path does not support the decay rate.

NREL's steady-state wave-RO file (CC-BY-4.0, MHKDR 649) is 6005 rows over 5.0 minutes and has no cleaning column, so it is not fitted. The EPA malathion workbook is public domain and is a pre/post snapshot, not a daily series. Two Harvard CIP/fouling sets are CC BY-NC-ND and are not redistributed.

## Code

- `src/reusetwin/model.py` fouling twin: permeability decay, cleaning, irreversible loss, replacement, energy and cost
- `src/reusetwin/policies.py` interval and threshold cleaning policies, grid optimiser
- `src/reusetwin/estimator.py` fouling-rate fit and days-to-threshold
- `src/reusetwin/publicdata.py` public-series proxy, segment fit, and scenario comparison
- `research/run_study.py` writes `research/results.json`; docs: [BRS](docs/BRS.md) · [SRS](docs/SRS.md) · [TRL](docs/TRL.md)

```bash
pip install -e ".[dev]" && python -m pytest -q && python research/run_study.py
```
