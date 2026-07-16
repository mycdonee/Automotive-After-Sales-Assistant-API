from fastapi import APIRouter, Depends

from app.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
    RetrievalResult,
)
from app.services.retrieval_service import TfidfRetrievalService
from app.services.semantic_retrieval_service import (
    SemanticRetrievalService,
)


router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


_tfidf_service = TfidfRetrievalService()
_semantic_service: SemanticRetrievalService | None = None


def get_tfidf_service() -> TfidfRetrievalService:
    return _tfidf_service


def get_semantic_service() -> SemanticRetrievalService:
    global _semantic_service

    # Load the transformer model only when semantic search is first used.
    if _semantic_service is None:
        _semantic_service = SemanticRetrievalService()

    return _semantic_service


@router.post(
    "/search",
    response_model=RetrievalResponse,
    summary="Search automotive service records",
)
def search_service_records(
    request: RetrievalRequest,
    tfidf_service: TfidfRetrievalService = Depends(
        get_tfidf_service
    ),
) -> RetrievalResponse:
    results: list[RetrievalResult]

    if request.method == "semantic":
        semantic_service = get_semantic_service()
        results = semantic_service.search(
            query=request.query,
            top_k=request.top_k,
        )
    else:
        results = tfidf_service.search(
            query=request.query,
            top_k=request.top_k,
        )

    return RetrievalResponse(
        query=request.query,
        method=request.method,
        result_count=len(results),
        results=results,
    )
    
    