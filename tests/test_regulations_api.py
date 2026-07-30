from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.regulation import (
    RegulationComparisonSearchResult,
    RegulationSearchResult,
)
from app.services.regulation_semantic_search_service import (
    get_regulation_semantic_search_service,
)


class FakeRegulationSearchService:
    """Return deterministic API results without loading an embedding model."""

    def __init__(self) -> None:
        self.regulation_calls: list[dict[str, object]] = []
        self.comparison_calls: list[dict[str, object]] = []

    def search_regulations(
        self,
        query: str,
        top_k: int = 5,
        jurisdiction: str | None = None,
        regulatory_system: str | None = None,
    ) -> list[RegulationSearchResult]:
        self.regulation_calls.append(
            {
                "query": query,
                "top_k": top_k,
                "jurisdiction": jurisdiction,
                "regulatory_system": regulatory_system,
            }
        )

        return [
            RegulationSearchResult(
                regulation_id="unece_r27",
                official_identifier="UN Regulation No. 27",
                title="Advance warning triangles",
                jurisdiction="UNECE",
                regulatory_system=(
                    "lighting_and_light_signalling"
                ),
                regulated_object=(
                    "Portable advance warning triangles"
                ),
                scope_summary=(
                    "Requirements for portable warning "
                    "triangles used near a halted vehicle."
                ),
                reviewed_version="Revision 3, 05 series",
                similarity_score=0.9123,
            )
        ]

    def search_comparisons(
        self,
        query: str,
        top_k: int = 5,
        regulatory_system: str | None = None,
    ) -> list[RegulationComparisonSearchResult]:
        self.comparison_calls.append(
            {
                "query": query,
                "top_k": top_k,
                "regulatory_system": regulatory_system,
            }
        )

        return [
            RegulationComparisonSearchResult(
                pair_id="unece_r27__fmvss_125",
                pair_number=11,
                left_regulation_id="unece_r27",
                right_regulation_id="fmvss_125",
                left_official_identifier=(
                    "UN Regulation No. 27"
                ),
                right_official_identifier=(
                    "FMVSS No. 125"
                ),
                regulatory_system=(
                    "lighting_and_light_signalling"
                ),
                comparison_focus=(
                    "portable_advance_warning_triangle_performance"
                ),
                comparison_level="partial",
                overlap_summary=(
                    "Both regulate portable advance-warning "
                    "devices, with different scope and tests."
                ),
                legal_equivalence=False,
                similarity_score=0.8876,
            )
        ]


@pytest.fixture
def fake_service() -> FakeRegulationSearchService:
    return FakeRegulationSearchService()


@pytest.fixture
def client(
    fake_service: FakeRegulationSearchService,
) -> Generator[TestClient, None, None]:
    dependency = (
        get_regulation_semantic_search_service
    )

    previous_override = (
        app.dependency_overrides.get(
            dependency
        )
    )

    app.dependency_overrides[
        dependency
    ] = lambda: fake_service

    with TestClient(app) as test_client:
        yield test_client

    if previous_override is None:
        app.dependency_overrides.pop(
            dependency,
            None,
        )
    else:
        app.dependency_overrides[
            dependency
        ] = previous_override


