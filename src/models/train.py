"""Train and save the baseline churn classifier from a prepared CSV."""

import argparse
from pathlib import Path

import joblib
import pandas as pd

from src.etl.transform import prepare_customers
from src.models.pipeline import FEATURE_COLUMNS, build_pipeline


def train(input_path: Path, output_path: Path) -> None:
    """Fit a model from a customer CSV and persist the fitted pipeline."""
    customers = prepare_customers(pd.read_csv(input_path))
    if customers["churn"].nunique() < 2:
        raise ValueError("Training data must contain both churn classes.")

    model = build_pipeline()
    model.fit(customers.loc[:, FEATURE_COLUMNS], customers["churn"].astype(int))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Prepared customer CSV.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/churn_model.joblib"),
        help="Destination for the fitted model.",
    )
    args = parser.parse_args()
    train(args.input, args.output)


if __name__ == "__main__":
    main()
