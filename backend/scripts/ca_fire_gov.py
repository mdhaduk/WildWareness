import requests
import json
import os
import folium
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google API Key + ID
API_KEY = os.getenv("GOOGLE_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

"""Fetches formatted address from Google Maps API given latitude and longitude."""
def getLocation(lat, lon):
    if lat is None or lon is None:
        return "Location not available"

    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["formatted_address"]  # Returns location name
    return "Error obtaining location"

"""
Fetches the first image URL for a given wildfire search term using Google Custom Search API.

:param search_term: The wildfire name or search keyword.
:return: URL of the first image found, or None if no image is found.
"""
def get_wildfire_image(search_term):
    # Construct the Google Custom Search API URL
    url = f"https://www.googleapis.com/customsearch/v1?q={search_term}&searchType=image&num=1&fileType=jpg&safe=active&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    try:
        # Make the request to Google API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        # Extract the first image URL
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["link"]  # Return the first image URL
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

# Function to extract and get information for fire incidents from passed in data
def get_fire_incidents(data, year, fires_data):
    for feature in data["features"]:
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})

        # Extract latitude and longitude
        coordinates = geometry.get("coordinates", [None, None])
        lon, lat = coordinates if len(coordinates) == 2 else (None, None)

        # Structure fire incident data and add to list
        fire_entry = {
            "id": properties.get("UniqueId", "N/A"),
            "name": properties.get("Name", "Unknown Fire"),
            "year": year,
            "county": properties.get("County", "Unknown County"),
            "latitude": lat,
            "longitude": lon,
            "location": getLocation(lat, lon),
            "acres_burned": properties.get("AcresBurned", "N/A"),
            "active": properties.get("IsActive", "False"),
            "url": get_wildfire_image(f'California {properties.get("Name", "Unknown Fire")} image'),
        }
        fires_data.append(fire_entry)
    # return fires_data

if __name__ == '__main__':
    # Fire incidents API 
    baseUrl = "https://www.fire.ca.gov/umbraco/api/IncidentApi/GeoJsonList"

    # Headers to prevent 403 errors
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
    }

    # Store formatted data
    fires_data = []
    total_fires = 0

    # Fetch data for years 2025, 2024, and 2023
    for year in range(2025, 2023, -1):
        response = requests.get(f"{baseUrl}?year={year}", headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()  # Convert JSON response
                if 'features' in data:
                    total_fires += len(data["features"])  # Count total fires
                    get_fire_incidents(data, year, fires_data)

            except requests.exceptions.JSONDecodeError:
                print(f"Failed to parse JSON for year {year}")
        else:
            print(f"Failed to retrieve data for year {year}: {response.status_code}")
    # Save the formatted data to a JSON file
    output_file = "fire_incidents.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(fires_data, file, indent=4)

    # Print formatted JSON and results to console
    print(json.dumps(fires_data, indent=4))
    print(f"✅ Total Fires Retrieved: {total_fires}")
    print(f"🔥 Data saved to {output_file}")