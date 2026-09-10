from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    code: str = Field(min_length=1)
    language: str = "python"


class Finding(BaseModel):
    category: str
    severity: str
    line: int | None = None
    issue: str
    explanation: str
    suggestion: str
    historical_rule: str | None = None


class ReviewResponse(BaseModel):
    quality_rating: float
    summary: str
    findings: list[Finding]
    best_practices: list[str]
    optimizations: list[str]
