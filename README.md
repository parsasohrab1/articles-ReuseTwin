# articles-ReuseTwin

Reverse-osmosis fouling digital twin and cleaning-schedule optimisation for industrial water reuse.
Product for the water special issue "AI in Water and Wastewater Treatment" (Water, MDPI).

**Maturity: TRL 4 on a synthetic twin** ([docs/TRL.md](docs/TRL.md)). No plant data yet.

- `src/reusetwin/model.py` fouling twin: permeability decay, cleaning, irreversible loss, replacement, energy and cost
- `src/reusetwin/policies.py` interval and threshold cleaning policies, grid optimiser
- `src/reusetwin/estimator.py` online fouling-rate fit and days-to-threshold
- `research/run_study.py` study; `tests/` 9 tests; docs: [BRS](docs/BRS.md) · [SRS](docs/SRS.md) · [TRL](docs/TRL.md)

```bash
pip install -e ".[dev]" && python -m pytest -q && python research/run_study.py
```
