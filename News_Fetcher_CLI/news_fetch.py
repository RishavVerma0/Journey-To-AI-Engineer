# I am trying to implement all the concepts that I have learnt in the 2nd week of my journey into a mini project.
# I am trying to create a CLI News Headline Fetcher.
# ============================================================
# news_fetch.py — CLI News Headline Fetcher
# ============================================================
# What this script does:
#   1. Takes user input from terminal (topic + count)
#   2. Calls NewsAPI to fetch real headlines
#   3. Saves results to a JSON file
#   4. Logs every important action to console + file
#
# How to run:
#   python news_fetch.py --topic AI --count 5
#   python news_fetch.py --topic cricket --count 10
#   python news_fetch.py --help
# ============================================================


# ── STEP 1: IMPORTS ─────────────────────────────────────────
# These are built-in Python modules (no install needed)
import json
import logging
import argparse
import os
from datetime import datetime
import requests
from dotenv import load_dotenv # type: ignore

# ── STEP 2: LOAD API KEY ─────────────────────────────────────
# load_dotenv() reads your .env file and makes its values
# available via os.getenv()
#
# Create a file called .env in the same folder as this script
# and add this line inside it (no quotes):
#   NEWS_API_KEY=your_actual_key_here
#
# Get your free key at: https://newsapi.org/register
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")


# ── STEP 3: SETUP LOGGING ────────────────────────────────────
# logging lets you track what your script is doing
# Instead of using print() everywhere, use logger.info() / logger.error()
#
# We set up TWO handlers:
#   - FileHandler  → writes logs to news.log file
#   - StreamHandler → prints logs to your terminal
#
# Log levels (low to high):
#   DEBUG → INFO → WARNING → ERROR → CRITICAL
#   We use INFO so we see normal + error messages

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("news.log"),
        logging.StreamHandler()
    ]

)

logger= logging.getLogger(__name__)

# ── STEP 4: ARGPARSE — READ CLI FLAGS ────────────────────────
# argparse lets users pass options when running the script
# Example: python news_fetch.py --topic AI --count 5
#
# Think of this as creating a "menu" for your CLI tool

def get_args():

    # Create the argument parser with a description
    parser = argparse.ArgumentParser(
        description="Fetch Top News Headlines from NewsAPI",
        epilog="Example: python news_fetch.py -- topic AI --count 5"
    )

    # Add --topic flag
    # type=str means it expects text
    # default="technology" means if user doesn't pass it, use "technology"
    parser.add_argument(
        "--topic",
        type=str,
        default="technology",
        help="Topic to fetch news about (e.g. AI, sports, India, crypto)"
    )

# Add --count flag
    # type=int means it expects a number
    # default=5 means fetch 5 headlines if user doesn't specify
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of headlines to fetch(default: 5, max: 100)"
    )

    # parse_args() reads what the user typed in terminal
    return parser.parse_args()

# ── STEP 5: FETCH HEADLINES FROM NEWSAPI ─────────────────────
# This function makes the actual API call
# It takes topic and count as inputs
# It returns the raw JSON response from NewsAPI

def fetch_headlines(topic, count):
    # The NewsAPI endpoint we are calling
    url = "https://newsapi.org/v2/everything"

    # params are the query parameters added to the URL
    # NewsAPI needs: q (search term), pageSize, apiKey, etc.
    params = {
        "q": topic,
        "pageSize": count,
        "apiKey": API_KEY,
        "language": "en",
        "sortBy": "publishedAt"
    }

    logger.info(f"fetching headlines for the topic: '{topic}' | count: {count}")
    # try/except handles errors gracefully
    # Instead of crashing, we log the error and return None
    try:
        # requests.get() sends a GET request to the URL with params
        response = requests.get(url, params=params, timeout=10)

        # raise_for_status() raises an error if status code is 4xx or 5xx
        # e.g. 401 = bad API key, 429 = too many requests
        response.raise_for_status()

        logger.info(f"API responded with status code: {response.status_code}")

    # .json() converts the response text into a Python dictionary
        return response.json()
    
    except requests.exceptions.ConnectionError:
        # This happens when there's no internet
        logger.error("Network Error: No Internet Connection. Please Check Your Internet Connection and Try Again.")
        return None
    
    except requests.exceptions.Timeout:
        # This happens when the API takes too long to respond
        logger.error("Request Timed Out: NewsAPI took too long to respond.")
        return None
    
    except requests.exceptions.RequestException as e:
        # This is a catch-all for any other request errors
        logger.error(f"An error occured while fecthing the request: {e}")
        return None
    

