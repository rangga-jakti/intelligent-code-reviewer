from fastapi import FastAPI, HTTPException

from app.config import GROQ_API_KEY
from app.schemas import ReviewRequest, ReviewResponse
from app.services.database import get_reviews, init_db, save_review
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


@app.post("/review", response_model=ReviewResponse)
def review_code(request: ReviewRequest):
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
def review_history():
    return {
        "reviews": get_reviews(),
    }