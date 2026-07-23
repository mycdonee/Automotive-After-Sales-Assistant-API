from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nhtsa_service_records.csv"
)

DEFAULT_MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "issue_classifier.joblib"
)

DEFAULT_METADATA_PATH = (
    PROJECT_ROOT
    / "models"
    / "classifier_metadata.json"
)

DEFAULT_REPORT_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "classification_report.json"
)

DEFAULT_CONFUSION_MATRIX_PATH = (
    PROJECT_ROOT
    / "evaluation"
    / "classification_confusion_matrix.csv"
)

MODEL_VERSION = "issue-classifier-logreg-v1"
TRAINING_DATA_SOURCE = "NHTSA Consumer Complaints"
DEFAULT_REVIEW_THRESHOLD = 0.60


def load_training_data(
    data_path: Path,
    min_records_per_category: int,
) -> pd.DataFrame:
    """Load and validate labelled complaint records for training."""

    if not data_path.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {data_path}"
        )

    records = pd.read_csv(
        data_path,
        dtype=str,
        keep_default_na=False,
    )

    required_columns = {
        "description",
        "category",
        "source",
    }

    missing_columns = required_columns.difference(
        records.columns
    )

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"Training data is missing required columns: {missing}"
        )

    working = records[
        [
            "description",
            "category",
            "source",
        ]
    ].copy()

    working["description"] = (
        working["description"]
        .astype(str)
        .str.strip()
    )

    working["category"] = (
        working["category"]
        .astype(str)
        .str.strip()
    )

    # Training uses complaint narratives only. Component and title fields
    # are excluded because they were used to create the category labels.
    working = working[
        working["description"].str.len().ge(40)
        & working["category"].ne("")
    ].copy()

    working = working.drop_duplicates(
        subset=[
            "description",
            "category",
        ]
    )

    category_counts = working[
        "category"
    ].value_counts()

    eligible_categories = category_counts[
        category_counts >= min_records_per_category
    ].index

    working = working[
        working["category"].isin(
            eligible_categories
        )
    ].copy()

    if working["category"].nunique() < 2:
        raise ValueError(
            "At least two sufficiently populated categories "
            "are required for classification."
        )

    return working.reset_index(drop=True)


def build_pipeline() -> Pipeline:
    """Create one pipeline for text vectorization and classification."""

    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    stop_words="english",
                    ngram_range=(1, 2),
                    min_df=2,
                    max_features=30_000,
                    sublinear_tf=True,
                ),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2_000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )


def make_json_serializable(
    value: Any,
) -> Any:
    """Convert NumPy values into standard Python JSON values."""

    if isinstance(value, dict):
        return {
            key: make_json_serializable(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_serializable(item)
            for item in value
        ]

    if isinstance(value, np.generic):
        return value.item()

    return value


def save_json(
    data: dict[str, Any],
    output_path: Path,
) -> None:
    """Write JSON through a temporary file to avoid partial output."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = output_path.with_suffix(
        f"{output_path.suffix}.tmp"
    )

    with temporary_path.open(
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(
            make_json_serializable(data),
            output_file,
            indent=2,
            ensure_ascii=False,
        )

    temporary_path.replace(output_path)


def save_model(
    pipeline: Pipeline,
    output_path: Path,
) -> None:
    """Save the fitted pipeline without separating preprocessing."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = output_path.with_suffix(
        f"{output_path.suffix}.tmp"
    )

    joblib.dump(
        pipeline,
        temporary_path,
    )

    temporary_path.replace(output_path)


