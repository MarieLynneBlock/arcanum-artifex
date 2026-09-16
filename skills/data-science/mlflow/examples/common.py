import argparse
import json
import os
import platform
import tempfile
from importlib.metadata import version
from pathlib import Path


def configure_local(experiment_name: str) -> Path:
    parser = argparse.ArgumentParser(description="Run a synthetic, local-only MLflow example.")
    parser.add_argument("--output-dir", type=Path)
    arguments = parser.parse_args()
    inherited = sorted(
        name for name in os.environ if name.startswith(("MLFLOW_", "OTEL_"))
    )
    if inherited:
        raise ValueError(
            "Use a clean demo process without inherited MLflow/OpenTelemetry settings: "
            + ", ".join(inherited)
        )
    if arguments.output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix="mlflow-skill-"))
    else:
        output_dir = arguments.output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=False)

    import mlflow
    from sqlalchemy.engine import URL

    tracking_uri = URL.create(
        "sqlite", database=str(output_dir / "tracking.db")
    ).render_as_string(hide_password=False)
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_registry_uri(tracking_uri)
    experiment_id = mlflow.create_experiment(
        experiment_name,
        artifact_location=(output_dir / "artifacts").as_uri(),
    )
    mlflow.set_experiment(experiment_id=experiment_id)
    return output_dir


def package_versions() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        **{
            package: version(package)
            for package in ("mlflow", "numpy", "pandas", "scikit-learn", "skops")
        },
    }


def write_summary(output_dir: Path, summary: dict) -> None:
    destination = output_dir / "summary.json"
    destination.write_text(
        json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8"
    )
    print(f"Results: {destination}")
