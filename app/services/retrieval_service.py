from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.retrieval import (
    RetrievalFilters,
    RetrievalResult,
)
from app.services.base_retrieval_service import (
    DEFAULT_DATA_PATH,
    BaseRetrievalService,
)


class TfidfRetrievalService(BaseRetrievalService):
    """Retrieve automotive records using TF-IDF similarity."""

    def __init__(
        self,
        data_path: Path = DEFAULT_DATA_PATH,
        default_source: str = "Synthetic service records",
    ) -> None:
        super().__init__(
            data_path=data_path,
            default_source=default_source,
        )

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )

        # The document matrix is built once and reused for every request.
        self.document_matrix = self.vectorizer.fit_transform(
            self.search_documents
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
        filters: RetrievalFilters | None = None,
    ) -> list[RetrievalResult]:
        normalized_query = query.strip()

        if not normalized_query:
            return []

        candidate_indices = self._get_candidate_indices(
            filters
        )

        if candidate_indices.size == 0:
            return []

        query_vector = self.vectorizer.transform(
            [normalized_query]
        )

        similarities = cosine_similarity(
            query_vector,
            self.document_matrix,
        ).flatten()

        return self._build_results(
            similarities=similarities,
            candidate_indices=candidate_indices,
            top_k=top_k,
        )
        