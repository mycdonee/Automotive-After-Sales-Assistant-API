from fastapi import APIRouter, Depends

from app.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
)
from app.services.retrieval_service import TfidfRetrievalService


router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


_retrieval_service = TfidfRetrievalService()


def get_retrieval_service() -> TfidfRetrievalService:
    return _retrieval_service


@router.post(
    "/search",
    response_model=RetrievalResponse,
    summary="Search automotive service records",
)
def search_service_records(
    request: RetrievalRequest,
    service: TfidfRetrievalService = Depends(
        get_retrieval_service
    ),
) -> RetrievalResponse:
    results = service.search(
        query=request.query,
        top_k=request.top_k,
    )

    return RetrievalResponse(
        query=request.query,
        method=request.method,
        result_count=len(results),
        results=results,
    )
    
    