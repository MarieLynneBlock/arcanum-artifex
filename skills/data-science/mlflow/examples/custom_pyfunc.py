import json
from pathlib import Path

from common import configure_local, package_versions, write_summary


def main() -> None:
    output_dir = configure_local("skill-custom-pyfunc")

    import mlflow
    import numpy as np
    import pandas as pd
    from mlflow.models import infer_signature

    versions = package_versions()
    settings = {"scale": 2.0, "offset": 1.0}
    settings_path = output_dir / "settings.json"
    settings_path.write_text(json.dumps(settings, allow_nan=False), encoding="utf-8")
    example = pd.DataFrame({"value": [0.0, 1.0, -2.0]})
    expected = pd.DataFrame({"prediction": [1.0, 3.0, -3.0]})
    with mlflow.start_run(run_name="source-based-affine-model") as run:
        mlflow.set_tags({"purpose": "synthetic-demo", "model_contract": "affine-v1"})
        mlflow.log_params(settings)
        mlflow.log_dict(versions, "environment/versions.json")
        model_info = mlflow.pyfunc.log_model(
            name="affine",
            python_model=str(Path(__file__).with_name("model_code.py")),
            artifacts={"settings": str(settings_path)},
            signature=infer_signature(example, expected),
            input_example=example,
            pip_requirements=[
                f"{package}=={versions[package]}" for package in ("mlflow", "numpy", "pandas")
            ],
        )
        settings_path.unlink()
        loaded = mlflow.pyfunc.load_model(model_info.model_uri)
        np.testing.assert_allclose(loaded.predict(example), expected)
        summary = {
            "tracking_uri": mlflow.get_tracking_uri(),
            "run_id": run.info.run_id,
            "model_uri": model_info.model_uri,
            "versions": versions,
            "input_example": example.to_dict(orient="list"),
            "expected_predictions": expected.to_dict(orient="list"),
            "release_status": "demo-only; no production approval",
        }
    write_summary(output_dir, summary)


if __name__ == "__main__":
    main()
