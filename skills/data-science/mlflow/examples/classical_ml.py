from common import configure_local, package_versions, write_summary


def main() -> None:
    output_dir = configure_local("skill-classical-ml")

    import mlflow
    import mlflow.sklearn
    import numpy as np
    import pandas as pd
    from mlflow.models import infer_signature
    from sklearn.base import clone
    from sklearn.datasets import make_classification
    from sklearn.dummy import DummyClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, average_precision_score, log_loss, roc_auc_score
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    seed = 42
    features, labels = make_classification(
        n_samples=600, n_features=8, n_informative=5, random_state=seed
    )
    frame = pd.DataFrame(features, columns=[f"feature_{index}" for index in range(8)])
    development_ids, test_ids = train_test_split(
        np.arange(len(frame)), test_size=0.2, stratify=labels, random_state=seed
    )
    train_ids, validation_ids = train_test_split(
        development_ids,
        test_size=0.25,
        stratify=labels[development_ids],
        random_state=seed,
    )
    split_ids = {
        "train": train_ids.tolist(),
        "validation": validation_ids.tolist(),
        "test": test_ids.tolist(),
    }
    versions = package_versions()

    def metrics_for(estimator, row_ids) -> dict[str, float]:
        probabilities = estimator.predict_proba(frame.iloc[row_ids])[:, 1]
        targets = labels[row_ids]
        return {
            "roc_auc": float(roc_auc_score(targets, probabilities)),
            "average_precision": float(average_precision_score(targets, probabilities)),
            "log_loss": float(log_loss(targets, probabilities)),
            "accuracy": float(accuracy_score(targets, probabilities >= 0.5)),
        }

    with mlflow.start_run(run_name="synthetic-model-selection") as parent:
        mlflow.set_tags({"purpose": "synthetic-demo", "protocol_id": "iid-stratified-v1"})
        mlflow.log_params({"seed": seed, "primary_metric": "roc_auc", "threshold": 0.5})
        mlflow.log_dict(versions, "environment/versions.json")
        mlflow.log_dict(split_ids, "data/split_ids.json")
        mlflow.log_artifact(__file__, artifact_path="code")
        for context, row_ids in (("training", train_ids), ("validation", validation_ids)):
            dataset = mlflow.data.from_pandas(
                frame.iloc[row_ids].assign(target=labels[row_ids]),
                name=f"synthetic-{context}",
                targets="target",
            )
            mlflow.log_input(dataset, context=context)

        baseline = DummyClassifier(strategy="prior").fit(frame.iloc[train_ids], labels[train_ids])
        baseline_validation = metrics_for(baseline, validation_ids)
        mlflow.log_metrics(
            {f"baseline_validation_{key}": value for key, value in baseline_validation.items()}
        )
        candidates = []
        for regularisation in (0.1, 1.0, 10.0):
            with mlflow.start_run(run_name=f"logistic-C-{regularisation}", nested=True) as trial:
                estimator = make_pipeline(
                    SimpleImputer(strategy="median"),
                    StandardScaler(),
                    LogisticRegression(C=regularisation, max_iter=500, random_state=seed),
                )
                estimator.fit(frame.iloc[train_ids], labels[train_ids])
                validation_metrics = metrics_for(estimator, validation_ids)
                mlflow.log_params({"C": regularisation, "seed": seed})
                mlflow.set_tags({"phase": "selection", "protocol_id": "iid-stratified-v1"})
                mlflow.log_metrics(
                    {f"validation_{key}": value for key, value in validation_metrics.items()}
                )
                candidates.append((validation_metrics["roc_auc"], trial.info.run_id, estimator))

        best_score, selected_run_id, selected = max(candidates, key=lambda item: item[0])
        final_model = clone(selected).fit(frame.iloc[development_ids], labels[development_ids])
        final_baseline = clone(baseline).fit(frame.iloc[development_ids], labels[development_ids])
        with mlflow.start_run(run_name="final-holdout", nested=True) as final_run:
            mlflow.set_tags({"phase": "final-test", "selected_run_id": selected_run_id})
            mlflow.log_params({"C": selected[-1].C, "seed": seed, "threshold": 0.5})
            for context, row_ids in (("training", development_ids), ("testing", test_ids)):
                mlflow.log_input(
                    mlflow.data.from_pandas(
                        frame.iloc[row_ids].assign(target=labels[row_ids]),
                        name=f"synthetic-final-{context}",
                        targets="target",
                    ),
                    context=context,
                )
            candidate_metrics = metrics_for(final_model, test_ids)
            baseline_metrics = metrics_for(final_baseline, test_ids)
            mlflow.log_metrics({f"test_{key}": value for key, value in candidate_metrics.items()})
            mlflow.log_metrics({f"baseline_test_{key}": value for key, value in baseline_metrics.items()})
            example = frame.iloc[development_ids[:5]]
            expected = final_model.predict_proba(example)
            model_info = mlflow.sklearn.log_model(
                final_model,
                name="classifier",
                serialization_format="skops",
                skops_trusted_types=["numpy.dtype"],
                pyfunc_predict_fn="predict_proba",
                signature=infer_signature(example, expected),
                input_example=example,
                pip_requirements=[
                    f"{package}=={versions[package]}"
                    for package in ("mlflow", "numpy", "pandas", "scikit-learn", "skops")
                ],
            )
            reloaded = mlflow.pyfunc.load_model(model_info.model_uri)
            np.testing.assert_allclose(reloaded.predict(example), expected, rtol=1e-10)
            mlflow.log_dict(
                {"columns": frame.columns.tolist(), "classes": final_model.classes_.tolist()},
                "inference/schema.json",
            )
            summary = {
                "tracking_uri": mlflow.get_tracking_uri(),
                "parent_run_id": parent.info.run_id,
                "selected_run_id": selected_run_id,
                "final_run_id": final_run.info.run_id,
                "model_uri": model_info.model_uri,
                "versions": versions,
                "split_ids": split_ids,
                "selected_validation_roc_auc": best_score,
                "candidate_metrics": candidate_metrics,
                "baseline_metrics": baseline_metrics,
                "input_example": example.to_dict(orient="list"),
                "expected_probabilities": expected.tolist(),
                "release_status": "demo-only; no production approval",
            }
            mlflow.log_dict(summary, "evaluation/summary.json")
    write_summary(output_dir, summary)


if __name__ == "__main__":
    main()