# ── STEP 6: PARSE + CLEAN THE RESPONSE ───────────────────────
# The raw API response has a LOT of fields we don't need
# This function picks only what matters and returns a clean list
def parse_articles(data):
    # data["articles"] is the list of articles from NewsAPI
    raw_articles = data.get("articles", [])

    # If no articles were found
    if not raw_articles:
        logger.warning("No articles found for the given topic in the API response.")
        return []
    
    cleaned = [] # our clean list of articles

    for article in raw_articles:
        # Skip articles with missing title or removed content
        if not article.get("title") or article.get("title") == "[Removed]":
            continue
        #Build a clean dictionary with only what we need
        cleaned.append({
            "title": article.get("title", "No Title"),
            "source": article.get("source", {}).get("name", "Unknown"),
            "author": article.get("author", "unknown"),
            "description": article.get("description", "No Description"),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", "")
        })

    logger.info(f"Parsed {len(cleaned)} valid articles")
    return cleaned

# ── STEP 7: SAVE RESULTS TO JSON FILE ────────────────────────
# This function saves the cleaned articles to a JSON file
# The filename includes topic + timestamp so files don't overwrite each other
def save_to_json(articles, topic):
    # Create a timestamp like: 20250522_1430
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # Build the filename using topic + timestamp
    filename = f"news_{topic}_{timestamp}.json"

    # Build the final output structure
    output = {
        "topic": topic,
        "fetched_at": datetime.now().isoformat(),
        "total_results": len(articles),
        "articles": articles
    }

    # Open the file and write JSON to it
    # indent=2 makes the JSON readable (pretty printed)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    logger.info(f"Results saved to: {filename}")
    return filename

# ── STEP 8: PRINT HEADLINES TO TERMINAL ──────────────────────
# This function prints the results in a clean readable format
def print_headlines(articles, topic):
    print("\n" + "=" * 55)
    print(f" Top {len(articles)} Headlines for: {topic.upper()}")
    print("=" * 55)

    for i, article in enumerate(articles, start=1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Author: {article['author']}")
        print(f"   Description: {article['description']}")
        print(f"   URL: {article['url']}")
        print(f"   Published At: {article['published_at']}")

    print("\n" + "=" * 55 + "\n")
    
# ── STEP 9: MAIN FUNCTION — CONNECTS EVERYTHING ──────────────
# This is the entry point of the script
# It calls all the functions in the right order

def main():
    logger.info("=" * 40)
    logger.info("Script Started")

    # Step 1: Get user input from CLI
    args = get_args()
    topic = args.topic
    count = args.count

    # Validate Count - NewsAPI max is 100

    if count < 1 or count > 100:
        logger.warning("Count exceeds Limits: Count must be between 1 and 100.")
        count = 100

    # Step 2: Check API Key Exists
    if not API_KEY:
        logger.error("NEWS_API_KEY not found. Please set it in your .env file")
        logger.error("Get your free key at: https://newsapi.org/register")
        return  # exit the function early
    
    # Step 3: fetch from NewsAPI
    data = fetch_headlines(topic , count)
    if data is None:
        logger.error("Failed to fetch data from NewsAPI. Exiting.")
        return
    #Step 4: Parse the response
    articles = parse_articles(data)
    if not articles:
        logger.error("No valid articles to show. Try a different topic.")
        return
    

    # Step 5: Print to terminal
    print_headlines(articles, topic)

    # Step 6: Save to JSON file
    saved_file = save_to_json(articles, topic)

    logger.info(f"Done! {len(articles)} articles fetched and saved to {saved_file}")
    logger.info("=" * 40)

# ── ENTRY POINT ──────────────────────────────────────────────
# This block runs only when you execute the script directly
# It will NOT run if another script imports this file
# This is a Python best practice — always wrap main() like this

if __name__ == "__main__":
    main()   
    