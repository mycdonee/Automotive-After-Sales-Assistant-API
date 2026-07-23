from functools import lru_cache

from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from app.schemas.classification import (
    ClassificationRequest,
    ClassificationResponse,
)
from app.services.classification_service import (
    IssueClassificationService,
)


router = APIRouter(
    prefix="/classification",
    tags=["Classification"],
)


@lru_cache(maxsize=1)
def get_classification_service(
) -> IssueClassificationService:
    """Reuse the fitted classifier across API requests."""

    return IssueClassificationService()


@router.post(
    "/predict",
    response_model=ClassificationResponse,
    summary="Classify an automotive issue",
)
def predict_issue_category(
    request: ClassificationRequest,
) -> ClassificationResponse:
    try:
        service = (
            get_classification_service()
        )
    except (
        FileNotFoundError,
        ValueError,
    ) as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "The classification model "
                "is currently unavailable."
            ),
        ) from exc

    return service.predict(
        text=request.text,
        top_k=request.top_k,
    )
    