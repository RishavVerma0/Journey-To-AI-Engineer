import argparse
import requests
import json
import logging
import sys
from typing import Tuple
from pathlib import Path

# Configure logging settings
# If verbose mode is enabled, show DEBUG logs
def setup_logging(verbose: bool):

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=level
    )


# Function to get latitude and longitude from city name
# Uses Open-Meteo geocoding API
def get_coords(city: str) -> Tuple[float, float]:

    # API endpoint for geocoding
    url = "https://geocoding-api.open-meteo.com/v1/search"

    logging.debug(f"Geocoding city: {city}")

    try:
        # Send GET request to API
        r = requests.get(
            url,
            params={"name": city, "count": 1},
            timeout=5
        )

        # Raise error if request fails
        r.raise_for_status()

    except requests.RequestException as e:

        logging.error(f"Geocoding request failed: {e}")
        sys.exit(1)

    # Convert response JSON into Python dictionary
    results = r.json().get("results")

    # If no city found, exit program
    if not results:

        logging.error(f"City not found: {city}")
        sys.exit(1)

    # Return latitude and longitude
    return results[0]["latitude"], results[0]["longitude"]


# Function to fetch current weather using coordinates
def get_weather(lat: float, lon: float) -> dict:

    # Weather API endpoint
    url = "https://api.open-meteo.com/v1/forecast"

    # Query parameters for API request
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }

    logging.info(f"Fetching weather at ({lat:.2f}, {lon:.2f})")

    try:
        # Send request to weather API
        r = requests.get(url, params=params, timeout=5)

        # Raise error for bad response
        r.raise_for_status()

    except requests.RequestException as e:

        logging.error(f"Weather request failed: {e}")
        sys.exit(1)

    # Return weather data as dictionary
    return r.json()


# Function to save weather data into JSON file
def save_data(data: dict, filename: str):

    # Get current script directory
    current_dir = Path(__file__).parent

    # Create full file path
    file_path = current_dir / filename

    # Save JSON file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    logging.info(f"Saved weather data to {file_path}")


# Main function
# Handles CLI arguments and program execution
def main():

    # Create argument parser object
    parser = argparse.ArgumentParser(
        description="Fetch current weather"
    )

    # Required city argument
    parser.add_argument(
        "--city",
        required=True,
        help="City name"
    )

    # Optional output filename
    parser.add_argument(
        "--output",
        default="weather.json"
    )

    # Optional verbose logging flag
    parser.add_argument(
        "--verbose",
        action="store_true"
    )

    # Parse CLI arguments
    args = parser.parse_args()

    # Setup logger
    setup_logging(args.verbose)

    # Get coordinates from city name
    lat, lon = get_coords(args.city)

    # Fetch weather data
    data = get_weather(lat, lon)

    # Save data into JSON file
    save_data(data, args.output)

    # Extract temperature from API response
    temp = data.get("current_weather", {}).get("temperature")

    # Print temperature if available
    if temp is not None:

        print(f"🌡 {args.city}: {temp}°C")

    else:

        print("Temperature data unavailable")


# Entry point of the program
# Ensures script runs only when executed directly
if __name__ == "__main__":
    main()