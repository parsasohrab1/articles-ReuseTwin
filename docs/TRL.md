# Technology readiness (evidence-based)

**Level: TRL 4.** TRL 5 is not claimed. A public seawater-RO indicator series was fitted and held out. The exponential fouling equation does not describe the later windows.

## Public series

Su, Yi Hsiang (2026), CC-BY-4.0, https://doi.org/10.5281/zenodo.21055948. Proxy K = (1 + flux_pct) / (1 + ndp_pct) on the n3 rows. The deposited deviations are non-negative, so K is biased high when a true deviation was negative. Licenses for sets that were not fitted are in [DATA_LICENSE.md](../data/DATA_LICENSE.md).

Split: eligible inter-CIP segments wholly before day 618 are train (9), wholly after are test (4), and 3 segments that contain the cutoff are unused. Days run from 6 to 771.

| Quantity | Value |
|---|---|
| Median training rate kf (per day) | 0.000146867 |
| Training segments with a positive rate | 6 of 9 (fraction 0.666667) |
| Median residual sd of log K | 0.0534777 |
| Held-out segments | 4, every rate negative |
| Held-out MAE of terminal K | 0.0546853 |
| Held-out mean error (predicted minus observed) | -0.0516526 |

The forecast decay is larger than the later windows, which rose. Irreversible loss per cleaning is not identified and is set to 0 in the scenario below. The feed index is fixed at 1 because the table has no separate fouling index. The same counts, written by the study script:

<!-- results:start -->
Days 6 to 771. Cutoff 618.
Eligible segments: train 9, test 4, crossed 3.
Median training rate 0.000146867 per day. Positive training segments 6 of 9 (0.666667). Median residual sd 0.0534777.
Held-out segments 4. Negative held-out rates 4 of 4. MAE of terminal K 0.0546853. Mean error, predicted minus observed, -0.0516526.
Tuned interval 310 days. Tuned threshold 0.94. Plant median interval 40 days. Irreversible loss used 0. Identified: False.
tuning 612 days, never: cost 0.0836993, cleanings 0, min K 0.914173.
tuning 612 days, interval_30d: cost 0.102303, cleanings 20, min K 0.99575.
tuning 612 days, interval_plant_median: cost 0.0966893, cleanings 15, min K 0.994289.
tuning 612 days, interval_tuned: cost 0.0828942, cleanings 1, min K 0.955633.
tuning 612 days, threshold_tuned: cost 0.0831645, cleanings 1, min K 0.940042.
year 365 days, never: cost 0.0821771, cleanings 0, min K 0.947944.
year 365 days, interval_30d: cost 0.102441, cleanings 12, min K 0.99575.
year 365 days, interval_plant_median: cost 0.0967915, cleanings 9, min K 0.994289.
year 365 days, interval_tuned: cost 0.0834172, cleanings 1, min K 0.955633.
year 365 days, threshold_tuned: cost 0.0821771, cleanings 0, min K 0.947944.
holdout 153 days, never: cost 0.0808997, cleanings 0, min K 0.977924.
holdout 153 days, interval_30d: cost 0.102302, cleanings 5, min K 0.99575.
holdout 153 days, interval_plant_median: cost 0.0933251, cleanings 3, min K 0.994289.
holdout 153 days, interval_tuned: cost 0.0808997, cleanings 0, min K 0.977924.
holdout 153 days, threshold_tuned: cost 0.0808997, cleanings 0, min K 0.977924.
NREL steady state: 6005 rows, runtime max 5 minutes, cleaning column False, used for fit False.
<!-- results:end -->

Scenario under the assumed `Params` prices (not plant invoices). Policies are chosen on the 612-day training span, then frozen.

| Horizon | Policy | Cost per m3 | Cleanings | Minimum K |
|---|---|---|---|---|
| 612 days (tuning) | Never | 0.0836993 | 0 | 0.914173 |
| 612 days (tuning) | Interval tuned (310 days) | 0.0828942 | 1 | 0.955633 |
| 612 days (tuning) | Threshold tuned (0.94) | 0.0831645 | 1 | 0.940042 |
| 612 days (tuning) | Plant median interval (40 days) | 0.0966893 | 15 | 0.994289 |
| 612 days (tuning) | Interval 30 days | 0.102303 | 20 | 0.995750 |
| 365 days | Never | 0.0821771 | 0 | 0.947944 |
| 365 days | Threshold tuned (0.94) | 0.0821771 | 0 | 0.947944 |
| 365 days | Interval tuned (310 days) | 0.0834172 | 1 | 0.955633 |
| 365 days | Plant median interval (40 days) | 0.0967915 | 9 | 0.994289 |
| 365 days | Interval 30 days | 0.102441 | 12 | 0.995750 |
| 153 days (hold-out length) | Never, and both tuned rules | 0.0808997 | 0 | 0.977924 |
| 153 days (hold-out length) | Plant median interval (40 days) | 0.0933251 | 3 | 0.994289 |
| 153 days (hold-out length) | Interval 30 days | 0.102302 | 5 | 0.995750 |

On the tuning span, one clean at 310 days is slightly cheaper than never cleaning. On a year, and on the hold-out length, the tuned rules do not beat never cleaning. Both fixed calendars cost more because they pay for cleans the assumed energy price does not recover at this rate. That ranking is a scenario on an unconfirmed rate.

NREL steady-state wave RO (CC-BY-4.0, MHKDR 649) has 6005 rows, a maximum runtime of 5.0 minutes, and no cleaning column. It is not a fouling series. The EPA malathion workbook (US public domain) is a pre/post snapshot. Orange County and Hazen Harvard sets are CC BY-NC-ND and were not used.

## Synthetic twin (separate from the public series)

`research/run_study.py` still runs the original twin (policies tuned on 20 training years at fouling scale 1.0; 100 test years per row; permeability measurement noise 3% for the noisy policy). Rounded from `results.json`:

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

On the synthetic twin, a 30-day calendar costs about 11% more than the tuned rules in the base case. Condition-based rules keep permeability above a floor when the fouling scale rises. Those statements are about the twin, not the public series.

## Not shown

The public proxy is a censored derived indicator, not a signed normalised permeability, and the raw 10-minute series is not in the deposit. Held-out windows contradict the fitted decay. Scenario costs use assumed prices. The synthetic twin's parameters remain assumptions.

## Next steps toward TRL 5

A signed daily normalised permeability, with cleaning dates and the plant's prices, from one reuse plant. Replay on later months has to predict permeability before a cost ranking is treated as evidence.
