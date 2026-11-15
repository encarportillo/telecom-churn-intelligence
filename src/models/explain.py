"""SHAP utilities for explaining churn model predictions."""

import pandas as pd
import shap
from sklearn.pipeline import Pipeline


def build_explainer(model: Pipeline, background: pd.DataFrame) -> shap.Explainer:
    """Create a model-agnostic explainer using representative background rows."""
    if background.empty:
        raise ValueError("At least one background row is required to explain predictions.")
    return shap.Explainer(model.predict_proba, background)
