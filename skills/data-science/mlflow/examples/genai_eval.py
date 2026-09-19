from common import configure_local, package_versions, write_summary


def main() -> None:
    output_dir = configure_local("skill-genai-evaluation")

    import mlflow
    import mlflow.genai
    from mlflow.genai.scorers import scorer

    @mlflow.trace(span_type="CHAIN")
    def answer(question: str) -> str:
        responses = {
            "What is the returns window?": "30 days",
            "Is collection available?": "Yes",
            "What does delivery cost?": "Free",
        }
        return responses.get(question, "Unknown")

    @scorer
    def exact_match(outputs, expectations) -> bool:
        return outputs == expectations["expected_response"]

    dataset = [
        {"inputs": {"question": "What is the returns window?"}, "expectations": {"expected_response": "30 days"}},
        {"inputs": {"question": "Is collection available?"}, "expectations": {"expected_response": "Yes"}},
        {"inputs": {"question": "What does delivery cost?"}, "expectations": {"expected_response": "5 credits"}},
    ]
    with mlflow.start_run(run_name="deterministic-offline-evaluation"):
        mlflow.set_tags({"purpose": "synthetic-demo", "protocol_id": "exact-match-v1"})
        mlflow.log_params({"application_version": "lookup-v1", "dataset_version": "synthetic-v1"})
        mlflow.log_dict({"rows": dataset}, "evaluation/dataset.json")
        mlflow.log_artifact(__file__, artifact_path="code")
        result = mlflow.genai.evaluate(data=dataset, predict_fn=answer, scorers=[exact_match])
        traces = mlflow.search_traces(run_id=result.run_id, return_type="list", flush=True)
        if len(traces) != len(dataset):
            raise ValueError("Evaluation trace coverage is incomplete")
        scores = []
        for trace in traces:
            assessments = trace.search_assessments(name="exact_match", type="feedback")
            if len(assessments) != 1:
                raise ValueError("Expected exactly one score per evaluation trace")
            assessment = assessments[0]
            if assessment.error is not None or not isinstance(assessment.value, bool):
                raise ValueError("Evaluation contains a scorer error or missing boolean score")
            scores.append(assessment.value)
        observed_mean = sum(scores) / len(scores)
        if abs(result.metrics["exact_match/mean"] - observed_mean) > 1e-12:
            raise ValueError("Aggregate score disagrees with row-level evidence")
        summary = {
            "tracking_uri": mlflow.get_tracking_uri(),
            "run_id": result.run_id,
            "versions": package_versions(),
            "row_count": len(dataset),
            "scored_rows": len(scores),
            "passed_rows": sum(scores),
            "failed_rows": len(scores) - sum(scores),
            "exact_match_mean": observed_mean,
            "release_status": "demo-only; deliberate quality failure; no production approval",
        }
        mlflow.log_dict(summary, "evaluation/summary.json")
    write_summary(output_dir, summary)


if __name__ == "__main__":
    main()
