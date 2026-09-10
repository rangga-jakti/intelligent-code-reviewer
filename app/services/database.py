import sqlite3
from pathlib import Path


DB_PATH = Path("data/reviews.db")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language TEXT NOT NULL,
                code TEXT NOT NULL,
                quality_rating REAL NOT NULL,
                summary TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()


def save_review(
    language: str,
    code: str,
    quality_rating: float,
    summary: str,
) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO reviews (
                language,
                code,
                quality_rating,
                summary
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                language,
                code,
                quality_rating,
                summary,
            ),
        )

        connection.commit()

        return cursor.lastrowid


def get_reviews() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                language,
                code,
                quality_rating,
                summary,
                created_at
            FROM reviews
            ORDER BY id DESC
            """
        ).fetchall()

        return [dict(row) for row in rows]