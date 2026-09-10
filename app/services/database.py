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
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                api_key TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            INSERT OR IGNORE INTO users (id, username, api_key)
            VALUES (1, 'default', 'dev-default-key')
            """
        )

        reviews_exists = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'reviews'
            """
        ).fetchone()

        if not reviews_exists:
            connection.execute(
                """
                CREATE TABLE reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL DEFAULT 1,
                    language TEXT NOT NULL,
                    code TEXT NOT NULL,
                    quality_rating REAL NOT NULL,
                    summary TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )
        else:
            columns = {
                row["name"]
                for row in connection.execute(
                    "PRAGMA table_info(reviews)"
                ).fetchall()
            }

            if "user_id" not in columns:
                connection.execute(
                    """
                    ALTER TABLE reviews
                    ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1
                    """
                )

        connection.commit()


def create_user(
    username: str,
    api_key: str,
) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (username, api_key)
            VALUES (?, ?)
            """,
            (username, api_key),
        )

        connection.commit()

        return cursor.lastrowid


def get_user_by_api_key(
    api_key: str,
) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, username, api_key, created_at
            FROM users
            WHERE api_key = ?
            """,
            (api_key,),
        ).fetchone()

        return dict(row) if row else None


def save_review(
    user_id: int,
    language: str,
    code: str,
    quality_rating: float,
    summary: str,
) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO reviews (
                user_id,
                language,
                code,
                quality_rating,
                summary
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                language,
                code,
                quality_rating,
                summary,
            ),
        )

        connection.commit()

        return cursor.lastrowid


def get_reviews(
    user_id: int | None = None,
) -> list[dict]:
    with get_connection() as connection:
        if user_id is None:
            rows = connection.execute(
                """
                SELECT
                    id,
                    user_id,
                    language,
                    code,
                    quality_rating,
                    summary,
                    created_at
                FROM reviews
                ORDER BY id DESC
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT
                    id,
                    user_id,
                    language,
                    code,
                    quality_rating,
                    summary,
                    created_at
                FROM reviews
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (user_id,),
            ).fetchall()

        return [dict(row) for row in rows]

def get_review_progress(user_id: int) -> dict:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_reviews,
                AVG(quality_rating) AS average_quality,
                MAX(quality_rating) AS best_quality,
                (
                    SELECT quality_rating
                    FROM reviews
                    WHERE user_id = ?
                    ORDER BY id DESC
                    LIMIT 1
                ) AS latest_quality,
                (
                    SELECT quality_rating
                    FROM reviews
                    WHERE user_id = ?
                    ORDER BY id ASC
                    LIMIT 1
                ) AS first_quality
            FROM reviews
            WHERE user_id = ?
            """,
            (user_id, user_id, user_id),
        ).fetchone()

        total_reviews = row["total_reviews"]

        if total_reviews == 0:
            return {
                "total_reviews": 0,
                "average_quality": None,
                "best_quality": None,
                "latest_quality": None,
                "improvement": None,
            }

        first_quality = row["first_quality"]
        latest_quality = row["latest_quality"]

        improvement = round(
            latest_quality - first_quality,
            1,
        )

        return {
            "total_reviews": total_reviews,
            "average_quality": round(
                row["average_quality"],
                1,
            ),
            "best_quality": row["best_quality"],
            "latest_quality": latest_quality,
            "improvement": improvement,
        }