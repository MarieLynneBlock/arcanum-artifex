"""Synthetic single-event workflow; no real data, file output or installation."""

from importlib.metadata import version

import numpy as np
import pandas as pd
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import proportional_hazard_test
from lifelines.utils import concordance_index
from sksurv.metrics import brier_score, concordance_index_censored
from sksurv.nonparametric import CensoringDistributionEstimator
from sksurv.util import Surv


FEATURES = ["monthly_contract", "baseline_usage"]
MODEL_COLUMNS = ["duration", "event", *FEATURES]


def make_cohort(size: int, seed: int, prefix: str) -> pd.DataFrame:
    """Generate independent subjects with a known PH process, in months."""
    generator = np.random.default_rng(seed)
    monthly_contract = generator.binomial(1, 0.5, size)
    baseline_usage = generator.normal(size=size)
    event_rate = 0.055 * np.exp(0.7 * monthly_contract - 0.4 * baseline_usage)
    event_time = generator.exponential(1.0 / event_rate)
    censor_time = np.minimum(generator.exponential(36.0, size), 24.0)
    return pd.DataFrame(
        {
            "subject_id": [f"{prefix}-{index}" for index in range(size)],
            "duration": np.minimum(event_time, censor_time),
            "event": event_time <= censor_time,
            "monthly_contract": monthly_contract,
            "baseline_usage": baseline_usage,
        }
    )


def validate_cohort(data: pd.DataFrame) -> None:
    """Check this example's baseline, positive-duration, single-event contract."""
    required = ["subject_id", *MODEL_COLUMNS]
    if data.empty or not data.columns.is_unique:
        raise ValueError("Expected nonempty data with unique column names.")
    if not set(required).issubset(data.columns):
        raise ValueError("Missing required cohort columns.")
    if data.loc[:, required].isna().any().any():
        raise ValueError("Missing outcomes, IDs or predictors require resolution.")
    if data["subject_id"].duplicated().any():
        raise ValueError("Expected one baseline row per subject.")
    if not data["event"].isin([0, 1]).all():
        raise ValueError("Event must be Boolean or explicitly coded 0/1.")
    if not np.isfinite(data.loc[:, ["duration", *FEATURES]].to_numpy(dtype=float)).all():
        raise ValueError("Duration and predictors must be finite numeric values.")
    if (data["duration"] <= 0).any():
        raise ValueError("Resolve non-positive durations before using this example.")
    if not data["event"].any():
        raise ValueError("No events: this example cannot fit or evaluate a Cox model.")


def normalize_event_indicator(data: pd.DataFrame) -> pd.DataFrame:
    """Return a copy whose validated event indicator has Boolean dtype."""
    normalized = data.copy()
    normalized["event"] = normalized["event"].astype(bool)
    return normalized


def check_metric_support(
    training: pd.DataFrame, testing: pd.DataFrame, times: np.ndarray
) -> None:
    """Reject unsupported Brier-score inputs without altering any outcomes."""
    if times.ndim != 1 or not times.size or not np.isfinite(times).all():
        raise ValueError("Expected a finite, nonempty one-dimensional time grid.")
    if (times <= 0).any() or (np.diff(times) <= 0).any():
        raise ValueError("Times must be positive and strictly increasing.")
    if times[0] < testing["duration"].min() or times[-1] >= testing["duration"].max():
        raise ValueError("Requested horizons lack evaluation follow-up support.")
    if testing["duration"].max() > training["duration"].max():
        raise ValueError("Evaluation follow-up exceeds training censoring support.")
    training_target = Surv.from_dataframe("event", "duration", training)
    censoring = CensoringDistributionEstimator().fit(training_target)
    relevant_events = testing.loc[
        testing["event"].astype(bool) & (testing["duration"] <= times[-1]), "duration"
    ].to_numpy()
    probabilities = censoring.predict_proba(np.concatenate([times, relevant_events]))
    if not np.isfinite(probabilities).all() or (probabilities <= 0).any():
        raise ValueError("Required censoring probabilities are not positive and finite.")
    print(f"Minimum required training censoring survival: {probabilities.min():.3f}")


def check_score_direction() -> None:
    """Verify each concordance API treats a larger score as greater event risk."""
    durations = np.array([1.0, 2.0, 3.0, 4.0])
    events = np.array([True, True, True, True])
    risk_scores = np.array([4.0, 3.0, 2.0, 1.0])
    assert concordance_index(durations, -risk_scores, events) == 1.0
    assert concordance_index_censored(events, durations, risk_scores)[0] == 1.0


def make_calibration_groups(predicted_risk: pd.Series) -> pd.Series | None:
    """Create non-arbitrary calibration groups, or decline when scores are tied."""
    if predicted_risk.nunique() < 2:
        return None
    groups = pd.qcut(predicted_risk, 4, labels=False, duplicates="drop")
    if groups.isna().any() or groups.nunique() < 2:
        return None
    return groups


def supports_calibration_horizon(rows: pd.DataFrame, horizon: float) -> bool:
    """Reject a horizon beyond observed group follow-up unless all had events."""
    if rows["duration"].max() >= horizon:
        return True
    return rows["event"].astype(bool).all()


