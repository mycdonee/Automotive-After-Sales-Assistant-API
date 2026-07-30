from __future__ import annotations

from functools import lru_cache
from typing import Protocol

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas.regulation import (
    Jurisdiction,
    RegulationComparisonSearchResult,
    RegulationDataset,
    RegulationSearchResult,
    RegulatorySystem,
)
from app.services.regulation_data_loader import (
    get_regulation_dataset,
)
from app.services.semantic_retrieval_service import (
    DEFAULT_MODEL_NAME,
    load_embedding_model,
)


class EmbeddingModel(Protocol):
    """Minimal interface required from an embedding model."""

    def encode(
        self,
        sentences: list[str] | tuple[str, ...],
        *,
        convert_to_numpy: bool,
        normalize_embeddings: bool,
        show_progress_bar: bool,
    ) -> np.ndarray:
        ...


class RegulationSemanticSearchService:
    """Search verified regulations and comparison pairs semantically."""

    def __init__(
        self,
        dataset: RegulationDataset | None = None,
        model_name: str = DEFAULT_MODEL_NAME,
        model: EmbeddingModel | None = None,
    ) -> None:
        self.dataset = (
            dataset
            if dataset is not None
            else get_regulation_dataset()
        )

        self.model_name = model_name

        self.model = (
            model
            if model is not None
            else load_embedding_model(model_name)
        )

        self.record_by_id = {
            record.regulation_id: record
            for record in self.dataset.records
        }

        self.regulation_embeddings = (
            self._encode_documents(
                self.dataset.regulation_search_documents
            )
        )

        self.comparison_embeddings = (
            self._encode_documents(
                self.dataset.comparison_search_documents
            )
        )

    def _encode_documents(
        self,
        documents: tuple[str, ...],
    ) -> np.ndarray:
        embeddings = np.asarray(
            self.model.encode(
                documents,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            ),
            dtype=float,
        )

        if embeddings.ndim != 2:
            raise ValueError(
                "Document embeddings must be a two-dimensional array."
            )

        if embeddings.shape[0] != len(documents):
            raise ValueError(
                "Document embedding count does not match "
                "the document count."
            )

        return embeddings

    def _encode_query(
        self,
        query: str,
    ) -> np.ndarray:
        embeddings = np.asarray(
            self.model.encode(
                [query],
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            ),
            dtype=float,
        )

        if (
            embeddings.ndim != 2
            or embeddings.shape[0] != 1
        ):
            raise ValueError(
                "Query embedding must contain exactly one vector."
            )

        return embeddings

    @staticmethod
    def _validate_top_k(
        top_k: int,
    ) -> None:
        if top_k < 1:
            raise ValueError(
                "top_k must be at least 1."
            )

    def _rank_candidate_indices(
        self,
        query: str,
        document_embeddings: np.ndarray,
        candidate_indices: np.ndarray,
        top_k: int,
    ) -> list[tuple[int, float]]:
        normalized_query = query.strip()

        if not normalized_query:
            return []

        self._validate_top_k(top_k)

        if candidate_indices.size == 0:
            return []

        query_embedding = self._encode_query(
            normalized_query
        )

        similarities = cosine_similarity(
            query_embedding,
            document_embeddings,
        ).flatten()

        candidate_scores = similarities[
            candidate_indices
        ]

        ranked_positions = (
            candidate_scores
            .argsort()[::-1][:top_k]
        )

        return [
            (
                int(candidate_indices[position]),
                float(candidate_scores[position]),
            )
            for position in ranked_positions
        ]

    def search_regulations(
        self,
        query: str,
        top_k: int = 5,
        jurisdiction: Jurisdiction | None = None,
        regulatory_system: RegulatorySystem | None = None,
    ) -> list[RegulationSearchResult]:
        """Search individual regulation records."""

        candidate_indices = np.array(
            [
                index
                for index, record in enumerate(
                    self.dataset.records
                )
                if (
                    jurisdiction is None
                    or record.jurisdiction
                    == jurisdiction
                )
                and (
                    regulatory_system is None
                    or record.regulatory_system
                    == regulatory_system
                )
            ],
            dtype=int,
        )

        ranked = self._rank_candidate_indices(
            query=query,
            document_embeddings=(
                self.regulation_embeddings
            ),
            candidate_indices=candidate_indices,
            top_k=top_k,
        )

        results: list[
            RegulationSearchResult
        ] = []

        for index, score in ranked:
            record = self.dataset.records[index]

            results.append(
                RegulationSearchResult(
                    regulation_id=record.regulation_id,
                    official_identifier=(
                        record.official_identifier
                    ),
                    title=record.title,
                    jurisdiction=record.jurisdiction,
                    regulatory_system=(
                        record.regulatory_system
                    ),
                    regulated_object=(
                        record.regulated_object
                    ),
                    scope_summary=record.scope_summary,
                    reviewed_version=(
                        record.reviewed_version
                    ),
                    similarity_score=round(
                        score,
                        4,
                    ),
                )
            )

        return results

    def search_comparisons(
        self,
        query: str,
        top_k: int = 5,
        regulatory_system: RegulatorySystem | None = None,
    ) -> list[
        RegulationComparisonSearchResult
    ]:
        """Search verified UNECE–FMVSS comparison pairs."""

        candidate_indices = np.array(
            [
                index
                for index, pair in enumerate(
                    self.dataset.comparison_pairs
                )
                if (
                    regulatory_system is None
                    or pair.regulatory_system
                    == regulatory_system
                )
            ],
            dtype=int,
        )

        ranked = self._rank_candidate_indices(
            query=query,
            document_embeddings=(
                self.comparison_embeddings
            ),
            candidate_indices=candidate_indices,
            top_k=top_k,
        )

        results: list[
            RegulationComparisonSearchResult
        ] = []

        for index, score in ranked:
            pair = self.dataset.comparison_pairs[
                index
            ]

            left_record = self.record_by_id[
                pair.left_regulation_id
            ]

            right_record = self.record_by_id[
                pair.right_regulation_id
            ]

            results.append(
                RegulationComparisonSearchResult(
                    pair_id=pair.pair_id,
                    pair_number=pair.pair_number,
                    left_regulation_id=(
                        pair.left_regulation_id
                    ),
                    right_regulation_id=(
                        pair.right_regulation_id
                    ),
                    left_official_identifier=(
                        left_record.official_identifier
                    ),
                    right_official_identifier=(
                        right_record.official_identifier
                    ),
                    regulatory_system=(
                        pair.regulatory_system
                    ),
                    comparison_focus=(
                        pair.comparison_focus
                    ),
                    comparison_level=(
                        pair.comparison_level
                    ),
                    overlap_summary=(
                        pair.overlap_summary
                    ),
                    legal_equivalence=(
                        pair.legal_equivalence
                    ),
                    similarity_score=round(
                        score,
                        4,
                    ),
                )
            )

        return results


@lru_cache(maxsize=1)
def get_regulation_semantic_search_service(
) -> RegulationSemanticSearchService:
    """Create and cache the regulation search service."""

    return RegulationSemanticSearchService()
