from app.services.rule_enrichment import (
    enrich_findings_with_historical_rules,
)


def test_sql_injection_finding_gets_historical_rule():
    code = """
user_id = input("ID: ")
query = "SELECT * FROM users WHERE id = '" + user_id + "'"
"""

    findings = [
        {
            "category": "security",
            "severity": "high",
            "line": 2,
            "issue": "SQL injection risk",
            "explanation": (
                "The query concatenates user-supplied input "
                "directly into the SQL string."
            ),
            "suggestion": "Use parameterized queries.",
            "historical_rule": None,
        }
    ]

    rules = [
        {
            "id": "3",
            "type": "security",
            "description": (
                "Never interpolate raw user input directly "
                "into SQL queries"
            ),
        }
    ]

    enriched = enrich_findings_with_historical_rules(
        code=code,
        findings=findings,
        historical_rules=rules,
    )

    assert len(enriched) == 1
    assert (
        enriched[0]["historical_rule"]
        == "Never interpolate raw user input directly into SQL queries"
    )


def test_unrelated_finding_keeps_historical_rule_null():
    code = """
def hello():
    return "hello"
"""

    findings = [
        {
            "category": "bug",
            "severity": "medium",
            "line": 2,
            "issue": "Example bug",
            "explanation": "An unrelated problem.",
            "suggestion": "Fix the problem.",
            "historical_rule": None,
        }
    ]

    rules = [
        {
            "id": "3",
            "type": "security",
            "description": (
                "Never interpolate raw user input directly "
                "into SQL queries"
            ),
        }
    ]

    enriched = enrich_findings_with_historical_rules(
        code=code,
        findings=findings,
        historical_rules=rules,
    )

    assert enriched[0]["historical_rule"] is None


def test_unrelated_same_category_rule_is_not_matched():
    code = """
query = "SELECT * FROM users WHERE id = %s"
"""

    findings = [
        {
            "category": "performance",
            "severity": "medium",
            "line": 1,
            "issue": "Unnecessary SELECT *",
            "explanation": (
                "Fetching all columns can increase I/O and memory usage."
            ),
            "suggestion": "Select only required columns.",
            "historical_rule": None,
        }
    ]

    rules = [
        {
            "id": "5",
            "type": "performance",
            "description": (
                "Avoid unnecessary nested loops when a more efficient "
                "approach exists"
            ),
        }
    ]

    enriched = enrich_findings_with_historical_rules(
        code=code,
        findings=findings,
        historical_rules=rules,
    )

    assert enriched[0]["historical_rule"] is None