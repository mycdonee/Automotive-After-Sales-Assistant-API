from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.retrieval import RetrievalResult
from app.services.base_retrieval_service import (
    DEFAULT_DATA_PATH,
    BaseRetrievalService,
)


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class SemanticRetrievalService(BaseRetrievalService):
    """Retrieve service records using sentence embeddings."""

    def __init__(
        self,
        data_path: Path = DEFAULT_DATA_PATH,
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        super().__init__(data_path=data_path)

        self.model_name = model_name

        # Load the embedding model once for repeated search requests.
        self.model = SentenceTransformer(self.model_name)

        # Cache document embeddings instead of recomputing them per request.
        self.document_embeddings = self.model.encode(
            self.search_documents,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

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

        return self._build_results(
            similarities=similarities,
            top_k=top_k,
        )
        