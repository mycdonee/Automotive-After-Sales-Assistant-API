from functools import lru_cache
from pathlib import Path

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.retrieval import (
    RetrievalFilters,
    RetrievalResult,
)
from app.services.base_retrieval_service import (
    DEFAULT_DATA_PATH,
    BaseRetrievalService,
)


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=2)
def load_embedding_model(
    model_name: str,
) -> SentenceTransformer:
    """Load each embedding model once and reuse it across datasets."""

    return SentenceTransformer(model_name)


class SemanticRetrievalService(BaseRetrievalService):
    """Retrieve automotive records using sentence embeddings."""

    def __init__(
        self,
        data_path: Path = DEFAULT_DATA_PATH,
        default_source: str = "Synthetic service records",
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        super().__init__(
            data_path=data_path,
            default_source=default_source,
        )

        self.model_name = model_name

        # The model is shared instead of loaded again for each dataset.
        self.model = load_embedding_model(
            self.model_name
        )

        # Each dataset keeps its own cached document embeddings.
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
            candidate_indices=candidate_indices,
            top_k=top_k,
        )
        