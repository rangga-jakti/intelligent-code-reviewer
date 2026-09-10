from app.services.database import (
    create_user,
    get_reviews,
    init_db,
    save_review,
)


def test_database_can_save_and_read_review(tmp_path, monkeypatch):
    import app.services.database as database

    test_db = tmp_path / "test_reviews.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    init_db()

    user_id = create_user(
        username="test-user",
        api_key="test-api-key",
    )

    review_id = save_review(
        user_id=user_id,
        language="python",
        code="print('hello')",
        quality_rating=9.5,
        summary="Clean code",
    )

    reviews = get_reviews(user_id=user_id)

    assert review_id == 1
    assert len(reviews) == 1
    assert reviews[0]["user_id"] == user_id
    assert reviews[0]["language"] == "python"
    assert reviews[0]["quality_rating"] == 9.5
    assert reviews[0]["summary"] == "Clean code"


def test_reviews_are_isolated_between_users(tmp_path, monkeypatch):
    import app.services.database as database

    test_db = tmp_path / "test_reviews.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    init_db()

    user_a = create_user(
        username="user-a",
        api_key="key-a",
    )

    user_b = create_user(
        username="user-b",
        api_key="key-b",
    )

    save_review(
        user_id=user_a,
        language="python",
        code="print('A')",
        quality_rating=9.0,
        summary="Review A",
    )

    save_review(
        user_id=user_b,
        language="python",
        code="print('B')",
        quality_rating=7.0,
        summary="Review B",
    )

    reviews_a = get_reviews(user_id=user_a)
    reviews_b = get_reviews(user_id=user_b)

    assert len(reviews_a) == 1
    assert reviews_a[0]["summary"] == "Review A"
    assert reviews_a[0]["user_id"] == user_a

    assert len(reviews_b) == 1
    assert reviews_b[0]["summary"] == "Review B"
    assert reviews_b[0]["user_id"] == user_b