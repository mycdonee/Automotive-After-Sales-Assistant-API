from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
)
from app.services.retrieval_registry import (
    get_retrieval_service,
)


router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


@router.post(
    "/search",
    response_model=RetrievalResponse,
    response_model_exclude_none=True,
    summary="Search automotive records",
)
def search_service_records(
    request: RetrievalRequest,
) -> RetrievalResponse:
    try:
        service = get_retrieval_service(
            method=request.method,
            dataset=request.dataset,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                f"The '{request.dataset}' retrieval dataset "
                "is currently unavailable."
            ),
        ) from exc

    results = service.search(
        query=request.query,
        top_k=request.top_k,
        filters=request.filters,
    )

    return RetrievalResponse(
        query=request.query,
        method=request.method,
        dataset=request.dataset,
        applied_filters=request.filters,
        result_count=len(results),
        results=results,
    )
    