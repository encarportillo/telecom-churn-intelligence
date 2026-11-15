"""Reusable churn model construction and artifact loading."""

from pathlib import Path

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

FEATURE_COLUMNS = ("tenure", "monthly_charges")


def build_pipeline() -> Pipeline:
    """Create a baseline classifier pipeline for numeric customer features."""
    return Pipeline(
        [
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )


def load_pipeline(path: str | Path) -> Pipeline:
    """Load a trained pipeline artifact from disk."""
    artifact = joblib.load(path)
    if not isinstance(artifact, Pipeline):
        raise TypeError(f"Model artifact at {path} is not a scikit-learn Pipeline.")
    return artifact
