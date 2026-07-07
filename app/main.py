from fastapi import FastAPI

app = FastAPI(
    title="Automotive After-Sales Service Assistant API",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return the current API health status."""
    return {"status": "ok"}
