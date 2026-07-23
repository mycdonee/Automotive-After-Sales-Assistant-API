from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(app)


def test_classification_predicts_braking_issue() -> None:
    response = client.post(
        "/classification/predict",
        json={
            "text": (
                "The brake pedal became hard "
                "and the vehicle could not stop."
            ),
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["predicted_category"]
        == "Braking System"
    )

    assert 0.0 <= body["confidence"] <= 1.0
    assert isinstance(
        body["review_required"],
        bool,
    )

    assert (
        body["model_version"]
        == "issue-classifier-logreg-v1"
    )

    assert (
        body["training_data_source"]
        == "NHTSA Consumer Complaints"
    )

    assert len(
        body["top_predictions"]
    ) == 3


def test_classification_predicts_electrical_issue() -> None:
    response = client.post(
        "/classification/predict",
        json={
            "text": (
                "The dashboard went completely "
                "black and the battery warning "
                "light came on while driving."
            ),
            "top_k": 3,
        },
    )

    assert response.status_code == 200

    assert (
        response.json()[
            "predicted_category"
        ]
        == "Electrical System"
    )


def test_classification_probabilities_are_ranked() -> None:
    response = client.post(
        "/classification/predict",
        json={
            "text": (
                "The steering became difficult "
                "to control on the highway."
            ),
            "top_k": 5,
        },
    )

    assert response.status_code == 200

    probabilities = [
        prediction["probability"]
        for prediction in response.json()[
            "top_predictions"
        ]
    ]

    assert probabilities == sorted(
        probabilities,
        reverse=True,
    )


def test_classification_rejects_short_text() -> None:
    response = client.post(
        "/classification/predict",
        json={
            "text": "brake",
            "top_k": 3,
        },
    )

    assert response.status_code == 422


def test_classification_rejects_invalid_top_k() -> None:
    response = client.post(
        "/classification/predict",
        json={
            "text": (
                "The engine overheats "
                "after extended driving."
            ),
            "top_k": 20,
        },
    )

    assert response.status_code == 422


def test_classification_rejects_unknown_fields() -> None:
    response = client.post(
        "/classification/predict",
        json={
            "text": (
                "The vehicle loses power "
                "while driving."
            ),
            "top_k": 3,
            "unknown_option": True,
        },
    )

    assert response.status_code == 422
    