def test_regulation_search_returns_typed_response(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/search",
        json={
            "query": (
                "  portable warning triangle "
                "requirements  "
            ),
            "top_k": 3,
            "jurisdiction": "UNECE",
            "regulatory_system": (
                "lighting_and_light_signalling"
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["query"]
        == "portable warning triangle requirements"
    )
    assert body["jurisdiction"] == "UNECE"
    assert (
        body["regulatory_system"]
        == "lighting_and_light_signalling"
    )
    assert body["result_count"] == 1

    first_result = body["results"][0]

    assert first_result["result_type"] == "regulation"
    assert (
        first_result["regulation_id"]
        == "unece_r27"
    )
    assert (
        first_result["official_identifier"]
        == "UN Regulation No. 27"
    )
    assert first_result["similarity_score"] == 0.9123

    assert fake_service.regulation_calls == [
        {
            "query": (
                "portable warning triangle requirements"
            ),
            "top_k": 3,
            "jurisdiction": "UNECE",
            "regulatory_system": (
                "lighting_and_light_signalling"
            ),
        }
    ]


def test_regulation_search_uses_default_top_k(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/search",
        json={
            "query": "electronic stability control",
        },
    )

    assert response.status_code == 200

    assert fake_service.regulation_calls == [
        {
            "query": "electronic stability control",
            "top_k": 5,
            "jurisdiction": None,
            "regulatory_system": None,
        }
    ]


def test_comparison_search_returns_typed_response(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/comparisons/search",
        json={
            "query": (
                "compare warning triangle requirements"
            ),
            "top_k": 2,
            "regulatory_system": (
                "lighting_and_light_signalling"
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["query"]
        == "compare warning triangle requirements"
    )
    assert body["result_count"] == 1

    first_result = body["results"][0]

    assert first_result["result_type"] == "comparison"
    assert (
        first_result["pair_id"]
        == "unece_r27__fmvss_125"
    )
    assert (
        first_result["comparison_level"]
        == "partial"
    )
    assert (
        first_result["legal_equivalence"]
        is False
    )

    assert fake_service.comparison_calls == [
        {
            "query": (
                "compare warning triangle requirements"
            ),
            "top_k": 2,
            "regulatory_system": (
                "lighting_and_light_signalling"
            ),
        }
    ]


def test_comparison_search_uses_default_top_k(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/comparisons/search",
        json={
            "query": "compare braking requirements",
        },
    )

    assert response.status_code == 200

    assert fake_service.comparison_calls == [
        {
            "query": "compare braking requirements",
            "top_k": 5,
            "regulatory_system": None,
        }
    ]


def test_blank_query_is_rejected(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/search",
        json={
            "query": "   ",
        },
    )

    assert response.status_code == 422
    assert fake_service.regulation_calls == []


def test_invalid_top_k_is_rejected(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/comparisons/search",
        json={
            "query": "lighting requirements",
            "top_k": 11,
        },
    )

    assert response.status_code == 422
    assert fake_service.comparison_calls == []


def test_invalid_jurisdiction_is_rejected(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/search",
        json={
            "query": "seat belt requirements",
            "jurisdiction": "European Union",
        },
    )

    assert response.status_code == 422
    assert fake_service.regulation_calls == []


def test_invalid_regulatory_system_is_rejected(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/search",
        json={
            "query": "engine emissions",
            "regulatory_system": "powertrain",
        },
    )

    assert response.status_code == 422
    assert fake_service.regulation_calls == []


def test_extra_request_field_is_rejected(
    client: TestClient,
    fake_service: FakeRegulationSearchService,
) -> None:
    response = client.post(
        "/regulations/comparisons/search",
        json={
            "query": "compare lighting requirements",
            "include_legal_advice": True,
        },
    )

    assert response.status_code == 422
    assert fake_service.comparison_calls == []


def test_openapi_documents_regulation_endpoints(
    client: TestClient,
) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()
    paths = openapi["paths"]

    assert "/regulations/search" in paths
    assert (
        "/regulations/comparisons/search"
        in paths
    )

    regulation_operation = paths[
        "/regulations/search"
    ]["post"]

    comparison_operation = paths[
        "/regulations/comparisons/search"
    ]["post"]

    assert (
        regulation_operation["summary"]
        == "Search verified regulations"
    )

    assert (
        comparison_operation["summary"]
        == "Search verified regulation comparisons"
    )

    schemas = openapi["components"]["schemas"]

    assert "RegulationSearchRequest" in schemas
    assert "RegulationSearchResponse" in schemas
    assert (
        "RegulationComparisonSearchRequest"
        in schemas
    )
    assert (
        "RegulationComparisonSearchResponse"
        in schemas
    )
