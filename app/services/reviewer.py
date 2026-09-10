import json

from groq import Groq

from app.schemas import Finding, ReviewResponse
from app.services.language_config import get_language_config
from app.services.scoring import calculate_quality_rating


class CodeReviewer:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def review(
        self,
        code: str,
        language: str,
        historical_rules: list[dict[str, str]],
    ) -> ReviewResponse:

        language_config = get_language_config(language)

        language_name = language_config["name"]
        focus_areas = "\n".join(
            f"- {item}" for item in language_config["focus"]
        )

        rules = "\n".join(
            f"- Rule {rule['id']} [{rule['type']}]: {rule['description']}"
            for rule in historical_rules
        )

        prompt = f"""
You are an expert software engineer, code reviewer, security analyst, and software architect.

Review the following {language_name} source code.

LANGUAGE-SPECIFIC REVIEW FOCUS:
{focus_areas}

HISTORICAL REVIEW RULES:
{rules}

Use the historical rules as evidence when relevant.

IMPORTANT: Return ONLY valid JSON.

Use EXACTLY these top-level fields:
- summary
- findings
- best_practices
- optimizations

Do NOT return quality_rating. The application calculates it separately.

Each finding MUST use:
{{
  "category": "security",
  "severity": "high",
  "line": 1,
  "issue": "Short issue title",
  "explanation": "Why this is a problem",
  "suggestion": "How to fix it",
  "historical_rule": "Exact historical rule description or null"
}}

Rules:
- category: bug, security, performance, formatting, architecture, maintainability
- severity: critical, high, medium, low, info
- line: integer or null
- historical_rule must contain only the exact historical rule description, without Rule ID or type
- historical_rule must be null when no historical rule is relevant
- findings must always be an array
- best_practices must always be an array
- optimizations must always be an array

CODE:
```{language}
{code}
```
"""

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert code reviewer. "
                        "Follow the JSON schema exactly."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        text = response.choices[0].message.content.strip()
        data = json.loads(text)

        findings = [
            Finding(**finding)
            for finding in data.get("findings", [])
        ]

        data["findings"] = findings
        data["quality_rating"] = calculate_quality_rating(findings)

        return ReviewResponse(**data)