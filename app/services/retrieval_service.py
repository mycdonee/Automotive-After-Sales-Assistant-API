from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.retrieval import RetrievalResult
from app.services.base_retrieval_service import (
    DEFAULT_DATA_PATH,
    BaseRetrievalService,
)


class TfidfRetrievalService(BaseRetrievalService):
    """Retrieve service records using TF-IDF similarity."""

    def __init__(self, data_path: Path = DEFAULT_DATA_PATH) -> None:
        super().__init__(data_path=data_path)

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
        )

        # Build the searchable document matrix once during initialization.
        self.document_matrix = self.vectorizer.fit_transform(
            self.search_documents
        )

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

        return self._build_results(
            similarities=similarities,
            top_k=top_k,
        )
        
        