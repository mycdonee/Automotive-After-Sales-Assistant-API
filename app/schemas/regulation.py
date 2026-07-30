from datetime import date
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


NonEmptyText = Annotated[
    str,
    Field(min_length=1),
]

Jurisdiction = Literal[
    "UNECE",
    "United States",
]

RegulatorySystem = Literal[
    "braking_and_stability",
    "occupant_restraint",
    "lighting_and_light_signalling",
]

SourceFormat = Literal[
    "pdf",
    "xml",
    "mixed",
]

ComparisonStatus = Literal[
    "approved",
    "rejected",
    "pending",
]

ComparisonLevel = Literal[
    "direct",
    "partial",
    "system_level",
]

ComparisonFocus = Literal[
    "light_vehicle_braking",
    "electronic_stability_control",
    "seat_belt_anchorages",
    "seat_belt_assemblies",
    "child_restraint_anchorages",
    "vehicle_lighting_installation",
    "light_signalling_device_performance",
    "road_illumination_device_performance",
    "retro_reflective_device_performance",
    "vehicle_conspicuity_marking_requirements",
    "portable_advance_warning_triangle_performance",
]


def _validate_unique_values(
    values: tuple[str, ...],
) -> tuple[str, ...]:
    if len(values) != len(set(values)):
        raise ValueError(
            "Collection values must be unique."
        )

    return values


class RegulationRecord(BaseModel):
    """Validated runtime representation of one regulation."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    schema_version: Literal["1.0"]

    regulation_id: str = Field(
        pattern=r"^(unece|fmvss)_[a-z0-9]+$",
    )

    jurisdiction: Jurisdiction
    authority: NonEmptyText
    official_identifier: NonEmptyText

    aliases: tuple[
        NonEmptyText,
        ...,
    ] = Field(
        min_length=1,
    )

    title: NonEmptyText
    citation: NonEmptyText
    regulatory_system: RegulatorySystem
    regulated_object: NonEmptyText
    scope_summary: NonEmptyText

    vehicle_applicability: tuple[
        NonEmptyText,
        ...,
    ]

    requirement_topics: tuple[
        NonEmptyText,
        ...,
    ] = Field(
        min_length=1,
    )

    reviewed_version: NonEmptyText

    reviewed_source_documents: tuple[
        NonEmptyText,
        ...,
    ] = Field(
        min_length=1,
    )

    source_format: SourceFormat
    source_content_date: date | None
    source_reviewed_on: date

    special_status_notes: tuple[
        NonEmptyText,
        ...,
    ]

    verification_status: Literal["verified"]

    @field_validator(
        "aliases",
        "vehicle_applicability",
        "requirement_topics",
        "reviewed_source_documents",
        "special_status_notes",
    )
    @classmethod
    def validate_unique_collections(
        cls,
        values: tuple[str, ...],
    ) -> tuple[str, ...]:
        return _validate_unique_values(values)


class RegulationComparisonPair(BaseModel):
    """Validated relationship between UNECE and FMVSS records."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    schema_version: Literal["1.0"]

    pair_number: int = Field(
        ge=1,
    )

    pair_id: str = Field(
        pattern=(
            r"^unece_[a-z0-9]+"
            r"__fmvss_[a-z0-9]+$"
        ),
    )

    left_regulation_id: str = Field(
        pattern=r"^unece_[a-z0-9]+$",
    )

    right_regulation_id: str = Field(
        pattern=r"^fmvss_[a-z0-9]+$",
    )

    status: ComparisonStatus
    comparison_level: ComparisonLevel
    regulatory_system: RegulatorySystem
    comparison_focus: ComparisonFocus
    overlap_summary: NonEmptyText

    comparable_topics: tuple[
        NonEmptyText,
        ...,
    ] = Field(
        min_length=1,
    )

    scope_differences: tuple[
        NonEmptyText,
        ...,
    ] = Field(
        min_length=1,
    )

    legal_equivalence: Literal[False]
    verification_reference: NonEmptyText
    source_reviewed_on: date

    @field_validator(
        "comparable_topics",
        "scope_differences",
    )
    @classmethod
    def validate_unique_collections(
        cls,
        values: tuple[str, ...],
    ) -> tuple[str, ...]:
        return _validate_unique_values(values)


class RegulationDataset(BaseModel):
    """Immutable, validated regulation data held in memory."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    records: tuple[
        RegulationRecord,
        ...,
    ]

    comparison_pairs: tuple[
        RegulationComparisonPair,
        ...,
    ]

    regulation_search_documents: tuple[
        str,
        ...,
    ]

    comparison_search_documents: tuple[
        str,
        ...,
    ]
