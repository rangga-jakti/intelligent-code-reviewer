1. Isi .env.example

Jalankan:

@'
GROQ_API_KEY=your_groq_api_key_here
'@ | Set-Content -Encoding UTF8 .env.example
2. Buat README portfolio-grade
@'
# 24/7 Intelligent Code Reviewer

AI-powered code quality and security analysis built with FastAPI, Groq, SQLite, and a lightweight web dashboard.

## Overview

The Intelligent Code Reviewer analyzes source code using an LLM-based review pipeline combined with historical engineering rules and deterministic quality scoring.

The system is designed to help developers identify security issues, maintainability problems, performance concerns, and coding best-practice violations before code reaches production.

## Features

- AI-powered code review
- Python, JavaScript, and SQL support
- Security, performance, maintainability, formatting, bug, and architecture findings
- Severity classification
- Line-level findings
- Historical engineering rule matching
- Historical-rule enrichment for explainable findings
- Deterministic quality scoring from 1.0 to 10.0
- User registration with API keys
- User-scoped review history
- Developer progress tracking
- Web dashboard
- SQLite persistence
- Automated test suite

## Architecture

```text
Web Dashboard
      |
      v
FastAPI API
      |
      +-------------------+
      |                   |
      v                   v
Authentication       Code Reviewer
                          |
              +-----------+-----------+
              |                       |
              v                       v
        Historical Rules          Groq LLM
              |                       |
              +-----------+-----------+
                          |
                          v
                  Quality Scoring
                          |
                          v
                       SQLite
                          |
              +-----------+-----------+
              |                       |
              v                       v
        Review History          Progress Tracking
Review Pipeline
Code Input
    |
Language Configuration
    |
Historical Rule Matching
    |
AI Code Review
    |
Finding Enrichment
    |
Deterministic Quality Scoring
    |
SQLite Persistence
    |
Dashboard Response
Tech Stack
Python
FastAPI
Groq API
Pydantic
SQLite
HTML
CSS
JavaScript
pytest
Project Structure
intelligent-code-reviewer/
├── app/
│   ├── auth.py
│   ├── config.py
│   ├── main.py
│   ├── schemas.py
│   └── services/
│       ├── database.py
│       ├── historical_rules.py
│       ├── language_config.py
│       ├── reviewer.py
│       ├── rule_enrichment.py
│       ├── rule_matcher.py
│       └── scoring.py
├── data/
│   └── historical_rules.csv
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
Setup
1. Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd intelligent-code-reviewer
2. Create a virtual environment

Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Configure the Groq API key

Create a .env file:

GROQ_API_KEY=your_groq_api_key_here

Never commit .env or expose the API key publicly.

5. Start the application
uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/
API
Register a user
POST /users

Example request:

{
  "username": "developer"
}

The API returns an application API key.

Review code
POST /review
X-API-Key: <application-api-key>

Example:

{
  "language": "python",
  "code": "def example():\n    return True"
}
Review history
GET /reviews
X-API-Key: <application-api-key>
Developer progress
GET /progress
X-API-Key: <application-api-key>
Quality Scoring

Quality is calculated deterministically from finding severity.

Higher-severity findings produce larger penalties.

Critical  → 3.0
High      → 2.0
Medium    → 1.0
Low       → 0.5
Info      → 0.1

The resulting score is bounded between 1.0 and 10.0.

This keeps the displayed quality rating explainable and independent from an arbitrary LLM-generated score.

Historical Rules

Historical engineering rules are stored in:

data/historical_rules.csv

The reviewer uses these rules as additional engineering context.

A rule is only attached to a finding when the application determines that the rule is sufficiently relevant.

This provides an explainability layer between the AI-generated finding and the engineering knowledge base.

Testing

Run the complete test suite:

pytest -q

Current test coverage includes:

API behavior
Authentication
User isolation
Review persistence
Progress tracking
Historical rule loading
Rule matching
Finding enrichment
Language configuration
Deterministic quality scoring
Security Notes
Groq credentials are loaded from environment variables.
.env is excluded from Git.
Review history is scoped by authenticated user.
SQL operations use parameterized queries.
Frontend rendering avoids inserting API-provided finding text directly as executable HTML.
Current Status

The application has been verified end-to-end locally:

Frontend
   ↓
FastAPI
   ↓
Groq AI
   ↓
Historical Rules
   ↓
Quality Scoring
   ↓
SQLite
   ↓
Review History
   ↓
Developer Progress

Automated test suite:

37 passed
Demo

A short product demonstration can show:

Opening the dashboard
Selecting a programming language
Submitting vulnerable code
AI-generated security findings
Historical engineering rule enrichment
Quality score
Review history
Developer progress
Roadmap

Potential future improvements:

Static analyzer integration such as Ruff, ESLint, and Semgrep
Improved finding deduplication
Confidence scoring
Diff-aware review
GitHub pull-request integration
Team-level analytics
Cloud deployment
Role-based access control
Feedback-driven review improvement
License

This project is intended as a portfolio and engineering demonstration project.
'@ | Set-Content -Encoding UTF8 README.md


### 3. Cek hasilnya

```powershell
Get-ChildItem README.md,.env.example | Select-Object Name,Length