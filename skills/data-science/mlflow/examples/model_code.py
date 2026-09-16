import json
from pathlib import Path

import mlflow
import numpy as np
import pandas as pd


class AffineModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        settings = json.loads(Path(context.artifacts["settings"]).read_text(encoding="utf-8"))
        self.scale = float(settings["scale"])
        self.offset = float(settings["offset"])
        if not np.isfinite([self.scale, self.offset]).all():
            raise ValueError("Model configuration must be finite")

    def predict(self, context, model_input, params=None):
        values = model_input["value"].to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError("Input values must be finite")
        predictions = values * self.scale + self.offset
        if not np.isfinite(predictions).all():
            raise ValueError("Predictions must be finite")
        return pd.DataFrame({"prediction": predictions}, index=model_input.index)


mlflow.models.set_model(AffineModel())
