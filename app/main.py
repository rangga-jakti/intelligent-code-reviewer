import secrets

from fastapi import Depends, FastAPI, HTTPException

from app.auth import get_current_user
from app.config import GROQ_API_KEY
from app.schemas import (
    ProgressResponse,
    ReviewRequest,
    ReviewResponse,
    UserCreate,
    UserResponse,
)
from app.services.database import (
    create_user,
    get_review_progress,
    get_reviews,
    init_db,
    save_review,
)
from app.services.historical_rules import load_rules
from app.services.language_config import get_language_config
from app.services.reviewer import CodeReviewer


app = FastAPI(
    title="24/7 Intelligent Code Reviewer",
    version="0.1.0",
)


init_db()


@app.get("/")
def root():
    return {"message": "Intelligent Code Reviewer is running"}


@app.post("/users", response_model=UserResponse)
def register_user(request: UserCreate):
    api_key = secrets.token_urlsafe(32)

    try:
        create_user(
            username=request.username,
            api_key=api_key,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=409,
            detail=f"Could not create user: {exc}",
        )

    return {
        "username": request.username,
        "api_key": api_key,
    }


@app.post("/review", response_model=ReviewResponse)
def review_code(
    request: ReviewRequest,
    current_user: dict = Depends(get_current_user),
):
    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured.",
        )

    try:
        get_language_config(request.language)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    try:
        rules = load_rules()
        reviewer = CodeReviewer(GROQ_API_KEY)

        result = reviewer.review(
            code=request.code,
            language=request.language,
            historical_rules=rules,
        )

        save_review(
            user_id=current_user["id"],
            language=request.language,
            code=request.code,
            quality_rating=result.quality_rating,
            summary=result.summary,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Review failed: {exc}",
        )


@app.get("/reviews")
def review_history(
    current_user: dict = Depends(get_current_user),
):
    return {
        "reviews": get_reviews(
            user_id=current_user["id"],
        ),
    }


@app.get("/progress", response_model=ProgressResponse)
def review_progress(
    current_user: dict = Depends(get_current_user),
):
    return get_review_progress(
        user_id=current_user["id"],
    )