import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    import app.services.database as database

    test_db = tmp_path / "test_reviews.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    database.init_db()


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Intelligent Code Reviewer is running"
    }


def test_review_requires_code():
    response = client.post(
        "/review",
        headers={
            "X-API-Key": "dev-default-key",
        },
        json={
            "language": "python",
        },
    )

    assert response.status_code == 422


def test_review_rejects_empty_code():
    response = client.post(
        "/review",
        headers={
            "X-API-Key": "dev-default-key",
        },
        json={
            "code": "",
            "language": "python",
        },
    )

    assert response.status_code == 422


def test_review_rejects_unsupported_language():
    response = client.post(
        "/review",
        headers={
            "X-API-Key": "dev-default-key",
        },
        json={
            "code": "fn main() {}",
            "language": "rust",
        },
    )

    assert response.status_code == 422
    assert "Unsupported language" in response.json()["detail"]


def test_review_history_requires_api_key():
    response = client.get("/reviews")

    assert response.status_code == 401


def test_review_history_accepts_valid_api_key():
    response = client.get(
        "/reviews",
        headers={
            "X-API-Key": "dev-default-key",
        },
    )

    assert response.status_code == 200
    assert "reviews" in response.json()


def test_review_history_rejects_invalid_api_key():
    response = client.get(
        "/reviews",
        headers={
            "X-API-Key": "invalid-key",
        },
    )

    assert response.status_code == 401


def test_review_history_isolated_between_users(tmp_path, monkeypatch):
    import app.services.database as database

    test_db = tmp_path / "test_reviews.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    database.init_db()

    user_a = database.create_user(
        username="api-user-a",
        api_key="api-key-a",
    )

    user_b = database.create_user(
        username="api-user-b",
        api_key="api-key-b",
    )

    database.save_review(
        user_id=user_a,
        language="python",
        code="print('A')",
        quality_rating=9.0,
        summary="Review A",
    )

    database.save_review(
        user_id=user_b,
        language="python",
        code="print('B')",
        quality_rating=7.0,
        summary="Review B",
    )

    response_a = client.get(
        "/reviews",
        headers={
            "X-API-Key": "api-key-a",
        },
    )

    response_b = client.get(
        "/reviews",
        headers={
            "X-API-Key": "api-key-b",
        },
    )

    assert response_a.status_code == 200
    assert response_b.status_code == 200

    reviews_a = response_a.json()["reviews"]
    reviews_b = response_b.json()["reviews"]

    assert len(reviews_a) == 1
    assert reviews_a[0]["summary"] == "Review A"

    assert len(reviews_b) == 1
    assert reviews_b[0]["summary"] == "Review B"


def test_register_user():
    response = client.post(
        "/users",
        json={
            "username": "new-user",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "new-user"
    assert "api_key" in data
    assert len(data["api_key"]) > 20


def test_registered_user_can_access_history():
    response = client.post(
        "/users",
        json={
            "username": "history-user",
        },
    )

    assert response.status_code == 200

    api_key = response.json()["api_key"]

    history_response = client.get(
        "/reviews",
        headers={
            "X-API-Key": api_key,
        },
    )

    assert history_response.status_code == 200
    assert history_response.json()["reviews"] == []