import argparse
import requests
import json
import logging
import sys

from datetime import datetime
from dataclasses import dataclass, asdict

BASE_URL = "https://api.github.com/search/repositories"


@dataclass
class Repo:
    name: str
    full_name: str
    stars: int
    forks: int
    description: str
    url: str
    language: str


def setup_logging(log_file=None, verbose=False):
    level = logging.DEBUG if verbose else logging.INFO

    handlers: list[logging.Handler] = []
    handlers.append(logging.StreamHandler())

    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=level,
        handlers=handlers
    )


def fetch_repos(topic: str, count: int, sort: str) -> list[Repo]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-search-cli"
    }

    repos = []
    page = 1

    while len(repos) < count:
        per_page = min(30, count - len(repos))

        params = {
            "q": f"topic:{topic}",
            "sort": sort,
            "per_page": per_page,
            "page": page
        }

        logging.debug(f"Fetching page {page} ({per_page} repos)")

        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code == 403:
            logging.error("Rate limited by GitHub API. Try again later.")
            break

        if response.status_code != 200:
            logging.error(
                f"GitHub API error {response.status_code}: {response.text}"
            )
            break

        items = response.json().get("items", [])

        if not items:
            logging.warning("No more repositories found.")
            break

        for item in items:
            repos.append(
                Repo(
                    name=item["name"],
                    full_name=item["full_name"],
                    stars=item["stargazers_count"],
                    forks=item["forks_count"],
                    description=item.get("description") or "",
                    url=item["html_url"],
                    language=item.get("language") or "Unknown"
                )
            )

        page += 1

    return repos[:count]


def main():
    parser = argparse.ArgumentParser(
        description="Search GitHub repositories by topic"
    )

    parser.add_argument(
        "--topic",
        required=True,
        help="GitHub topic to search"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of repositories to fetch"
    )

    parser.add_argument(
        "--output",
        default="repos.json",
        help="Output JSON file"
    )

    parser.add_argument(
        "--log_file",
        default=None,
        help="Optional log file"
    )

    parser.add_argument(
        "--sort",
        choices=["stars", "forks", "updated"],
        default="stars",
        help="Sort repositories"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    setup_logging(args.log_file, args.verbose)

    logging.info(
        f"Searching GitHub topic='{args.topic}' count={args.count}"
    )

    try:
        repos = fetch_repos(args.topic, args.count, args.sort)

    except requests.RequestException as e:
        logging.error(f"Network error: {e}")
        sys.exit(1)

    payload = {
        "topic": args.topic,
        "count": len(repos),
        "fetched_at": datetime.utcnow().isoformat(),
        "repos": [asdict(repo) for repo in repos]
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    logging.info(
        f"Saved {len(repos)} repositories -> {args.output}"
    )

    for repo in repos:
        print(f"⭐ {repo.stars:>6}  {repo.full_name}")


if __name__ == "__main__":
    main()