from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from sklearn.pipeline import Pipeline

from app.schemas.classification import (
    CategoryPrediction,
    ClassificationResponse,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

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


class IssueClassificationService:
    """Classify automotive issue descriptions with a saved pipeline."""

    def __init__(
        self,
        model_path: Path = DEFAULT_MODEL_PATH,
        metadata_path: Path = DEFAULT_METADATA_PATH,
    ) -> None:
        self.model_path = model_path
        self.metadata_path = metadata_path

        self.pipeline = self._load_pipeline()
        self.metadata = self._load_metadata()

        classifier = self.pipeline.named_steps.get(
            "classifier"
        )

        if classifier is None or not hasattr(
            classifier,
            "classes_",
        ):
            raise ValueError(
                "The saved classification pipeline "
                "does not contain fitted class labels."
            )

        self.classes = np.asarray(
            classifier.classes_
        )

        self.review_threshold = float(
            self.metadata.get(
                "review_threshold",
                0.60,
            )
        )

    def _load_pipeline(self) -> Pipeline:
        """Load the fitted vectorizer and classifier as one artifact."""

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Classification model not found: {self.model_path}"
            )

        pipeline = joblib.load(
            self.model_path
        )

        if not isinstance(
            pipeline,
            Pipeline,
        ):
            raise ValueError(
                "The classification artifact "
                "is not a scikit-learn Pipeline."
            )

        return pipeline

    def _load_metadata(
        self,
    ) -> dict[str, Any]:
        """Load version and training information for API responses."""

        if not self.metadata_path.exists():
            raise FileNotFoundError(
                "Classification metadata not found: "
                f"{self.metadata_path}"
            )

        with self.metadata_path.open(
            "r",
            encoding="utf-8",
        ) as metadata_file:
            metadata = json.load(
                metadata_file
            )

        required_fields = {
            "model_version",
            "training_data_source",
        }

        missing_fields = required_fields.difference(
            metadata
        )

        if missing_fields:
            missing = ", ".join(
                sorted(missing_fields)
            )
            raise ValueError(
                "Classification metadata is missing: "
                f"{missing}"
            )

        return metadata

    def predict(
        self,
        text: str,
        top_k: int = 3,
    ) -> ClassificationResponse:
        normalized_text = text.strip()

        probabilities = (
            self.pipeline.predict_proba(
                [normalized_text]
            )[0]
        )

        ranked_indices = (
            probabilities
            .argsort()[::-1][:top_k]
        )

        top_predictions = [
            CategoryPrediction(
                category=str(
                    self.classes[index]
                ),
                probability=round(
                    float(
                        probabilities[index]
                    ),
                    4,
                ),
            )
            for index in ranked_indices
        ]

        best_prediction = top_predictions[0]

        # Low-confidence predictions are flagged for human review rather
        # than being treated as reliable automatic classifications.
        review_required = (
            best_prediction.probability
            < self.review_threshold
        )

        return ClassificationResponse(
            predicted_category=(
                best_prediction.category
            ),
            confidence=(
                best_prediction.probability
            ),
            review_required=review_required,
            model_version=str(
                self.metadata[
                    "model_version"
                ]
            ),
            training_data_source=str(
                self.metadata[
                    "training_data_source"
                ]
            ),
            top_predictions=top_predictions,
        )
        