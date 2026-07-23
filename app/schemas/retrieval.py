from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


RetrievalMethod = Literal["tfidf", "semantic"]
RetrievalDataset = Literal["synthetic", "nhtsa"]


class RetrievalFilters(BaseModel):
    """Optional metadata filters applied before result ranking."""

    model_config = ConfigDict(extra="forbid")

    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Broad automotive issue category.",
        examples=["Braking System"],
    )
    make: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Vehicle manufacturer.",
        examples=["FORD"],
    )
    model: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Vehicle model.",
        examples=["F-150"],
    )
    model_year: int | None = Field(
        default=None,
        ge=1900,
        le=2100,
        description="Vehicle model year.",
        examples=[2024],
    )


class RetrievalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Natural-language description of the vehicle issue.",
        examples=["The vehicle takes much longer to stop."],
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of matching records to return.",
    )
    method: RetrievalMethod = Field(
        default="tfidf",
        description="Retrieval method used to rank records.",
    )
    dataset: RetrievalDataset = Field(
        default="synthetic",
        description="Dataset searched by the retrieval service.",
    )
    filters: RetrievalFilters | None = Field(
        default=None,
        description="Optional metadata filters for the selected dataset.",
    )

    @field_validator("query")
    @classmethod
    def validate_query(cls, value: str) -> str:
        normalized_query = value.strip()

        if len(normalized_query) < 3:
            raise ValueError(
                "Query must contain at least three non-whitespace characters."
            )

        return normalized_query


class RetrievalResult(BaseModel):
    record_id: str
    title: str
    description: str
    category: str
    component: str
    source: str
    make: str | None = None
    model: str | None = None
    model_year: str | None = None
    received_date: str | None = None
    similarity_score: float


class RetrievalResponse(BaseModel):
    query: str
    method: RetrievalMethod
    dataset: RetrievalDataset
    applied_filters: RetrievalFilters | None = None
    result_count: int
    results: list[RetrievalResult]
    