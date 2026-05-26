# 01 — Weather CLI

A beginner-friendly command-line tool that fetches current weather for any city using the **Open-Meteo API** (no API key required).

> **Learning focus:** `argparse` · `requests` · `json` · `logging` · error handling with `raise_for_status()`

---

## Project structure

```
01-weather-cli/
├── weather.py      # main script
├── requirements.txt    # dependencies
└── README.md
```

---

## Setup

```bash
# 1. Clone and navigate
git clone https://github.com/your-username/cli-practice-projects.git
cd cli-practice-projects/01-weather-cli

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
# Basic usage
python weather_cli.py --city "Mumbai"

# Save output to a custom file
python weather_cli.py --city "Delhi" --output delhi_weather.json

# Enable verbose/debug logging
python weather_cli.py --city "Bangalore" --verbose
```

### Arguments

| Argument | Type | Default | Description |
|---|---|---|---|
| `--city` | `str` | *(required)* | City name to look up |
| `--output` | `str` | `weather.json` | Output JSON filename |
| `--verbose` | flag | `False` | Show DEBUG-level logs |

---

## Example output

**Console:**
```
2025-01-15 10:23:01 INFO Fetching weather at (19.08, 72.88)
🌡  Mumbai: 31.2°C
```

**weather.json:**
```json
{
  "latitude": 19.08,
  "longitude": 72.88,
  "current_weather": {
    "temperature": 31.2,
    "windspeed": 14.5,
    "weathercode": 2,
    "time": "2025-01-15T10:00"
  }
}
```

---

## API used

[Open-Meteo](https://open-meteo.com/) — free, no API key needed.

- Geocoding endpoint: `https://geocoding-api.open-meteo.com/v1/search`
- Weather endpoint: `https://api.open-meteo.com/v1/forecast`

---

## Key concepts practised

- `argparse.ArgumentParser` — parsing CLI arguments
- `requests.get()` with `params=` — building query strings cleanly
- `r.raise_for_status()` — raising exceptions on HTTP errors
- `logging.basicConfig()` — setting log level and format
- `json.dump()` with `indent=2` — saving pretty-printed JSON
- `sys.exit(1)` — exiting with a non-zero code on failure

---

## Requirements

```
requests>=2.31.0
```