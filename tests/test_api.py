from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Intelligent Code Reviewer is running"
    }
def test_review_requires_code():
    response = client.post(
        "/review",
        json={
            "language": "python"
        },
    )
    assert response.status_code == 422
def test_review_rejects_empty_code():
    response = client.post(
        "/review",
        json={
            "code": "",
            "language": "python",
        },
    )
    assert response.status_code == 422
def test_review_rejects_unsupported_language():
    response = client.post(
        "/review",
        json={
            "code": "fn main() {}",
            "language": "rust",
        },
    )

    assert response.status_code == 422
    assert "Unsupported language" in response.json()["detail"]

def test_review_history():
    response = client.get("/reviews")

    assert response.status_code == 200
    assert "reviews" in response.json()
