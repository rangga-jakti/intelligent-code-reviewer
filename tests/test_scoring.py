from app.schemas import Finding
from app.services.scoring import calculate_quality_rating
def make_finding(severity: str) -> Finding:
    return Finding(
        category="security",
        severity=severity,
        line=1,
        issue="Test issue",
        explanation="Test explanation",
        suggestion="Test suggestion",
    )
def test_no_findings_returns_10():
    assert calculate_quality_rating([]) == 10.0
def test_high_finding_returns_8():
    findings = [make_finding("high")]
    assert calculate_quality_rating(findings) == 8.0
def test_high_and_low_returns_7_5():
    findings = [
        make_finding("high"),
        make_finding("low"),
    ]
    assert calculate_quality_rating(findings) == 7.5
def test_critical_finding_returns_7():
    findings = [make_finding("critical")]
    assert calculate_quality_rating(findings) == 7.0
def test_rating_never_below_1():
    findings = [make_finding("critical")] * 10
    assert calculate_quality_rating(findings) == 1.0
