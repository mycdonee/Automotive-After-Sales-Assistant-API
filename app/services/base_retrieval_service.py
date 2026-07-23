from pathlib import Path

import numpy as np
import pandas as pd

from app.schemas.retrieval import (
    RetrievalFilters,
    RetrievalResult,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SYNTHETIC_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "service_records.csv"
)

NHTSA_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nhtsa_service_records.csv"
)

DEFAULT_DATA_PATH = SYNTHETIC_DATA_PATH


class BaseRetrievalService:
    """Provide shared data loading, filtering, and result formatting."""

    REQUIRED_COLUMNS = {
        "record_id",
        "title",
        "description",
        "category",
        "component",
    }

    OPTIONAL_COLUMNS = (
        "source",
        "make",
        "model",
        "model_year",
        "received_date",
    )

    def __init__(
        self,
        data_path: Path = DEFAULT_DATA_PATH,
        default_source: str = "Synthetic service records",
    ) -> None:
        self.data_path = data_path
        self.default_source = default_source
        self.records = self._load_records()
        self.search_documents = self._build_search_documents()

    def _load_records(self) -> pd.DataFrame:
        """Load the selected dataset and normalize its optional fields."""

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Retrieval dataset not found: {self.data_path}"
            )

        records = pd.read_csv(
            self.data_path,
            dtype=str,
            keep_default_na=False,
        )

        missing_columns = self.REQUIRED_COLUMNS.difference(
            records.columns
        )

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(
                f"Dataset is missing required columns: {missing}"
            )

        if records.empty:
            raise ValueError("Retrieval dataset must not be empty.")

        # Both datasets use one internal schema, even when metadata is absent.
        for column in self.OPTIONAL_COLUMNS:
            if column not in records.columns:
                records[column] = ""

        records["source"] = records["source"].replace(
            "",
            self.default_source,
        )

        return records.reset_index(drop=True)

    def _build_search_documents(self) -> list[str]:
        """Combine text and metadata into one searchable representation."""

        vehicle_context = (
            self.records["make"]
            + " "
            + self.records["model"]
            + " "
            + self.records["model_year"]
        ).str.strip()

        return (
            self.records["title"]
            + ". "
            + self.records["description"]
            + ". Category: "
            + self.records["category"]
            + ". Component: "
            + self.records["component"]
            + ". Vehicle: "
            + vehicle_context
        ).tolist()

    def _get_candidate_indices(
        self,
        filters: RetrievalFilters | None,
    ) -> np.ndarray:
        """Return row indices that satisfy all requested metadata filters."""

        if filters is None:
            return np.arange(
                len(self.records),
                dtype=int,
            )

        filter_values = filters.model_dump(
            exclude_none=True
        )

        if not filter_values:
            return np.arange(
                len(self.records),
                dtype=int,
            )

        mask = pd.Series(
            True,
            index=self.records.index,
        )

        for field, requested_value in filter_values.items():
            normalized_value = (
                str(requested_value)
                .strip()
                .casefold()
            )

            normalized_column = (
                self.records[field]
                .astype(str)
                .str.strip()
                .str.casefold()
            )

            mask &= normalized_column.eq(normalized_value)

        return np.flatnonzero(
            mask.to_numpy()
        )

    @staticmethod
    def _optional_value(
        record: pd.Series,
        field: str,
    ) -> str | None:
        value = str(record[field]).strip()

        return value or None

    def _build_results(
        self,
        similarities: np.ndarray,
        candidate_indices: np.ndarray,
        top_k: int,
    ) -> list[RetrievalResult]:
        """Rank eligible records and convert them into response models."""

        if candidate_indices.size == 0:
            return []

        candidate_scores = similarities[candidate_indices]

        ranked_positions = (
            candidate_scores
            .argsort()[::-1][:top_k]
        )

        ranked_indices = candidate_indices[
            ranked_positions
        ]

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
                    source=str(record["source"]),
                    make=self._optional_value(
                        record,
                        "make",
                    ),
                    model=self._optional_value(
                        record,
                        "model",
                    ),
                    model_year=self._optional_value(
                        record,
                        "model_year",
                    ),
                    received_date=self._optional_value(
                        record,
                        "received_date",
                    ),
                    similarity_score=round(
                        float(similarities[index]),
                        4,
                    ),
                )
            )

        return results
    