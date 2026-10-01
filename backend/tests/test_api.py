import os

# Force local mock mode during tests.
os.environ["MOCK_AI"] = "true"

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_generate_mock():

    response = client.post(
        "/generate",
        json={
            "document_type": (
                "Freelance Work Contract"
            ),
            "parties": (
                "Jane Doe (Freelancer), "
                "TechNova Inc. (Client)"
            ),
            "terms": (
                "Payment within 30 days; "
                "Confidentiality applies; "
                "Termination on 15 days notice"
            ),
            "effective_date": (
                "April 15, 2026"
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["mock"] is True

    assert (
        "FREELANCE WORK CONTRACT"
        in body["content"]
    )

    assert (
        "Payment within 30 days"
        in body["content"]
    )