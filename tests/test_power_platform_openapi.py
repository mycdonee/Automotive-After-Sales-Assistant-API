import json
from pathlib import Path
from typing import Any

import pytest

from app.main import app
from scripts.export_power_platform_openapi import (
    DEFAULT_HOST,
    DEFAULT_OUTPUT_PATH,
    MAX_CONNECTOR_SIZE_BYTES,
    build_power_platform_spec,
    validate_host,
    write_power_platform_spec,
)


EXPECTED_OPERATION_IDS = {
    "SearchRegulations",
    "SearchRegulationComparisons",
}


def collect_references(
    value: Any,
) -> list[str]:
    """Collect every JSON reference from a nested specification."""

    references: list[str] = []

    if isinstance(value, dict):
        for key, child in value.items():
            if (
                key == "$ref"
                and isinstance(child, str)
            ):
                references.append(child)
            else:
                references.extend(
                    collect_references(child)
                )

    elif isinstance(value, list):
        for child in value:
            references.extend(
                collect_references(child)
            )

    return references


def test_connector_uses_swagger_2() -> None:
    spec = build_power_platform_spec(
        host="api.example.com"
    )

    assert spec["swagger"] == "2.0"
    assert "openapi" not in spec
    assert "components" not in spec

    assert spec["host"] == "api.example.com"
    assert spec["basePath"] == "/"
    assert spec["schemes"] == ["https"]

    assert spec["consumes"] == [
        "application/json"
    ]

    assert spec["produces"] == [
        "application/json"
    ]


def test_connector_contains_expected_operations() -> None:
    spec = build_power_platform_spec(
        host="api.example.com"
    )

    operation_ids = {
        operation["operationId"]
        for path_item in spec["paths"].values()
        for method, operation in path_item.items()
        if method == "post"
    }

    assert operation_ids == EXPECTED_OPERATION_IDS
    assert len(operation_ids) == 2


def test_connector_operation_ids_match_fastapi() -> None:
    fastapi_schema = app.openapi()

    assert (
        fastapi_schema["paths"]
        ["/regulations/search"]
        ["post"]
        ["operationId"]
        == "SearchRegulations"
    )

    assert (
        fastapi_schema["paths"]
        ["/regulations/comparisons/search"]
        ["post"]
        ["operationId"]
        == "SearchRegulationComparisons"
    )


def test_connector_references_existing_definitions() -> None:
    spec = build_power_platform_spec(
        host="api.example.com"
    )

    definitions = spec["definitions"]

    for reference in collect_references(spec):
        prefix = "#/definitions/"

        assert reference.startswith(prefix)

        definition_name = reference.removeprefix(
            prefix
        )

        assert definition_name in definitions


def test_connector_avoids_openapi_3_keywords() -> None:
    spec = build_power_platform_spec(
        host="api.example.com"
    )

    serialized = json.dumps(spec)

    unsupported_keywords = (
        '"components"',
        '"requestBody"',
        '"nullable"',
        '"anyOf"',
        '"oneOf"',
        '"const"',
    )

    for keyword in unsupported_keywords:
        assert keyword not in serialized


def test_connector_preserves_legal_boundary() -> None:
    spec = build_power_platform_spec(
        host="api.example.com"
    )

    legal_equivalence = (
        spec["definitions"]
        ["RegulationComparisonSearchResult"]
        ["properties"]
        ["legal_equivalence"]
    )

    assert legal_equivalence["type"] == "boolean"
    assert legal_equivalence["enum"] == [False]
    assert legal_equivalence["default"] is False


def test_connector_file_is_below_size_limit(
    tmp_path: Path,
) -> None:
    output_path = (
        tmp_path / "swagger.json"
    )

    size = write_power_platform_spec(
        output_path=output_path,
        host="api.example.com",
    )

    assert output_path.exists()
    assert size == output_path.stat().st_size
    assert size < MAX_CONNECTOR_SIZE_BYTES

    loaded = json.loads(
        output_path.read_text(
            encoding="utf-8"
        )
    )

    assert loaded["swagger"] == "2.0"
    assert loaded["host"] == "api.example.com"


@pytest.mark.parametrize(
    "invalid_host",
    [
        "",
        "   ",
        "https://api.example.com",
        "http://api.example.com",
        "api.example.com/v1",
    ],
)
def test_invalid_connector_host_is_rejected(
    invalid_host: str,
) -> None:
    with pytest.raises(
        ValueError,
    ):
        validate_host(invalid_host)

def test_committed_connector_matches_exporter() -> None:
    committed_spec = json.loads(
        DEFAULT_OUTPUT_PATH.read_text(
            encoding="utf-8"
        )
    )

    generated_spec = build_power_platform_spec(
        host=DEFAULT_HOST
    )

    assert committed_spec == generated_spec

    assert (
        DEFAULT_OUTPUT_PATH.stat().st_size
        < MAX_CONNECTOR_SIZE_BYTES
    )

