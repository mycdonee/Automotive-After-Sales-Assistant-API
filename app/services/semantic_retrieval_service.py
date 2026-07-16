from pathlib import Path

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.retrieval import RetrievalResult


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "service_records.csv"
DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class SemanticRetrievalService:
    """Retrieve service records using sentence embeddings."""

    REQUIRED_COLUMNS = {
        "record_id",
        "title",
        "description",
        "category",
        "component",
    }

    def __init__(
        self,
        data_path: Path = DEFAULT_DATA_PATH,
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        self.data_path = data_path
        self.model_name = model_name
        self.records = self._load_records()

        # Combine searchable fields into one text representation.
        self.search_documents = (
            self.records["title"].fillna("")
            + ". "
            + self.records["description"].fillna("")
            + ". Category: "
            + self.records["category"].fillna("")
            + ". Component: "
            + self.records["component"].fillna("")
        ).tolist()

        # The model is loaded once when the service is created.
        self.model = SentenceTransformer(self.model_name)

        # Document embeddings are also computed only once.
        self.document_embeddings = self.model.encode(
            self.search_documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
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

        query_embedding = self.model.encode(
            [normalized_query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        similarities = cosine_similarity(
            query_embedding,
            self.document_embeddings,
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
    
    