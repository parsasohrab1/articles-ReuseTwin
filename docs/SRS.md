# Software Requirements Specification (SRS)

| ID | Requirement | Module | Test |
|----|-------------|--------|------|
| FR-1 | Permeability decays with the feed fouling index | `model.py` | `test_no_cleaning_lets_permeability_decay`, `test_fouling_scale_raises_cost` |
| FR-2 | Cleaning restores permeability to the clean level; the clean level falls at each cleaning | `model.py` | `test_cleaning_restores_permeability_and_costs_money`, `test_irreversible_loss_accumulates` |
| FR-3 | The membrane is replaced when the clean level falls below the replacement level | `model.py` | `test_replacement_resets_clean_level` |
| FR-4 | Interval and threshold cleaning policies | `policies.py` | `test_threshold_policy_keeps_k_above_threshold` |
| FR-5 | Grid optimisation of a policy parameter | `policies.py` | `test_optimum_is_interior` |
| FR-6 | Estimate the fouling rate and the days to a threshold from noisy permeability | `estimator.py` | `test_rate_estimator_recovers_known_rate`, `test_days_to_threshold_edge_cases` |

Parameters (all assumed, `model.py`): fouling rate 0.004 per day at index 1, irreversible loss 1.5% per cleaning, energy 1 kWh/m3 at clean state and proportional to 1/permeability, energy price 0.08, cleaning cost 150 plus one day of downtime valued at 0.5 per m3, membrane replacement 25 000 below clean level 0.6, flow 2000 m3/day.
