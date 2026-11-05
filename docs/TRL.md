# Technology readiness (evidence-based)

**Level: TRL 4 on a synthetic fouling twin.** TRL 5 is not claimed.

## Evidence
9 unit tests pass. `research/run_study.py` (policies tuned on 20 training years at fouling scale 1.0; 100 test years per row; permeability measurement noise 3% for the "noisy" policy):

| Test fouling | Policy | Cost per m3 | Cleanings per year | Minimum permeability |
|---|---|---|---|---|
| x1.0 | Interval, tuned (80 days) | 0.1035 | 4.0 | 0.67 |
| x1.0 | Threshold on true K (0.74) | 0.1035 | 4.9 | 0.74 |
| x1.0 | Threshold on noisy K (0.70) | 0.1037 | 4.5 | 0.71 |
| x1.0 | Interval 30 days (calendar practice) | 0.1151 | 12.0 | 0.74 |
| x1.5 | Interval, tuned | 0.1118 | 4.0 | 0.56 |
| x1.5 | Threshold on true K | 0.1118 | 8.6 | 0.74 |
| x1.5 | Threshold on noisy K | 0.1104 | 7.3 | 0.70 |
| x0.6 | Interval, tuned | 0.0976 | 4.0 | 0.78 |
| x0.6 | Threshold on true K | 0.0983 | 2.6 | 0.74 |

A well-tuned fixed interval costs as much as a condition-based rule when tuned for the right fouling level. Condition-based rules do not save cost here; they keep permeability above a floor when fouling rises (minimum 0.70 to 0.74 against 0.56 for the interval) and adapt the number of cleanings. A calendar of 30 days costs about 11% more than the tuned rules in the base case.

## Not shown
A synthetic twin whose model form and parameters are assumptions; cost differences between the tuned rules are small and depend on the assumed prices. No plant data.

## Next steps toward TRL 5
Daily permeability, pressure and feed data from one RO plant (or a public pilot-plant dataset), fit of the fouling rate to it, and replay of the cleaning decisions on held-out months.
