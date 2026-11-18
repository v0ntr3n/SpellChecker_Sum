# SpellChecker & Text Summarizer

[![Live Demo](https://img.shields.io/badge/demo-vercel-000000?style=flat&logo=vercel)](https://examples-eight-pi.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A lightweight web application and REST API for **English spell checking** (with token-offset mapping and contextual replacement) and **extractive text summarization**, built with Python (Flask) and deployed serverless on Vercel.

🔗 **Live Demo:** [https://examples-eight-pi.vercel.app](https://examples-eight-pi.vercel.app)

---

## Features

- **Token-Preserving Spell Check (`/mistake`):** Identifies misspelled words against a curated English lexicon (`en.json`), maps normalized tokens back to their exact character positions, and returns both corrected text and word-level correction mappings.
- **Extractive Summarization (`/sumarize`):** Condenses long-form English paragraphs into concise summaries.
- **Zero-Build Web Interface (`Web.html`):** Interactive browser UI communicating directly with the Flask JSON endpoints.
- **Serverless Deployment:** Configured via `vercel.json` for instant deployment on Vercel Python Runtime.

---

## Project Structure

```text
SpellChecker_Sum/
├── api/
│   ├── index.py                  # Flask application & REST routes
│   ├── spellcheck/
│   │   ├── spellchecker.py       # Dictionary lookup & edit-distance candidate scorer
│   │   └── utils.py              # Token normalization & original-text reconstruction
│   └── sumarize/
│       └── summarize.py          # Extractive text summarization engine
├── Web.html                      # Interactive frontend interface
├── en.json                       # English frequency dictionary
├── requirements.txt              # Python dependencies
├── vercel.json                   # Vercel serverless routing configuration
└── LICENSE
```

---

## API Reference

### 1. Spell Check (`POST /mistake`)

**Request Body:**
```json
{
  "text": "Thiss is an exampel of mispeled text."
}
```

**Response:**
```json
{
  "response": "This is an example of misspelled text.",
  "corections": {
    "Thiss": "This",
    "exampel": "example",
    "mispeled": "misspelled"
  }
}
```

### 2. Text Summarization (`POST /sumarize`)

**Request Body:**
```json
{
  "text": "Long article or paragraph text to summarize..."
}
```

**Response:**
```json
{
  "summary": "Concise extracted summary..."
}
```

---

## Local Development

```bash
git clone https://github.com/v0ntr3n/SpellChecker_Sum.git
cd SpellChecker_Sum

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m api.index
```

## License

Released under the [MIT License](LICENSE).
