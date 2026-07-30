from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from app.schemas.regulation import (
    RegulationComparisonSearchRequest,
    RegulationComparisonSearchResponse,
    RegulationSearchRequest,
    RegulationSearchResponse,
)
from app.services.regulation_semantic_search_service import (
    RegulationSemanticSearchService,
    get_regulation_semantic_search_service,
)


router = APIRouter(
    prefix="/regulations",
    tags=["Regulations"],
)


RegulationSearchServiceDependency = Annotated[
    RegulationSemanticSearchService,
    Depends(
        get_regulation_semantic_search_service
    ),
]


@router.post(
    "/search",
    response_model=RegulationSearchResponse,
    summary="Search verified regulations",
    description=(
        "Semantically search verified UNECE and United States "
        "regulation records. Results are informational and do "
        "not establish legal equivalence."
    ),
)
def search_regulations(
    request: RegulationSearchRequest,
    service: RegulationSearchServiceDependency,
) -> RegulationSearchResponse:
    results = service.search_regulations(
        query=request.query,
        top_k=request.top_k,
        jurisdiction=request.jurisdiction,
        regulatory_system=request.regulatory_system,
    )

    return RegulationSearchResponse(
        query=request.query,
        jurisdiction=request.jurisdiction,
        regulatory_system=request.regulatory_system,
        result_count=len(results),
        results=results,
    )


@router.post(
    "/comparisons/search",
    response_model=RegulationComparisonSearchResponse,
    summary="Search verified regulation comparisons",
    description=(
        "Semantically search the approved UNECE–FMVSS "
        "comparison pairs. Comparison results describe "
        "overlap and differences but never assert legal "
        "equivalence."
    ),
)
def search_regulation_comparisons(
    request: RegulationComparisonSearchRequest,
    service: RegulationSearchServiceDependency,
) -> RegulationComparisonSearchResponse:
    results = service.search_comparisons(
        query=request.query,
        top_k=request.top_k,
        regulatory_system=request.regulatory_system,
    )

    return RegulationComparisonSearchResponse(
        query=request.query,
        regulatory_system=request.regulatory_system,
        result_count=len(results),
        results=results,
    )