def check_rejections(training: pd.DataFrame, testing: pd.DataFrame) -> None:
    """Exercise failure paths without treating them as model-quality thresholds."""
    for column, value in [("event", np.nan), ("event", 2), ("duration", -1.0)]:
        invalid = training.astype({"event": float}).copy()
        invalid.loc[invalid.index[0], column] = value
        try:
            validate_cohort(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Invalid {column} was accepted.")
    try:
        check_metric_support(training, testing, np.array([36.0]))
    except ValueError:
        pass
    else:
        raise AssertionError("Unsupported horizon was accepted.")

    integer_events = training.copy()
    integer_events["event"] = integer_events["event"].astype(int)
    validate_cohort(integer_events)
    assert normalize_event_indicator(integer_events)["event"].dtype == bool

    assert make_calibration_groups(pd.Series([0.5, 0.5, 0.5])) is None


def main() -> None:
    """Run a reproducible API smoke test, not a production model assessment."""
    training = make_cohort(1000, seed=42, prefix="train")
    testing = make_cohort(400, seed=43, prefix="test")
    for cohort in (training, testing):
        validate_cohort(cohort)
    training = normalize_event_indicator(training)
    testing = normalize_event_indicator(testing)
    assert set(training["subject_id"]).isdisjoint(testing["subject_id"])
    check_rejections(training, testing)
    check_score_direction()
    times = np.array([3.0, 6.0, 12.0])
    check_metric_support(training, testing, times)

    model = CoxPHFitter().fit(
        training.loc[:, MODEL_COLUMNS], duration_col="duration", event_col="event"
    )
    diagnostics = proportional_hazard_test(
        model, training.loc[:, MODEL_COLUMNS], time_transform="rank"
    )
    predictions = model.predict_survival_function(testing.loc[:, FEATURES], times=times)
    assert predictions.columns.equals(testing.index)
    survival_probabilities = predictions.to_numpy().T
    assert survival_probabilities.shape == (len(testing), len(times))
    assert np.isfinite(survival_probabilities).all()
    assert ((survival_probabilities >= 0) & (survival_probabilities <= 1)).all()
    assert (np.diff(survival_probabilities, axis=1) <= 1e-12).all()

    risk_scores = model.predict_partial_hazard(testing.loc[:, FEATURES]).to_numpy()
    lifelines_concordance = concordance_index(
        testing["duration"], -risk_scores, testing["event"]
    )
    sksurv_concordance = concordance_index_censored(
        testing["event"].to_numpy(), testing["duration"].to_numpy(), risk_scores
    )[0]
    # Both are Harrell's C; they can diverge when durations or scores are tied.
    assert 0.0 <= lifelines_concordance <= 1.0
    assert 0.0 <= sksurv_concordance <= 1.0

    training_target = Surv.from_dataframe("event", "duration", training)
    testing_target = Surv.from_dataframe("event", "duration", testing)
    baseline = KaplanMeierFitter().fit(training["duration"], training["event"])
    baseline_probabilities = np.tile(baseline.predict(times).to_numpy(), (len(testing), 1))
    _, model_brier = brier_score(
        training_target, testing_target, survival_probabilities, times
    )
    _, baseline_brier = brier_score(
        training_target, testing_target, baseline_probabilities, times
    )
    assert np.isfinite(model_brier).all() and np.isfinite(baseline_brier).all()

    calibration = testing.loc[:, ["duration", "event"]].copy()
    calibration["predicted_risk"] = 1.0 - survival_probabilities[:, -1]
    calibration_rows = []
    groups = make_calibration_groups(calibration["predicted_risk"])
    if groups is not None:
        calibration["group"] = groups
        for group, rows in calibration.groupby("group", observed=True):
            result = {
                "group": group,
                "subjects": len(rows),
                "horizon": times[-1],
                "at_risk_at_horizon": int((rows["duration"] >= times[-1]).sum()),
                "predicted_risk": rows["predicted_risk"].mean(),
                "calibration_status": "unsupported",
                "km_event_risk": np.nan,
                "risk_lower_95": np.nan,
                "risk_upper_95": np.nan,
            }
            if supports_calibration_horizon(rows, times[-1]):
                observed = KaplanMeierFitter().fit(
                    rows["duration"], rows["event"], timeline=[0.0, times[-1]]
                )
                interval = observed.confidence_interval_survival_function_.loc[times[-1]]
                result.update(
                    calibration_status="supported",
                    km_event_risk=1.0 - observed.predict(times[-1]),
                    risk_lower_95=1.0 - interval.iloc[1],
                    risk_upper_95=1.0 - interval.iloc[0],
                )
            calibration_rows.append(result)

    print("SYNTHETIC ONLY: independent baseline cohorts; time unit = months")
    print({name: version(name) for name in ["lifelines", "scikit-survival", "pandas", "numpy"]})
    print(f"Train events: {training['event'].sum()}/{len(training)}")
    print(f"Test events: {testing['event'].sum()}/{len(testing)}")
    print(f"Held-out Harrell concordance (lifelines): {lifelines_concordance:.3f}")
    print(f"Held-out Harrell concordance (scikit-survival): {sksurv_concordance:.3f}")
    print(pd.DataFrame({"month": times, "cox_brier": model_brier, "km_brier": baseline_brier}))
    print("Rank-transformed Schoenfeld test; not proof of PH:")
    print(diagnostics.summary)
    print(
        f"Illustrative {times[-1]:g}-month grouped calibration; "
        "independent censoring by construction:"
    )
    if calibration_rows:
        print(pd.DataFrame(calibration_rows).to_string(index=False))
    else:
        print("Unavailable: predictions did not form at least two non-tied groups.")
    print("PASS: input, rejection, alignment, probability and score-direction checks.")
    print("Not assessed: real cohort validity, graphical PH checks or deployment readiness.")


if __name__ == "__main__":
    main()