def train_and_evaluate(
    records: pd.DataFrame,
    test_size: float,
    random_state: int,
) -> tuple[
    Pipeline,
    dict[str, Any],
    pd.DataFrame,
]:
    """Train the classifier and evaluate it on a stratified test set."""

    texts = records["description"]
    labels = records["category"]

    (
        train_texts,
        test_texts,
        train_labels,
        test_labels,
    ) = train_test_split(
        texts,
        labels,
        test_size=test_size,
        random_state=random_state,
        stratify=labels,
    )

    pipeline = build_pipeline()

    pipeline.fit(
        train_texts,
        train_labels,
    )

    predictions = pipeline.predict(
        test_texts
    )

    report = classification_report(
        test_labels,
        predictions,
        output_dict=True,
        zero_division=0,
    )

    classes = list(
        pipeline.named_steps[
            "classifier"
        ].classes_
    )

    matrix = confusion_matrix(
        test_labels,
        predictions,
        labels=classes,
    )

    confusion_matrix_frame = pd.DataFrame(
        matrix,
        index=classes,
        columns=classes,
    )

    metrics = {
        "accuracy": float(
            accuracy_score(
                test_labels,
                predictions,
            )
        ),
        "macro_f1": float(
            f1_score(
                test_labels,
                predictions,
                average="macro",
                zero_division=0,
            )
        ),
        "weighted_f1": float(
            f1_score(
                test_labels,
                predictions,
                average="weighted",
                zero_division=0,
            )
        ),
    }

    metadata = {
        "model_version": MODEL_VERSION,
        "model_type": "LogisticRegression",
        "text_features": "TfidfVectorizer",
        "training_data_source": TRAINING_DATA_SOURCE,
        "training_timestamp_utc": datetime.now(
            UTC
        ).isoformat(),
        "scikit_learn_version": sklearn.__version__,
        "random_state": random_state,
        "test_size": test_size,
        "review_threshold": DEFAULT_REVIEW_THRESHOLD,
        "total_records": int(len(records)),
        "training_records": int(len(train_texts)),
        "test_records": int(len(test_texts)),
        "classes": classes,
        "class_distribution": (
            records["category"]
            .value_counts()
            .sort_index()
            .to_dict()
        ),
        "metrics": metrics,
    }

    evaluation_report = {
        "metadata": metadata,
        "classification_report": report,
    }

    return (
        pipeline,
        evaluation_report,
        confusion_matrix_frame,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Train and evaluate the automotive issue classifier."
        )
    )

    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to the processed NHTSA training dataset.",
    )

    parser.add_argument(
        "--model-output",
        type=Path,
        default=DEFAULT_MODEL_PATH,
        help="Path for the fitted classification pipeline.",
    )

    parser.add_argument(
        "--metadata-output",
        type=Path,
        default=DEFAULT_METADATA_PATH,
        help="Path for model metadata used during inference.",
    )

    parser.add_argument(
        "--report-output",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Path for the full classification report.",
    )

    parser.add_argument(
        "--confusion-matrix-output",
        type=Path,
        default=DEFAULT_CONFUSION_MATRIX_PATH,
        help="Path for the confusion matrix CSV.",
    )

    parser.add_argument(
        "--test-size",
        type=float,
        default=0.20,
        help="Fraction of records reserved for evaluation.",
    )

    parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for reproducible train-test splitting.",
    )

    parser.add_argument(
        "--min-records-per-category",
        type=int,
        default=20,
        help=(
            "Minimum records required for a category "
            "to remain in the training dataset."
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not 0.0 < args.test_size < 1.0:
        raise ValueError(
            "--test-size must be between 0 and 1."
        )

    records = load_training_data(
        data_path=args.data,
        min_records_per_category=(
            args.min_records_per_category
        ),
    )

    print("Training dataset summary")
    print("------------------------")
    print(f"Records: {len(records):,}")
    print(f"Categories: {records['category'].nunique()}")
    print("\nClass distribution:")
    print(
        records["category"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    (
        pipeline,
        evaluation_report,
        confusion_matrix_frame,
    ) = train_and_evaluate(
        records=records,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    save_model(
        pipeline=pipeline,
        output_path=args.model_output,
    )

    save_json(
        data=evaluation_report["metadata"],
        output_path=args.metadata_output,
    )

    save_json(
        data=evaluation_report,
        output_path=args.report_output,
    )

    args.confusion_matrix_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    confusion_matrix_frame.to_csv(
        args.confusion_matrix_output,
    )

    metrics = evaluation_report[
        "metadata"
    ]["metrics"]

    print("\nEvaluation summary")
    print("------------------")
    print(
        f"Accuracy:    {metrics['accuracy']:.4f}"
    )
    print(
        f"Macro F1:    {metrics['macro_f1']:.4f}"
    )
    print(
        f"Weighted F1: {metrics['weighted_f1']:.4f}"
    )

    print(f"\nModel saved to: {args.model_output}")
    print(
        f"Metadata saved to: {args.metadata_output}"
    )
    print(
        f"Report saved to: {args.report_output}"
    )
    print(
        "Confusion matrix saved to: "
        f"{args.confusion_matrix_output}"
    )


if __name__ == "__main__":
    main()
    