from typing import Literal

from pydantic import BaseModel, Field


RetrievalMethod = Literal["tfidf", "semantic"]


class RetrievalRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Natural-language description of the vehicle issue.",
        examples=["My brakes make a squeaking noise at low speed."],
    )
    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of matching service records to return.",
    )
    method: RetrievalMethod = Field(
        default="tfidf",
        description="Retrieval method used to rank service records.",
    )


class RetrievalResult(BaseModel):
    record_id: str
    title: str
    description: str
    category: str
    component: str
    similarity_score: float


class RetrievalResponse(BaseModel):
    query: str
    method: RetrievalMethod
    result_count: int
    results: list[RetrievalResult]
    
    