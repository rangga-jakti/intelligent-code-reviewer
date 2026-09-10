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
        historical_rules: list[str],
    ) -> ReviewResponse:

        rules = "\n".join(f"- {rule}" for rule in historical_rules)

        prompt = f"""
You are an expert software engineer, code reviewer, security analyst, and software architect.

Review the following {language} source code.

Historical review rules:
{rules}

IMPORTANT: Return ONLY valid JSON.
IMPORTANT: You MUST use EXACTLY these top-level fields:
- quality_rating
- summary
- findings
- best_practices
- optimizations

The JSON structure MUST be:
{{
  "quality_rating": 1,
  "summary": "Brief overall assessment",
  "findings": [
    {{
      "category": "security",
      "severity": "high",
      "line": 1,
      "issue": "Short issue title",
      "explanation": "Why this is a problem",
      "suggestion": "How to fix it"
    }}
  ],
  "best_practices": ["Recommendation"],
  "optimizations": ["Optimization recommendation"]
}}

Rules for findings:
- category must be one of: bug, security, performance, formatting, architecture, maintainability
- severity must be one of: critical, high, medium, low, info
- line must be an integer or null
- quality_rating must be between 1 and 10
- findings must always be an array
- best_practices must always be an array
- optimizations must always be an array
- If there are no findings, return an empty findings array

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
                    "content": "You are an expert code reviewer. Follow the requested JSON schema exactly."
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
