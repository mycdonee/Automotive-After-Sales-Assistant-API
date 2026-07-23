import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from app.services.base_retrieval_service import (
    NHTSA_DATA_PATH,
)


client = TestClient(app)


def test_retrieval_search_returns_ranked_results() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "My brakes make a squeaking noise",
            "top_k": 3,
            "method": "tfidf",
            "dataset": "synthetic",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["method"] == "tfidf"
    assert body["dataset"] == "synthetic"
    assert body["result_count"] == 3

    first_result = body["results"][0]

    assert first_result["record_id"] == "SR001"
    assert first_result["category"] == "Braking System"
    assert (
        first_result["source"]
        == "Synthetic service records"
    )
    assert 0.0 <= first_result["similarity_score"] <= 1.0


def test_retrieval_respects_top_k() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "The battery loses power overnight",
            "top_k": 2,
            "method": "tfidf",
        },
    )

    assert response.status_code == 200
    assert response.json()["result_count"] == 2
    assert len(response.json()["results"]) == 2


def test_retrieval_rejects_short_query() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "x",
            "top_k": 3,
            "method": "tfidf",
        },
    )

    assert response.status_code == 422


def test_retrieval_rejects_invalid_top_k() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "Engine overheating",
            "top_k": 50,
            "method": "tfidf",
        },
    )

    assert response.status_code == 422


def test_retrieval_rejects_unknown_method() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "Engine overheating",
            "method": "unknown",
        },
    )

    assert response.status_code == 422


def test_retrieval_rejects_unknown_dataset() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "Engine overheating",
            "method": "tfidf",
            "dataset": "private_database",
        },
    )

    assert response.status_code == 422


def test_semantic_retrieval_understands_natural_language() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "The car battery is dead every morning",
            "top_k": 3,
            "method": "semantic",
            "dataset": "synthetic",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["method"] == "semantic"
    assert body["result_count"] == 3

    first_result = body["results"][0]

    assert first_result["record_id"] in {
        "SR007",
        "SR008",
    }
    assert first_result["category"] == "Electrical System"


def test_semantic_retrieval_respects_top_k() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "The cabin does not become cold",
            "top_k": 2,
            "method": "semantic",
        },
    )

    assert response.status_code == 200
    assert response.json()["result_count"] == 2


def test_nhtsa_retrieval_applies_metadata_filters() -> None:
    records = pd.read_csv(
        NHTSA_DATA_PATH,
        dtype=str,
        keep_default_na=False,
    )

    eligible_records = records[
        records["make"].str.strip().ne("")
        & records["model_year"].str.fullmatch(
            r"\d{4}",
            na=False,
        )
    ]

    sample_record = eligible_records.iloc[0]

    category = sample_record["category"]
    make = sample_record["make"]
    model_year = int(sample_record["model_year"])
    query = sample_record["description"][:500]

    response = client.post(
        "/retrieval/search",
        json={
            "query": query,
            "top_k": 3,
            "method": "tfidf",
            "dataset": "nhtsa",
            "filters": {
                "category": category,
                "make": make,
                "model_year": model_year,
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["dataset"] == "nhtsa"
    assert body["result_count"] >= 1
    assert body["applied_filters"]["category"] == category
    assert body["applied_filters"]["make"] == make
    assert (
        body["applied_filters"]["model_year"]
        == model_year
    )

    for result in body["results"]:
        assert result["category"] == category
        assert result["make"].casefold() == make.casefold()
        assert result["model_year"] == str(model_year)
        assert (
            result["source"]
            == "NHTSA Consumer Complaints"
        )


def test_retrieval_returns_empty_results_for_unmatched_filter() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "Engine overheating",
            "top_k": 3,
            "method": "tfidf",
            "dataset": "synthetic",
            "filters": {
                "category": "Category That Does Not Exist"
            },
        },
    )

    assert response.status_code == 200
    assert response.json()["result_count"] == 0
    assert response.json()["results"] == []
    