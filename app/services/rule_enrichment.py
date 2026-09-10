from app.services.rule_matcher import match_historical_rules


MIN_MATCH_SCORE = 3


def enrich_findings_with_historical_rules(
    code: str,
    findings: list[dict],
    historical_rules: list[dict[str, str]],
) -> list[dict]:
    enriched_findings = []

    for finding in findings:
        finding_copy = dict(finding)

        category = str(
            finding.get("category", "")
        ).lower()

        relevant_rules = [
            rule
            for rule in historical_rules
            if rule["type"].lower() == category
        ]

        if relevant_rules:
            matches = match_historical_rules(
                code=code,
                findings=[finding],
                historical_rules=relevant_rules,
            )

            strong_matches = [
                match
                for match in matches
                if match["score"] >= MIN_MATCH_SCORE
            ]

            if strong_matches:
                finding_copy["historical_rule"] = (
                    strong_matches[0]["description"]
                )

        enriched_findings.append(finding_copy)

    return enriched_findings