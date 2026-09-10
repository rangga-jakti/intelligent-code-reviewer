from app.services.rule_matcher import match_historical_rules


RULES = [
    {
        "id": "1",
        "type": "formatting",
        "description": "Avoid single-character variable names - they hurt readability",
    },
    {
        "id": "2",
        "type": "performance",
        "description": "Cache repeated database lookups inside the request loop",
    },
    {
        "id": "3",
        "type": "security",
        "description": "Never interpolate raw user input directly into SQL queries",
    },
]


def test_sql_injection_matches_security_rule():
    code = """
user_id = input("ID: ")
query = "SELECT * FROM users WHERE id = '" + user_id + "'"
"""

    findings = [
        {
            "category": "security",
            "issue": "SQL injection vulnerability",
            "explanation": "Raw user input is interpolated into SQL.",
        }
    ]

    matches = match_historical_rules(
        code,
        findings,
        RULES,
    )

    assert matches
    assert matches[0]["id"] == "3"


def test_irrelevant_rules_are_not_forced():
    code = """
def hello():
    return "hello"
"""

    findings = []

    matches = match_historical_rules(
        code,
        findings,
        RULES,
    )

    assert matches == []


def test_matches_are_sorted_by_score():
    code = """
user_id = input("ID: ")
query = "SELECT * FROM users WHERE id = '" + user_id + "'"
"""

    findings = [
        {
            "category": "security",
            "issue": "SQL injection",
            "explanation": "User input is used in SQL.",
        }
    ]

    matches = match_historical_rules(
        code,
        findings,
        RULES,
    )

    scores = [rule["score"] for rule in matches]

    assert scores == sorted(scores, reverse=True)

def test_sql_injection_finding_matches_historical_rule():
    code = """
user_id = input("ID: ")
query = "SELECT * FROM users WHERE id = '" + user_id + "'"
"""

    findings = [
        {
            "category": "security",
            "issue": "SQL injection risk",
            "explanation": (
                "The query concatenates user-supplied input "
                "directly into the SQL string."
            ),
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

    matches = match_historical_rules(
        code,
        findings,
        rules,
    )

    assert matches
    assert matches[0]["id"] == "3"