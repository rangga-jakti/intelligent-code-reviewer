SUPPORTED_LANGUAGES = {
    "python": {
        "name": "Python",
        "extensions": [".py"],
        "focus": [
            "PEP 8 and readability",
            "Pythonic patterns",
            "exception handling",
            "security",
            "performance",
        ],
    },
    "javascript": {
        "name": "JavaScript",
        "extensions": [".js"],
        "focus": [
            "ESLint-style best practices",
            "async/await usage",
            "JavaScript security",
            "performance",
            "readability",
        ],
    },
    "sql": {
        "name": "SQL",
        "extensions": [".sql"],
        "focus": [
            "SQL injection prevention",
            "query performance",
            "index usage",
            "transaction safety",
            "query readability",
        ],
    },
}
def get_language_config(language: str) -> dict:
    normalized = language.strip().lower()
    if normalized not in SUPPORTED_LANGUAGES:
        supported = ", ".join(SUPPORTED_LANGUAGES.keys())
        raise ValueError(
            f"Unsupported language '{language}'. "
            f"Supported languages: {supported}"
        )
    return SUPPORTED_LANGUAGES[normalized]
