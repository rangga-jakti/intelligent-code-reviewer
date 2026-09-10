from app.schemas import Finding

SEVERITY_PENALTIES = {
    "critical": 3.0,
    "high": 2.0,
    "medium": 1.0,
    "low": 0.5,
    "info": 0.1,
}

def calculate_quality_rating(findings: list[Finding]) -> float:
    penalty = sum(
        SEVERITY_PENALTIES.get(f.severity.lower(), 0.0)
        for f in findings
    )

    rating = max(1.0, 10.0 - penalty)
    return round(rating, 1)
