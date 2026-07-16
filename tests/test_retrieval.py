from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_retrieval_search_returns_ranked_results() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "My brakes make a squeaking noise",
            "top_k": 3,
            "method": "tfidf",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["query"] == "My brakes make a squeaking noise"
    assert body["method"] == "tfidf"
    assert body["result_count"] == 3
    assert len(body["results"]) == 3

    first_result = body["results"][0]

    assert first_result["record_id"] == "SR001"
    assert first_result["category"] == "Braking System"
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
            "top_k": 3,
            "method": "unknown",
        },
    )

    assert response.status_code == 422
    
def test_semantic_retrieval_returns_ranked_results() -> None:
    response = client.post(
        "/retrieval/search",
        json={
            "query": "The car battery is dead every morning",
            "top_k": 3,
            "method": "semantic",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["method"] == "semantic"
    assert body["result_count"] == 3
    assert len(body["results"]) == 3

    first_result = body["results"][0]

    assert first_result["record_id"] in {"SR007", "SR008"}
    assert first_result["category"] == "Electrical System"
    assert 0.0 <= first_result["similarity_score"] <= 1.0


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
    assert response.json()["method"] == "semantic"
    assert response.json()["result_count"] == 2
    assert len(response.json()["results"]) == 2
    
    