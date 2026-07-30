from fastapi import FastAPI

from app.routes.classification import (
    router as classification_router,
)
from app.routes.health import (
    router as health_router,
)
from app.routes.retrieval import (
    router as retrieval_router,
)
from app.routes.regulations import (
    router as regulations_router,
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    application = FastAPI(
        title=(
            "Automotive After-Sales "
            "Service Assistant API"
        ),
        description=(
            "Backend prototype for natural-language "
            "automotive record retrieval, issue "
            "classification, and structured "
            "information extraction."
        ),
        version="0.5.0",
    )

    application.include_router(
        health_router
    )

    application.include_router(
        retrieval_router
    )

    application.include_router(
        classification_router
    )

    application.include_router(
        regulations_router
    )

    return application


app = create_app()
