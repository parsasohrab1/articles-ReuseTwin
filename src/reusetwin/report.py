"""Registration text. Every count is taken from the public-series payload."""

from __future__ import annotations

from pathlib import Path

START = "<!-- results:start -->"
END = "<!-- results:end -->"


def g(value: float) -> str:
    return f"{value:.6g}"


def measured_block(real: dict) -> str:
    fit = real["fit"]
    hold = real["holdout_prediction"]
    split = real["split"]
    sched = real["schedule_scenario"]
    rates = fit["train_rates_per_day"]
    test_rates = hold["test_rates_per_day"]
    n_pos = sum(rate > 0 for rate in rates)
    n_neg = sum(rate < 0 for rate in test_rates)
    lines = [
        (
            f"Days {g(split['day_min'])} to {g(split['day_max'])}. "
            f"Cutoff {g(split['cutoff'])}."
        ),
        (
            f"Eligible segments: train {split['n_eligible']['train']}, "
            f"test {split['n_eligible']['test']}, "
            f"crossed {split['n_eligible']['crossed']}."
        ),
        (
            f"Median training rate {g(fit['kf_per_day'])} per day. "
            f"Positive training segments {n_pos} of {len(rates)} "
            f"({g(fit['fraction_train_rates_positive'])}). "
            f"Median residual sd {g(fit['median_residual_sd'])}."
        ),
        (
            f"Held-out segments {hold['n']}. "
            f"Negative held-out rates {n_neg} of {len(test_rates)}. "
            f"MAE of terminal K {g(hold['mae_k'])}. "
            f"Mean error, predicted minus observed, {g(hold['mean_error_k'])}."
        ),
        (
            f"Tuned interval {g(sched['interval_days_tuned'])} days. "
            f"Tuned threshold {g(sched['threshold_k_tuned'])}. "
            f"Plant median interval {g(sched['plant_median_interval_days'])} days. "
            "Irreversible loss used "
            f"{g(sched['irreversible_used'])}. Identified: {sched['irreversible_identified']}."
        ),
    ]
    for horizon in ("tuning", "year", "holdout"):
        block = sched[horizon]
        for name, metrics in block["policies"].items():
            lines.append(
                f"{horizon} {block['horizon_days']} days, {name}: "
                f"cost {g(metrics['cost_per_m3'])}, "
                f"cleanings {metrics['cleanings']}, "
                f"min K {g(metrics['min_k'])}."
            )
    nrel = real["screened_out"]["nrel_wave_ro_steady_state"]
    lines.append(
        f"NREL steady state: {nrel['n_rows']} rows, "
        f"runtime max {g(nrel['runtime_minutes_max'])} minutes, "
        f"cleaning column {nrel['has_cleaning_column']}, "
        f"used for fit {nrel['used_for_fit']}."
    )
    return "\n".join(lines)


def abstract_text(real: dict) -> str:
    """Short research abstract. No bibliographic citations. Counts come from the payload."""
    fit = real["fit"]
    hold = real["holdout_prediction"]
    sched = real["schedule_scenario"]
    rates = fit["train_rates_per_day"]
    test_rates = hold["test_rates_per_day"]
    n_pos = sum(rate > 0 for rate in rates)
    n_neg = sum(rate < 0 for rate in test_rates)
    year = sched["year"]["policies"]
    tune = sched["tuning"]["policies"]
    paragraphs = [
        (
            "This note asks whether an exponential permeability decay, fit on the early "
            "part of one public seawater reverse-osmosis series, predicts later windows "
            "and whether a permeability threshold then costs less than a fixed cleaning "
            "interval. The series is the de-identified daily indicator table and "
            "clean-in-place ledger in Zenodo deposit 10.5281/zenodo.21055948, "
            "licensed CC-BY-4.0. The raw ten-minute records and the plant prices are "
            "not in the deposit. A permeability proxy is the ratio of one plus the "
            "stored specific-flux deviation to one plus the stored net-driving-pressure "
            "deviation, on the trimmed daily basis. Those deviations are stored as "
            "non-negative numbers, so the proxy is biased high when a true deviation "
            "was negative."
        ),
        (
            "Windows between cleanings are fit by a straight line on the logarithm of "
            "the proxy. A window that contains the day at eighty percent of the span "
            "is unused. The rate used afterwards is the median of the earlier eligible "
            "windows. Interval and threshold rules are chosen on that training length "
            "with a feed index of one and with no irreversible loss, because a "
            "per-cleaning loss was not identified. Costs use the repository price "
            "assumptions, not invoices. The equation is the decay already stated in "
            "the repository model. Cleaning chemistry is not stated."
        ),
        (
            f"The median training rate is {g(fit['kf_per_day'])} per day. "
            f"{n_pos} of {len(rates)} training windows have a positive rate. "
            f"All {n_neg} of {len(test_rates)} held-out windows have a negative rate. "
            f"The mean absolute error of terminal proxy permeability is {g(hold['mae_k'])}, "
            "and the mean error, predicted minus observed, is "
            f"{g(hold['mean_error_k'])}. The decay forecast sits below the later "
            "observations. On the training length, one clean at "
            f"{g(sched['interval_days_tuned'])} days costs "
            f"{g(tune['interval_tuned']['cost_per_m3'])} per cubic metre against "
            f"{g(tune['never']['cost_per_m3'])} for no cleaning. On a year, no cleaning "
            f"costs {g(year['never']['cost_per_m3'])}, the tuned threshold does not fire, "
            f"and a thirty-day calendar costs {g(year['interval_30d']['cost_per_m3'])}. "
            "That ranking is a scenario on a rate the later windows do not support."
        ),
        (
            "The achievement recorded here is the negative hold-out, not a saving and "
            "not a plant design. This text has not been uploaded."
        ),
    ]
    return "\n\n".join(paragraphs)


