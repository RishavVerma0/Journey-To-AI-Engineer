# 02 — Joke Fetcher CLI

A command-line tool that fetches N jokes by category using the **JokeAPI** and saves them to JSON. Introduces the `--count` loop pattern central to all batch-fetch CLIs.

> **Learning focus:** looping requests · `--count` argument · `choices=` validation · skipping failures gracefully · `datetime` timestamps

---

## Project structure

```
02-joke-fetcher/
├── joke.py             # main script
├── requirements.txt    # dependencies
└── README.md
```

---

## Setup

```bash
cd cli-practice-projects/02-joke-fetcher

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## Usage

```bash
# Fetch 5 programming jokes (default)
python joke_fetch.py

# Fetch 3 jokes from a specific category
python joke_fetch.py --category dark --count 3

# Custom output file + verbose logging
python joke_fetch.py --category pun --count 10 --output puns.json --verbose
```

### Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `--category` | `str` | `programming` | Category: `programming`, `misc`, `dark`, `pun` |
| `--count` | `int` | `5` | Number of jokes to fetch |
| `--output` | `str` | `jokes.json` | Output JSON filename |
| `--verbose` | flag | `False` | Show DEBUG-level logs |

---

## Example output

**Console:**
```
2025-01-15 10:30:00 [INFO] Fetching joke 1/3
2025-01-15 10:30:01 [INFO] Fetching joke 2/3
2025-01-15 10:30:01 [INFO] Fetching joke 3/3
2025-01-15 10:30:02 [INFO] Saved 3 jokes → jokes.json

[1] Why do Java programmers wear glasses? Because they don't C#.
[2] A SQL query walks into a bar, walks up to two tables and asks... "Can I join you?"
[3] How many programmers does it take to change a light bulb? None — it's a hardware problem.
```

**jokes.json:**
```json
{
  "count": 3,
  "jokes": [
    {
      "id": 23,
      "category": "Programming",
      "joke": "Why do Java programmers wear glasses?...",
      "fetched_at": "2025-01-15T10:30:01.123456"
    }
  ]
}
```

---

## API used

[JokeAPI v2](https://v2.jokeapi.dev/) — free, no API key needed.

- Endpoint: `https://v2.jokeapi.dev/joke/{category}`

---

## Key concepts practised

- `for i in range(args.count)` — the batch-fetch loop pattern
- `choices=` in `add_argument()` — restricting valid values
- `try/except requests.RequestException` — skipping failed requests instead of crashing
- `logging.warning()` vs `logging.error()` — choosing the right level
- `datetime.utcnow().isoformat()` — adding timestamps to saved data
- `sys.exit(1)` — failing cleanly when zero results are fetched

---

## Requirements

```
requests>=2.31.0
```