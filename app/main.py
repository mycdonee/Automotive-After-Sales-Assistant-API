from fastapi import FastAPI

from app.routes.health import router as health_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    application = FastAPI(
        title="Automotive After-Sales Service Assistant API",
        description=(
            "Backend prototype for automotive service text retrieval, "
            "issue classification, and structured information extraction."
        ),
        version="0.1.0",
    )

    application.include_router(health_router)

    return application


app = create_app()