def manuscript_text(real: dict) -> str:
    data = real["dataset"]
    return "\n".join([
        "An exponential fouling rate does not predict later windows of one public seawater reverse-osmosis series",
        "",
        "Abstract",
        "",
        abstract_text(real),
        "",
        "1. Data",
        "",
        (
            f"Source: {data['citation']}. License: {data['license']}. "
            f"Proxy: {data['proxy']} "
            "Files and the sets that were screened and not fitted are named in "
            "data/DATA_LICENSE.md. The National Renewable Energy Laboratory steady-state "
            "file is a minutes-long transport test and is not used for the rate. "
            "Two Harvard sets under CC BY-NC-ND are not in this repository."
        ),
        "",
        "2. Fit and comparison",
        "",
        (
            "The rate is the slope of log permeability on day index, the estimator "
            "already in src/reusetwin/estimator.py. The twin steps the same exponential "
            "decay as src/reusetwin/model.py, with the feed index fixed at 1. "
            "Rules are an interval and a threshold on the proxy, chosen by lowest "
            "scenario cost on the training length, then frozen. A fixed 30-day "
            "interval and the plant's median training gap are the fixed-time comparisons. "
            "No cleaning formulation, chemical name, or unpublished control law is stated."
        ),
        "",
        "3. Counts",
        "",
        measured_block(real),
        "",
        "4. Reading",
        "",
        (
            "Read the held-out rates before the cost rows. Every held-out window rises, "
            "so the median training decay is not confirmed. A cost row that prefers no "
            "cleaning, or a long interval, is a scenario under assumed prices on that "
            "unconfirmed rate. It is not a measured plant saving and not a cleaning design."
        ),
        "",
        "5. What is withheld",
        "",
        (
            "The manuscript states the public proxy, the log-linear rate, and the "
            "interval and threshold comparison already in this repository. It does not "
            "state cleaning chemistry. It has not been uploaded."
        ),
        "",
        "Data availability",
        "",
        (
            "Su, Yi Hsiang. Auditable clean-in-place decision support from routine "
            "single-plant SWRO SCADA: reproducibility deposit. Zenodo, "
            "https://doi.org/10.5281/zenodo.21055948, CC-BY-4.0."
        ),
        "",
        (
            "Sitterley, Kurban, Zachary Binger, and Scott Jenne. Experimental wave "
            "desalination data with variable feed and pressure input. National Renewable "
            "Energy Laboratory, Marine and Hydrokinetic Data Repository submission 649, "
            "https://mhkdr.openei.org/submissions/649, CC-BY-4.0. Screened, not fitted."
        ),
        "",
    ])


def fill_marked(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise ValueError(f"missing results markers in {path}")
    pre, rest = text.split(START, 1)
    _, post = rest.split(END, 1)
    path.write_text(
        f"{pre}{START}\n{block.rstrip()}\n{END}{post}",
        encoding="utf-8",
        newline="\n",
    )


def write_registration(root: Path, real: dict) -> None:
    """Refresh marked counts and rewrite the article files from one payload."""
    root = Path(root)
    block = measured_block(real)
    for relative in (
        "README.md",
        "docs/TRL.md",
        "docs/ACHIEVEMENTS.md",
        "docs/JOURNAL_FIT.md",
        "docs/REGISTRATION.md",
    ):
        fill_marked(root / relative, block)
    article = root / "article"
    article.mkdir(parents=True, exist_ok=True)
    (article / "abstract.md").write_text(abstract_text(real) + "\n", encoding="utf-8", newline="\n")
    (article / "manuscript.txt").write_text(
        manuscript_text(real), encoding="utf-8", newline="\n")
