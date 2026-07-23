from functools import lru_cache
from pathlib import Path

from app.schemas.retrieval import (
    RetrievalDataset,
    RetrievalMethod,
)
from app.services.base_retrieval_service import (
    NHTSA_DATA_PATH,
    SYNTHETIC_DATA_PATH,
)
from app.services.retrieval_service import (
    TfidfRetrievalService,
)
from app.services.semantic_retrieval_service import (
    SemanticRetrievalService,
)


RetrievalService = (
    TfidfRetrievalService
    | SemanticRetrievalService
)


DATASET_CONFIG: dict[
    RetrievalDataset,
    tuple[Path, str],
] = {
    "synthetic": (
        SYNTHETIC_DATA_PATH,
        "Synthetic service records",
    ),
    "nhtsa": (
        NHTSA_DATA_PATH,
        "NHTSA Consumer Complaints",
    ),
}


@lru_cache(maxsize=4)
def get_retrieval_service(
    method: RetrievalMethod,
    dataset: RetrievalDataset,
) -> RetrievalService:
    """Create one reusable service for each method and dataset pair."""

    data_path, default_source = DATASET_CONFIG[dataset]

    if method == "semantic":
        return SemanticRetrievalService(
            data_path=data_path,
            default_source=default_source,
        )

    return TfidfRetrievalService(
        data_path=data_path,
        default_source=default_source,
    )
    