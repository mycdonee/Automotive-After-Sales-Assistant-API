from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, get_args

from app.schemas.regulation import (
    ComparisonFocus,
    ComparisonLevel,
    Jurisdiction,
    RegulatorySystem,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_OUTPUT_PATH = (
    PROJECT_ROOT
    / "integrations"
    / "power_platform"
    / "swagger.json"
)

DEFAULT_HOST = (
    "replace-with-your-api-host.example.com"
)

CONNECTOR_VERSION = "1.0.0"

MAX_CONNECTOR_SIZE_BYTES = 1_000_000


def validate_host(
    host: str,
) -> str:
    """Validate a Swagger 2.0 host without scheme or path."""

    normalized = host.strip()

    if not normalized:
        raise ValueError(
            "Connector host must not be empty."
        )

    if "://" in normalized:
        raise ValueError(
            "Connector host must not include "
            "http:// or https://."
        )

    if "/" in normalized:
        raise ValueError(
            "Connector host must not include a path."
        )

    return normalized


def text_property(
    summary: str,
    description: str,
    **constraints: Any,
) -> dict[str, Any]:
    property_schema: dict[str, Any] = {
        "type": "string",
        "x-ms-summary": summary,
        "description": description,
    }

    property_schema.update(constraints)

    return property_schema


def integer_property(
    summary: str,
    description: str,
    **constraints: Any,
) -> dict[str, Any]:
    property_schema: dict[str, Any] = {
        "type": "integer",
        "format": "int32",
        "x-ms-summary": summary,
        "description": description,
    }

    property_schema.update(constraints)

    return property_schema


def number_property(
    summary: str,
    description: str,
    **constraints: Any,
) -> dict[str, Any]:
    property_schema: dict[str, Any] = {
        "type": "number",
        "format": "double",
        "x-ms-summary": summary,
        "description": description,
    }

    property_schema.update(constraints)

    return property_schema


def boolean_property(
    summary: str,
    description: str,
    **constraints: Any,
) -> dict[str, Any]:
    property_schema: dict[str, Any] = {
        "type": "boolean",
        "x-ms-summary": summary,
        "description": description,
    }

    property_schema.update(constraints)

    return property_schema


def object_definition(
    properties: dict[str, Any],
    required: list[str],
    summary: str,
    description: str,
) -> dict[str, Any]:
    return {
        "type": "object",
        "required": required,
        "additionalProperties": False,
        "x-ms-summary": summary,
        "description": description,
        "properties": properties,
    }


def build_definitions() -> dict[str, Any]:
    jurisdictions = list(
        get_args(Jurisdiction)
    )

    regulatory_systems = list(
        get_args(RegulatorySystem)
    )

    comparison_focuses = list(
        get_args(ComparisonFocus)
    )

    comparison_levels = list(
        get_args(ComparisonLevel)
    )

    regulation_request = object_definition(
        summary="Regulation Search Request",
        description=(
            "Natural-language request for searching "
            "verified regulation records."
        ),
        required=["query"],
        properties={
            "query": text_property(
                summary="Query",
                description=(
                    "Describe the regulation, requirement, "
                    "regulated object, or vehicle system."
                ),
                minLength=3,
                maxLength=500,
                example=(
                    "Portable warning triangle requirements"
                ),
                **{
                    "x-ms-visibility": "important",
                },
            ),
            "top_k": integer_property(
                summary="Maximum Results",
                description=(
                    "Maximum number of ranked results."
                ),
                default=5,
                minimum=1,
                maximum=10,
                **{
                    "x-ms-visibility": "advanced",
                },
            ),
            "jurisdiction": text_property(
                summary="Jurisdiction",
                description=(
                    "Optionally restrict results to UNECE "
                    "or United States standards."
                ),
                enum=jurisdictions,
                **{
                    "x-ms-visibility": "advanced",
                },
            ),
            "regulatory_system": text_property(
                summary="Regulatory System",
                description=(
                    "Optionally restrict results to one "
                    "supported automotive regulatory system."
                ),
                enum=regulatory_systems,
                **{
                    "x-ms-visibility": "advanced",
                },
            ),
        },
    )

    regulation_result = object_definition(
        summary="Regulation Search Result",
        description=(
            "One semantically ranked regulation record."
        ),
        required=[
            "result_type",
            "regulation_id",
            "official_identifier",
            "title",
            "jurisdiction",
            "regulatory_system",
            "regulated_object",
            "scope_summary",
            "reviewed_version",
            "similarity_score",
        ],
        properties={
            "result_type": text_property(
                summary="Result Type",
                description=(
                    "Indicates an individual regulation result."
                ),
                enum=["regulation"],
            ),
            "regulation_id": text_property(
                summary="Regulation ID",
                description=(
                    "Stable internal regulation identifier."
                ),
            ),
            "official_identifier": text_property(
                summary="Official Identifier",
                description=(
                    "Official UNECE or FMVSS identifier."
                ),
            ),
            "title": text_property(
                summary="Title",
                description="Official regulation title.",
            ),
            "jurisdiction": text_property(
                summary="Jurisdiction",
                description="Regulation jurisdiction.",
                enum=jurisdictions,
            ),
            "regulatory_system": text_property(
                summary="Regulatory System",
                description=(
                    "Automotive regulatory-system category."
                ),
                enum=regulatory_systems,
            ),
            "regulated_object": text_property(
                summary="Regulated Object",
                description=(
                    "Vehicle system, component, or object "
                    "regulated by the source."
                ),
            ),
            "scope_summary": text_property(
                summary="Scope Summary",
                description=(
                    "Reviewed high-level scope summary."
                ),
            ),
            "reviewed_version": text_property(
                summary="Reviewed Version",
                description=(
                    "Version reviewed for this dataset."
                ),
            ),
            "similarity_score": number_property(
                summary="Similarity Score",
                description=(
                    "Semantic ranking signal. This is not "
                    "legal confidence or compliance approval."
                ),
                minimum=-1.0,
                maximum=1.0,
            ),
        },
    )

    regulation_response = object_definition(
        summary="Regulation Search Response",
        description=(
            "Response containing ranked regulation records."
        ),
        required=[
            "query",
            "result_count",
            "results",
        ],
        properties={
            "query": text_property(
                summary="Query",
                description="Normalized search query.",
            ),
            "jurisdiction": text_property(
                summary="Jurisdiction",
                description=(
                    "Applied jurisdiction filter, when present."
                ),
                enum=jurisdictions,
            ),
            "regulatory_system": text_property(
                summary="Regulatory System",
                description=(
                    "Applied regulatory-system filter, "
                    "when present."
                ),
                enum=regulatory_systems,
            ),
            "result_count": integer_property(
                summary="Result Count",
                description=(
                    "Number of returned regulation records."
                ),
                minimum=0,
            ),
            "results": {
                "type": "array",
                "x-ms-summary": "Results",
                "description": (
                    "Ranked regulation-search results."
                ),
                "items": {
                    "$ref": (
                        "#/definitions/"
                        "RegulationSearchResult"
                    )
                },
            },
        },
    )

    comparison_request = object_definition(
        summary="Comparison Search Request",
        description=(
            "Natural-language request for searching "
            "approved UNECE–FMVSS comparison pairs."
        ),
        required=["query"],
        properties={
            "query": text_property(
                summary="Query",
                description=(
                    "Describe the regulatory comparison topic."
                ),
                minLength=3,
                maxLength=500,
                example=(
                    "Compare European and United States "
                    "warning triangle requirements"
                ),
                **{
                    "x-ms-visibility": "important",
                },
            ),
            "top_k": integer_property(
                summary="Maximum Results",
                description=(
                    "Maximum number of ranked comparison pairs."
                ),
                default=5,
                minimum=1,
                maximum=10,
                **{
                    "x-ms-visibility": "advanced",
                },
            ),
            "regulatory_system": text_property(
                summary="Regulatory System",
                description=(
                    "Optionally restrict comparison pairs "
                    "to one regulatory system."
                ),
                enum=regulatory_systems,
                **{
                    "x-ms-visibility": "advanced",
                },
            ),
        },
    )

    comparison_result = object_definition(
        summary="Comparison Search Result",
        description=(
            "One semantically ranked UNECE–FMVSS "
            "comparison pair."
        ),
        required=[
            "result_type",
            "pair_id",
            "pair_number",
            "left_regulation_id",
            "right_regulation_id",
            "left_official_identifier",
            "right_official_identifier",
            "regulatory_system",
            "comparison_focus",
            "comparison_level",
            "overlap_summary",
            "legal_equivalence",
            "similarity_score",
        ],
        properties={
            "result_type": text_property(
                summary="Result Type",
                description=(
                    "Indicates a regulation-comparison result."
                ),
                enum=["comparison"],
            ),
            "pair_id": text_property(
                summary="Pair ID",
                description=(
                    "Stable internal comparison-pair ID."
                ),
            ),
            "pair_number": integer_property(
                summary="Pair Number",
                description=(
                    "Reviewed comparison-pair number."
                ),
                minimum=1,
            ),
            "left_regulation_id": text_property(
                summary="UNECE Regulation ID",
                description=(
                    "Internal ID of the UNECE regulation."
                ),
            ),
            "right_regulation_id": text_property(
                summary="FMVSS Regulation ID",
                description=(
                    "Internal ID of the United States standard."
                ),
            ),
            "left_official_identifier": text_property(
                summary="UNECE Official Identifier",
                description=(
                    "Official identifier of the UNECE source."
                ),
            ),
            "right_official_identifier": text_property(
                summary="FMVSS Official Identifier",
                description=(
                    "Official identifier of the FMVSS source."
                ),
            ),
            "regulatory_system": text_property(
                summary="Regulatory System",
                description=(
                    "Shared regulatory-system category."
                ),
                enum=regulatory_systems,
            ),
            "comparison_focus": text_property(
                summary="Comparison Focus",
                description=(
                    "Reviewed technical comparison focus."
                ),
                enum=comparison_focuses,
            ),
            "comparison_level": text_property(
                summary="Comparison Level",
                description=(
                    "Strength and scope of the comparison."
                ),
                enum=comparison_levels,
            ),
            "overlap_summary": text_property(
                summary="Overlap Summary",
                description=(
                    "Reviewed summary of meaningful overlap."
                ),
            ),
            "legal_equivalence": boolean_property(
                summary="Legal Equivalence",
                description=(
                    "Always false. The comparison does not "
                    "establish legal interchangeability."
                ),
                enum=[False],
                default=False,
            ),
            "similarity_score": number_property(
                summary="Similarity Score",
                description=(
                    "Semantic ranking signal. This is not "
                    "legal confidence or compliance approval."
                ),
                minimum=-1.0,
                maximum=1.0,
            ),
        },
    )

    comparison_response = object_definition(
        summary="Comparison Search Response",
        description=(
            "Response containing ranked regulation "
            "comparison pairs."
        ),
        required=[
            "query",
            "result_count",
            "results",
        ],
        properties={
            "query": text_property(
                summary="Query",
                description="Normalized search query.",
            ),
            "regulatory_system": text_property(
                summary="Regulatory System",
                description=(
                    "Applied regulatory-system filter, "
                    "when present."
                ),
                enum=regulatory_systems,
            ),
            "result_count": integer_property(
                summary="Result Count",
                description=(
                    "Number of returned comparison pairs."
                ),
                minimum=0,
            ),
            "results": {
                "type": "array",
                "x-ms-summary": "Results",
                "description": (
                    "Ranked comparison-search results."
                ),
                "items": {
                    "$ref": (
                        "#/definitions/"
                        "RegulationComparisonSearchResult"
                    )
                },
            },
        },
    )

    return {
        "RegulationSearchRequest": (
            regulation_request
        ),
        "RegulationSearchResult": (
            regulation_result
        ),
        "RegulationSearchResponse": (
            regulation_response
        ),
        "RegulationComparisonSearchRequest": (
            comparison_request
        ),
        "RegulationComparisonSearchResult": (
            comparison_result
        ),
        "RegulationComparisonSearchResponse": (
            comparison_response
        ),
    }


def build_power_platform_spec(
    host: str = DEFAULT_HOST,
) -> dict[str, Any]:
    """Build a connector-specific Swagger 2.0 definition."""

    validated_host = validate_host(host)

    return {
        "swagger": "2.0",
        "info": {
            "title": (
                "Automotive Regulatory Search"
            ),
            "description": (
                "Search verified automotive regulations "
                "and scoped UNECE–FMVSS comparison pairs. "
                "Results are informational and do not "
                "establish legal equivalence."
            ),
            "version": CONNECTOR_VERSION,
        },
        "host": validated_host,
        "basePath": "/",
        "schemes": ["https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "paths": {
            "/regulations/search": {
                "post": {
                    "tags": ["Regulations"],
                    "summary": (
                        "Search verified regulations"
                    ),
                    "description": (
                        "Semantically search verified UNECE "
                        "and United States regulation records."
                    ),
                    "operationId": "SearchRegulations",
                    "x-ms-visibility": "important",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "x-ms-summary": (
                                "Regulation Search Request"
                            ),
                            "description": (
                                "Search query and optional "
                                "metadata filters."
                            ),
                            "schema": {
                                "$ref": (
                                    "#/definitions/"
                                    "RegulationSearchRequest"
                                )
                            },
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": (
                                "Successful regulation search."
                            ),
                            "schema": {
                                "$ref": (
                                    "#/definitions/"
                                    "RegulationSearchResponse"
                                )
                            },
                        },
                        "422": {
                            "description": (
                                "Request validation failed."
                            )
                        },
                    },
                }
            },
            "/regulations/comparisons/search": {
                "post": {
                    "tags": ["Regulations"],
                    "summary": (
                        "Search regulation comparisons"
                    ),
                    "description": (
                        "Semantically search approved "
                        "UNECE–FMVSS comparison pairs."
                    ),
                    "operationId": (
                        "SearchRegulationComparisons"
                    ),
                    "x-ms-visibility": "important",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "x-ms-summary": (
                                "Comparison Search Request"
                            ),
                            "description": (
                                "Comparison query and optional "
                                "regulatory-system filter."
                            ),
                            "schema": {
                                "$ref": (
                                    "#/definitions/"
                                    "RegulationComparisonSearchRequest"
                                )
                            },
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": (
                                "Successful comparison search."
                            ),
                            "schema": {
                                "$ref": (
                                    "#/definitions/"
                                    "RegulationComparisonSearchResponse"
                                )
                            },
                        },
                        "422": {
                            "description": (
                                "Request validation failed."
                            )
                        },
                    },
                }
            },
        },
        "definitions": build_definitions(),
    }


def write_power_platform_spec(
    output_path: Path,
    host: str,
) -> int:
    """Write the Swagger definition and return its byte size."""

    spec = build_power_platform_spec(
        host=host
    )

    encoded = (
        json.dumps(
            spec,
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")

    if len(encoded) >= MAX_CONNECTOR_SIZE_BYTES:
        raise ValueError(
            "Power Platform connector definition must "
            "be smaller than 1 MB."
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_bytes(encoded)

    return len(encoded)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Export a Power Platform-compatible "
            "Swagger 2.0 connector definition."
        )
    )

    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help=(
            "Public API host without scheme or path. "
            f"Default: {DEFAULT_HOST}"
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=(
            "Output JSON path. "
            f"Default: {DEFAULT_OUTPUT_PATH}"
        ),
    )

    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()

    size = write_power_platform_spec(
        output_path=arguments.output,
        host=arguments.host,
    )

    print(
        "Power Platform Swagger 2.0 "
        f"written to: {arguments.output}"
    )

    print(
        f"Host: {validate_host(arguments.host)}"
    )

    print(f"Size: {size} bytes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
