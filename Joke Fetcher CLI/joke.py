import argparse, requests, json, logging, sys
from datetime import datetime 

CATEGORIES = ["programming", "general", "Knock-Konck", "dark", "pun", "misc"]

def setup_logging(verbose):
    logging.basicConfig(
        format = "%(asctime)s [%(levelname)s] %(message)s",
        level=logging.DEBUG if verbose else logging.INFO
    )

def fetch_joke(category: str) -> dict:
    url = f"https://v2.jokeapi.dev/joke/{category}"
    params = {"type": "single", "safe-mode": True}
    r = requests.get(url, params=params, timeout=8)
    r.raise_for_status()
    data = r.json()
    return{
        "id": data["id"],
        "category": data["category"],
        "joke": data["joke"],
        "fetched_at": datetime.utcnow().isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="Fetch jokes by category")
    parser.add_argument("--category", default="programming", choices=CATEGORIES, help="Joke Category")
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--output", default="jokes.json")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    setup_logging(args.verbose)

    jokes = []
    for i in range(args.count):
        logging.debug(f"Fetching joke {i+1}/{args.count}")
        try:
            jokes.append(fetch_joke(args.category))
        except requests.RequestException as e:
            logging.warning(f"Skipping joke {i+1}: due to {e}")

    if not jokes:
        logging.error("No jokes fetched. Exiting.")
        sys.exit(1)

    with open(args.output, "w") as f:
        json.dump({"count": len(jokes), "jokes": jokes}, f, indent=2)
    logging.info(f"saved {len(jokes)}, jokes -> {args.output}")
    

    for j, joke in enumerate(jokes, 1):
        print(f"\n[{j}] {joke['joke']}")

if __name__ == "__main__":
    main()
