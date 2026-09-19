import argparse
import json
import math
from pathlib import Path


def finite_number(value, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return float(value)


def compare(evidence: dict, policy: dict) -> None:
    from mlflow import validate_evaluation_results
    from mlflow.models import EvaluationResult, MetricThreshold

    if not isinstance(evidence, dict) or not isinstance(policy, dict):
        raise ValueError("Evidence and policy must be JSON objects")
    for role in ("candidate", "baseline"):
        record = evidence.get(role)
        if not isinstance(record, dict) or not isinstance(record.get("metrics"), dict):
            raise ValueError(f"{role} and its metrics must be JSON objects")
    candidate = evidence["candidate"]
    baseline = evidence["baseline"]
    for field in (
        "protocol_id", "evaluation_dataset_id", "split_id", "phase",
        "model_uri", "run_id",
    ):
        for role, record in (("candidate", candidate), ("baseline", baseline)):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip() or "[TODO]" in value:
                raise ValueError(f"{role} {field} is missing")
        if candidate[field] != baseline[field] and field in (
            "protocol_id", "evaluation_dataset_id", "split_id", "phase",
        ):
            raise ValueError(f"Candidate and baseline {field} differ")
    if candidate["phase"] not in ("validation", "final-test"):
        raise ValueError("Evidence phase must be validation or final-test")
    rules = policy["metrics"]
    if not isinstance(rules, dict) or not rules:
        raise ValueError("Policy must declare at least one metric")
    thresholds = {}
    candidate_metrics = {}
    baseline_metrics = {}
    for metric, rule in rules.items():
        if not isinstance(rule, dict) or set(rule) - {
            "threshold", "higher_is_better", "min_absolute_change", "min_relative_change"
        }:
            raise ValueError(f"Invalid policy rule for {metric}")
        if type(rule.get("higher_is_better")) is not bool:
            raise ValueError(f"Direction must be explicit for {metric}")
        # Unlike MetricThreshold itself, this gate always requires an absolute threshold.
        if "threshold" not in rule:
            raise ValueError(f"{metric} rule requires an explicit 'threshold' value")
        threshold = finite_number(rule["threshold"], f"{metric} threshold")
        improvements = {}
        for field in ("min_absolute_change", "min_relative_change"):
            if field in rule:
                change = finite_number(rule[field], f"{metric} {field}")
                if change < 0:
                    raise ValueError(f"{field} cannot be negative")
                improvements[field] = change
        for role, record, destination in (
            ("candidate", candidate, candidate_metrics),
            ("baseline", baseline, baseline_metrics),
        ):
            destination[metric] = finite_number(record["metrics"].get(metric), f"{role} {metric}")
        if "min_relative_change" in improvements and baseline_metrics[metric] <= 0:
            raise ValueError(f"Relative improvement requires a positive baseline for {metric}")
        thresholds[metric] = MetricThreshold(
            threshold=threshold, greater_is_better=rule["higher_is_better"], **improvements
        )
    validate_evaluation_results(
        validation_thresholds=thresholds,
        candidate_result=EvaluationResult(metrics=candidate_metrics, artifacts={}),
        baseline_result=EvaluationResult(metrics=baseline_metrics, artifacts={}),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compare local metric evidence against a policy; never promote or deploy. "
            "Every policy metric rule must set an explicit numeric 'threshold' and boolean "
            "'higher_is_better', even when only 'min_absolute_change'/'min_relative_change' "
            "gating is desired."
        )
    )
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--policy", required=True, type=Path)
    arguments = parser.parse_args()
    try:
        from mlflow.models.evaluation.validation import ModelValidationFailedException
    except ImportError as error:
        print(f"GATE COULD NOT RUN: {error}")
        return 2
    try:
        evidence = json.loads(arguments.evidence.read_text(encoding="utf-8"))
        policy = json.loads(arguments.policy.read_text(encoding="utf-8"))
        compare(evidence, policy)
    except ModelValidationFailedException as error:
        print(f"METRIC GATE FAILED: {error}")
        return 1
    except (KeyError, TypeError, ValueError, OSError) as error:
        print(f"INVALID EVIDENCE OR POLICY: {error}")
        return 2
    except Exception as error:
        print(f"GATE COULD NOT RUN: {error}")
        return 2
    print("METRIC GATE PASSED: scalar checks only; not a release approval")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
