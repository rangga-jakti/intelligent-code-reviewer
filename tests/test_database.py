from app.services.database import (
    get_reviews,
    init_db,
    save_review,
)


def test_database_can_save_and_read_review(tmp_path, monkeypatch):
    import app.services.database as database

    test_db = tmp_path / "test_reviews.db"

    monkeypatch.setattr(database, "DB_PATH", test_db)

    init_db()

    review_id = save_review(
        language="python",
        code="print('hello')",
        quality_rating=9.5,
        summary="Clean code",
    )

    reviews = get_reviews()

    assert review_id == 1
    assert len(reviews) == 1
    assert reviews[0]["language"] == "python"
    assert reviews[0]["quality_rating"] == 9.5
    assert reviews[0]["summary"] == "Clean code"