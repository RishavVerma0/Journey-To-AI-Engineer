# news_fetch.py — CLI News Headline Fetcher

A command-line tool that fetches real news headlines using NewsAPI, saves results as JSON, and logs every action to a file.

Built as part of Week 2 daily script practice — covers: `requests`, `argparse`, `json`, `logging`, `.env`

---

## What it does

- Accepts a topic and count from the terminal
- Calls NewsAPI and fetches real headlines
- Prints results cleanly in the terminal
- Saves results to a timestamped JSON file
- Logs all actions to `news.log`

---

## Setup

**1. Clone the repo and go into the folder**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install requests python-dotenv
```

**4. Get your free API key**

Go to https://newsapi.org/register and sign up. It's free.

**5. Create a `.env` file in the same folder**
```
NEWS_API_KEY=your_actual_key_here
```

---

## How to run

```bash
# Basic usage (defaults: topic=technology, count=5)
python news_fetch.py

# Custom topic and count
python news_fetch.py --topic AI --count 10
python news_fetch.py --topic cricket --count 3
python news_fetch.py --topic "climate change" --count 7

# See all options
python news_fetch.py --help
```

---

## Example output

```
=======================================================
  Top 5 headlines for: AI
=======================================================

1. OpenAI releases new model with improved reasoning
   Source : TechCrunch
   Published : 2025-05-22
   URL : https://techcrunch.com/...

2. Google DeepMind announces AlphaFold 3
   Source : The Verge
   Published : 2025-05-21
   URL : https://theverge.com/...
```

---

## Files generated

| File | Description |
|------|-------------|
| `news_fetch.py` | Main script |
| `news.log` | Log file (auto-created on first run) |
| `news_AI_20250522_1430.json` | Results saved with topic + timestamp |
| `.env` | Your API key (never commit this) |

---

## Concepts used

| Concept | Where |
|---------|-------|
| `argparse` | `--topic` and `--count` CLI flags |
| `requests` | GET call to NewsAPI |
| `json` | Parsing response + saving to file |
| `logging` | Console + file logging throughout |
| `dotenv` | Loading API key from `.env` safely |
| `datetime` | Timestamping saved files |

---

## .gitignore

Make sure your `.env` and log files are not pushed to GitHub:

```
.env
*.log
news_*.json
venv/
__pycache__/
```

---

*Week 2 — Day 5 script | AI Engineer roadmap*
