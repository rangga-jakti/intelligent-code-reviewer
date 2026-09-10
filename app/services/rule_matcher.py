import re


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "avoid",
    "be",
    "can",
    "for",
    "from",
    "in",
    "inside",
    "it",
    "more",
    "never",
    "of",
    "on",
    "or",
    "over",
    "the",
    "to",
    "when",
    "where",
    "with",
}


def tokenize(text: str) -> set[str]:
    tokens = set(
        re.findall(
            r"[a-zA-Z0-9_]+",
            text.lower(),
        )
    )

    return tokens - STOP_WORDS


def match_historical_rules(
    code: str,
    findings: list[dict],
    historical_rules: list[dict[str, str]],
) -> list[dict[str, str]]:
    code_tokens = tokenize(code)

    finding_text = " ".join(
        " ".join(
            str(value)
            for key, value in finding.items()
            if key in {"category", "issue", "explanation"}
        )
        for finding in findings
    )

    finding_tokens = tokenize(finding_text)

    matched_rules = []

    for rule in historical_rules:
        rule_tokens = tokenize(
            f"{rule['type']} {rule['description']}"
        )

        relevant_tokens = code_tokens | finding_tokens

        score = len(
            rule_tokens & relevant_tokens
        )

        if score > 0:
            matched_rules.append(
                {
                    "id": rule["id"],
                    "type": rule["type"],
                    "description": rule["description"],
                    "score": score,
                }
            )

    matched_rules.sort(
        key=lambda rule: rule["score"],
        reverse=True,
    )

    return matched_rules