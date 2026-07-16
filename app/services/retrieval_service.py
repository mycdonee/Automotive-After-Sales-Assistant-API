from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.retrieval import RetrievalResult


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "service_records.csv"


class TfidfRetrievalService:
    """Retrieve automotive service records using TF-IDF similarity."""

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

        self.search_documents = (
            self.records["title"].fillna("")
            + " "
            + self.records["description"].fillna("")
            + " "
            + self.records["category"].fillna("")
            + " "
            + self.records["component"].fillna("")
        ).tolist()

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )

        self.document_matrix = self.vectorizer.fit_transform(
            self.search_documents
        )

    def _load_records(self) -> pd.DataFrame:
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

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievalResult]:
        normalized_query = query.strip()

        if not normalized_query:
            return []

        query_vector = self.vectorizer.transform([normalized_query])

        similarities = cosine_similarity(
            query_vector,
            self.document_matrix,
        ).flatten()

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
    
    