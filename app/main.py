from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.retrieval import router as retrieval_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    application = FastAPI(
        title="Automotive After-Sales Service Assistant API",
        description=(
            "Backend prototype for automotive service text retrieval, "
            "issue classification, and structured information extraction."
        ),
        version="0.2.0",
    )

    application.include_router(health_router)
    application.include_router(retrieval_router)

    return application


app = create_app()

