import json

from groq import Groq

from app.schemas import ReviewResponse


class CodeReviewer:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def review(
        self,
        code: str,
        language: str,
        historical_rules: list[dict[str, str]],
    ) -> ReviewResponse:

        rules = "\n".join(
            f"- Rule {rule["id"]} [{rule["type"]}]: {rule["description"]}"
            for rule in historical_rules
        )

        prompt = f"""
You are an expert software engineer, code reviewer, security analyst, and software architect.

Review the following {language} source code.

HISTORICAL REVIEW RULES:
{rules}

Use the historical rules as evidence when they are relevant to a finding.

IMPORTANT: Return ONLY valid JSON.

Use EXACTLY these top-level fields:
- quality_rating
- summary
- findings
- best_practices
- optimizations

Each finding MUST use this structure:
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
- quality_rating: number from 1 to 10
- findings: always an array
- best_practices: always an array
- optimizations: always an array
- historical_rule MUST contain the exact description from the historical rules when a rule supports the finding
- historical_rule MUST be null when no historical rule is relevant

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
                    "content": "You are an expert code reviewer. Follow the JSON schema exactly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )

        text = response.choices[0].message.content.strip()
        data = json.loads(text)

        return ReviewResponse(**data)
