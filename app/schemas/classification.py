from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class ClassificationRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    text: str = Field(
        ...,
        min_length=10,
        max_length=5_000,
        description=(
            "Natural-language description of an automotive issue."
        ),
        examples=[
            (
                "The brake pedal became hard and "
                "the vehicle could not stop."
            )
        ],
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=5,
        description=(
            "Number of category predictions returned."
        ),
    )

    @field_validator("text")
    @classmethod
    def validate_text(
        cls,
        value: str,
    ) -> str:
        normalized_text = value.strip()

        if len(normalized_text) < 10:
            raise ValueError(
                "Text must contain at least ten "
                "non-whitespace characters."
            )

        return normalized_text


class CategoryPrediction(BaseModel):
    category: str
    probability: float


class ClassificationResponse(BaseModel):
    predicted_category: str
    confidence: float
    review_required: bool
    model_version: str
    training_data_source: str
    top_predictions: list[
        CategoryPrediction
    ]
    