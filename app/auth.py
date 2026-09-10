from fastapi import Header, HTTPException

from app.services.database import get_user_by_api_key


def get_current_user(
    x_api_key: str | None = Header(
        default=None,
        alias="X-API-Key",
    ),
) -> dict:
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="X-API-Key header is required.",
        )

    user = get_user_by_api_key(x_api_key)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key.",
        )

    return user