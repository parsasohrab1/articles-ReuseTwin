# Data licenses

The fit uses one redistributed table. Three other public RO sets were screened and not fitted. Harvard sets under CC BY-NC-ND were not downloaded into this repository.

## Used

Yi Hsiang Su (2026). *Auditable clean-in-place decision support from routine single-plant SWRO SCADA: reproducibility deposit.* Zenodo. https://doi.org/10.5281/zenodo.21055948

- License: CC-BY-4.0 (data). The two CSV files under `data/swro_su2026/` are the deposited derived tables, unchanged.
- What is not included, here or in the deposit: the raw 10-minute SCADA series, prices, membrane model, and calendar dates.
- This repository does not copy the deposit's analysis scripts. The fouling equation is the one already in `src/reusetwin/model.py`.

## Screened, not fitted

| Set | License | Why it was not fitted |
|-----|---------|------------------------|
| NREL experimental wave-desalination RO, steady state. Sitterley, Binger, and Jenne, MHKDR 649, https://mhkdr.openei.org/submissions/649 | CC-BY-4.0 | Minutes-long transport test at set pressures. No cleaning events. File: `data/nrel_wave_ro/steady_state.csv`. The screen (row count, duration, no cleaning column) is computed in `results.json`. |
| EPA membrane malathion workbook, https://doi.org/10.23719/1529271 | US public domain (17 USC 105) | Pre-clean and post-clean flux and rejection snapshots for one foulant exposure. Not a daily series. Not redistributed. |
| Orange County RO fouling data, https://doi.org/10.7910/DVN/PVY3QD | CC BY-NC-ND 4.0 | Non-commercial and no-derivatives. Not redistributed and not fitted. |
| Hazen RO facility CIP data, https://doi.org/10.7910/DVN/VURALX | CC BY-NC-ND 4.0 | Non-commercial and no-derivatives. Not redistributed and not fitted. |
