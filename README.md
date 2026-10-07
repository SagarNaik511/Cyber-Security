# Password Strength & Security Analyzer

An educational Flask web application that analyzes password strength in memory and generates unique passwords with Python's `secrets` module. It does not use a database, cookies, analytics, local storage, or third-party password APIs.

## Problem statement and objective

Weak and reused passwords remain a common cause of account compromise. This project demonstrates a transparent cybersecurity solution that detects common password weaknesses and gives actionable advice without collecting the password.

## Features

- Score from 0–100 with Very Weak, Weak, Moderate, Strong, and Very Strong classifications
- Length, character diversity, common-password, substitution, sequence, keyboard, date, and repetition checks
- Estimated entropy (a search-space estimate, not a cracking-time promise)
- Dynamic checklist and recommendations
- Secure 8–32 character generator with selectable character sets
- Responsive dark cybersecurity dashboard
- Flask JSON API and automated tests

## Technology and structure

Python, Flask, HTML5, CSS3, vanilla JavaScript, pytest, and the standard-library `secrets` module.

```text
password-security-analyzer/
├── app.py
├── analyzer/
│   ├── common_passwords.py
│   ├── password_analyzer.py
│   └── password_generator.py
├── templates/index.html
├── static/css/style.css
├── static/js/script.js
├── tests/test_analyzer.py
├── requirements.txt
└── PROJECT_REPORT.md
```

## Installation and running

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open <http://127.0.0.1:5000>. For production deployment, use a WSGI server and HTTPS; Flask's development server is for demonstrations only.

## API

- `GET /` serves the dashboard.
- `POST /api/analyze` accepts `{"password":"..."}` and returns score, strength, entropy, checks, warnings, and recommendations.
- `GET /api/generate?length=16&uppercase=true&lowercase=true&numbers=true&symbols=true` returns a generated password.

The API never logs or echoes submitted passwords. The browser also never writes them to local storage.

## Demonstration examples

- `password123`: Very Weak/Weak; common and predictable.
- `Password123`: Weak/Moderate; mixed case does not remove predictability.
- `P@ssword2026`: Moderate/Weak; substitutions and dates are predictable.
- `correct-horse-battery-staple`: Strong depending on context; unique, long passphrases are preferable.

## Testing

```powershell
pytest -q
```

Tests cover classifications, common passwords, repeated characters, sequences, entropy, length, and generator character requirements.

## Security considerations and future enhancements

This is a heuristic educational analyzer, not a breach checker or guarantee. A production extension could use a privacy-preserving k-anonymity breach service with explicit consent, stronger locale-aware corpora, rate limiting, Content Security Policy headers, and deployment behind HTTPS. Passwords must still never be stored or logged.
