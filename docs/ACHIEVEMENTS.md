# Achievements

Record of what this product has produced. Counts are written by `research/run_study.py` from `research/results.json`. This page is not a journal submission.

| Item | Record |
|---|---|
| Product | Exponential fouling-rate fit and a frozen comparison of cleaning rules |
| Data used | Su 2026, Zenodo 10.5281/zenodo.21055948, CC-BY-4.0 |
| Data screened out | NREL MHKDR 649 steady state, CC-BY-4.0; EPA malathion workbook, US public domain |
| Data not taken | Orange County and Hazen Harvard sets, CC BY-NC-ND 4.0 |
| Method disclosed | Log-linear rate of a public permeability proxy; interval and threshold rules already in this repository |
| Method not disclosed | No cleaning chemistry and no unpublished control law |
| Maturity | TRL 4. See `docs/TRL.md` |
| Article text | `article/manuscript.txt` and `article/abstract.md` |
| Call checked | Water (MDPI), Water Treatment Technology and Artificial Intelligence, deadline 30 October 2026 |
| Uploaded | No. The deadline had passed on the check date 7 November 2026 |
| Patent counsel | Not confirmed. Upload stays closed |

## Measured result

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

The held-out rates are the achievement. They are negative, so a cost ranking on the training rate is not a saving.
