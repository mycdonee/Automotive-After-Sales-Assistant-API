import numpy as np
import pytest

from app.services.regulation_semantic_search_service import (
    RegulationSemanticSearchService,
)


class KeywordEmbeddingModel:
    """Provide deterministic embeddings without loading a real model."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, ...]] = []

    def encode(
        self,
        sentences: list[str] | tuple[str, ...],
        *,
        convert_to_numpy: bool,
        normalize_embeddings: bool,
        show_progress_bar: bool,
    ) -> np.ndarray:
        assert convert_to_numpy is True
        assert normalize_embeddings is True
        assert show_progress_bar is False

        texts = tuple(sentences)
        self.calls.append(texts)

        return np.asarray(
            [
                self._vectorize(text)
                for text in texts
            ],
            dtype=float,
        )

    @staticmethod
    def _vectorize(
        text: str,
    ) -> np.ndarray:
        normalized = text.casefold()

        warning_phrases = (
            "advance warning",
            "warning triangle",
            "warning triangles",
            "equilateral-triangle",
            "equilateral triangle",
            "warning device",
        )

        vector = np.asarray(
            [
                float(
                    "un r27" in normalized
                    or "un regulation no. 27"
                    in normalized
                ),
                float(
                    "fmvss 125" in normalized
                    or "fmvss no. 125"
                    in normalized
                ),
                5.0
                * sum(
                    phrase in normalized
                    for phrase in warning_phrases
                ),
                float(
                    "brak" in normalized
                    or "stability control"
                    in normalized
                ),
                float(
                    "seat belt" in normalized
                    or "child restraint"
                    in normalized
                    or "anchorages"
                    in normalized
                ),
                float(
                    "lighting" in normalized
                    or "lamp" in normalized
                    or "retro-reflect"
                    in normalized
                    or "conspicuity"
                    in normalized
                ),
            ],
            dtype=float,
        )

        if not vector.any():
            vector[-1] = 0.001

        norm = np.linalg.norm(vector)

        return vector / norm


class InvalidEmbeddingModel:
    """Return an invalid one-dimensional embedding array."""

    def encode(
        self,
        sentences: list[str] | tuple[str, ...],
        *,
        convert_to_numpy: bool,
        normalize_embeddings: bool,
        show_progress_bar: bool,
    ) -> np.ndarray:
        return np.asarray(
            [1.0, 0.0],
            dtype=float,
        )


def test_service_precomputes_document_embeddings_once() -> None:
    model = KeywordEmbeddingModel()

    service = RegulationSemanticSearchService(
        model=model
    )

    assert len(model.calls) == 2
    assert len(model.calls[0]) == 18
    assert len(model.calls[1]) == 11

    assert service.regulation_embeddings.shape == (
        18,
        6,
    )

    assert service.comparison_embeddings.shape == (
        11,
        6,
    )


def test_search_regulations_ranks_warning_triangle_records() -> None:
    service = RegulationSemanticSearchService(
        model=KeywordEmbeddingModel()
    )

    results = service.search_regulations(
        query=(
            "UN R27 and FMVSS 125 advance "
            "warning triangle requirements"
        ),
        top_k=3,
    )

    top_ids = {
        result.regulation_id
        for result in results[:2]
    }

    assert top_ids == {
        "unece_r27",
        "fmvss_125",
    }

    for result in results:
        assert result.result_type == "regulation"
        assert -1.0 <= result.similarity_score <= 1.0


def test_search_regulations_applies_metadata_filters() -> None:
    service = RegulationSemanticSearchService(
        model=KeywordEmbeddingModel()
    )

    results = service.search_regulations(
        query="braking and stability control",
        top_k=10,
        jurisdiction="UNECE",
        regulatory_system="braking_and_stability",
    )

    assert {
        result.regulation_id
        for result in results
    } == {
        "unece_r13h",
        "unece_r140",
    }

    assert all(
        result.jurisdiction == "UNECE"
        for result in results
    )

    assert all(
        result.regulatory_system
        == "braking_and_stability"
        for result in results
    )


def test_search_comparisons_ranks_warning_triangle_pair() -> None:
    service = RegulationSemanticSearchService(
        model=KeywordEmbeddingModel()
    )

    results = service.search_comparisons(
        query=(
            "compare UN R27 and FMVSS 125 "
            "advance warning triangle requirements"
        ),
        top_k=3,
    )

    first_result = results[0]

    assert (
        first_result.pair_id
        == "unece_r27__fmvss_125"
    )

    assert (
        first_result.comparison_focus
        == "portable_advance_warning_triangle_performance"
    )

    assert first_result.result_type == "comparison"
    assert first_result.legal_equivalence is False


def test_search_comparisons_applies_system_filter() -> None:
    service = RegulationSemanticSearchService(
        model=KeywordEmbeddingModel()
    )

    results = service.search_comparisons(
        query="seat belt and child restraint anchorages",
        top_k=10,
        regulatory_system="occupant_restraint",
    )

    assert {
        result.pair_id
        for result in results
    } == {
        "unece_r14__fmvss_210",
        "unece_r16__fmvss_209",
        "unece_r145__fmvss_225",
    }

    assert all(
        result.regulatory_system
        == "occupant_restraint"
        for result in results
    )


def test_empty_query_returns_no_results_without_encoding() -> None:
    model = KeywordEmbeddingModel()

    service = RegulationSemanticSearchService(
        model=model
    )

    calls_before_search = len(model.calls)

    assert (
        service.search_regulations(
            query="   ",
        )
        == []
    )

    assert (
        service.search_comparisons(
            query="\n\t",
        )
        == []
    )

    assert len(model.calls) == calls_before_search


def test_invalid_top_k_is_rejected() -> None:
    service = RegulationSemanticSearchService(
        model=KeywordEmbeddingModel()
    )

    with pytest.raises(
        ValueError,
        match="top_k must be at least 1",
    ):
        service.search_regulations(
            query="braking requirements",
            top_k=0,
        )

    with pytest.raises(
        ValueError,
        match="top_k must be at least 1",
    ):
        service.search_comparisons(
            query="lighting comparison",
            top_k=-1,
        )


def test_invalid_document_embedding_shape_is_rejected() -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Document embeddings must be "
            "a two-dimensional array"
        ),
    ):
        RegulationSemanticSearchService(
            model=InvalidEmbeddingModel()
        )
