from pathlib import Path

import numpy as np
import pandas as pd

from app.schemas.retrieval import RetrievalResult


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "service_records.csv"


class BaseRetrievalService:
    """Provide shared data loading and result formatting logic."""

    REQUIRED_COLUMNS = {
        "record_id",
        "title",
        "description",
        "category",
        "component",
    }

    def __init__(self, data_path: Path = DEFAULT_DATA_PATH) -> None:
        self.data_path = data_path
        self.records = self._load_records()
        self.search_documents = self._build_search_documents()

    def _load_records(self) -> pd.DataFrame:
        """Load and validate the service-record dataset."""

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Service-record dataset not found: {self.data_path}"
            )

        records = pd.read_csv(self.data_path)

        missing_columns = self.REQUIRED_COLUMNS.difference(records.columns)

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(
                f"Dataset is missing required columns: {missing}"
            )

        if records.empty:
            raise ValueError("Service-record dataset must not be empty.")

        return records

    def _build_search_documents(self) -> list[str]:
        """Combine relevant fields into one searchable document per record."""

        return (
            self.records["title"].fillna("")
            + ". "
            + self.records["description"].fillna("")
            + ". Category: "
            + self.records["category"].fillna("")
            + ". Component: "
            + self.records["component"].fillna("")
        ).tolist()

    def _build_results(
        self,
        similarities: np.ndarray,
        top_k: int,
    ) -> list[RetrievalResult]:
        """Rank similarity scores and convert rows into response models."""

        ranked_indices = similarities.argsort()[::-1][:top_k]

        results: list[RetrievalResult] = []

        for index in ranked_indices:
            record = self.records.iloc[index]

            results.append(
                RetrievalResult(
                    record_id=str(record["record_id"]),
                    title=str(record["title"]),
                    description=str(record["description"]),
                    category=str(record["category"]),
                    component=str(record["component"]),
                    similarity_score=round(
                        float(similarities[index]),
                        4,
                    ),
                )
            )

        return results
    