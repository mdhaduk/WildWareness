import requests
import time
import os
import json
import random
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_KEY")

# Set of counties where we want to fetch homeless shelters
COUNTIES = {
    "Alameda, Humboldt", "Los Angeles", "Mariposa", "Kings", "Tehama", "Lassen", "Shasta",
    "Lake", "Butte, Tehama", "Imperial", "Butte", "Mendocino", "Riverside, San Bernardino",
    "Colusa, Lake", "Napa", "Modoc", "Placer", "Stanislaus", "Sierra", "San Diego",
    "Trinity", "Alameda", "Humboldt, Trinity", "Colusa", "Marin", "Siskiyou", "Glenn",
    "Tuolumne", "Santa Clara", "Solano", "San Bernardino", "Yuba", "Los Angeles, San Bernardino",
    "Mono", "Riverside", "San Benito", "San Joaquin", "Nevada", "Alameda, San Joaquin",
    "Ventura", "Fresno", "Kern, Tulare", "Plumas", "Mariposa, Tuolumne", "San Luis Obispo",
    "Amador", "Humboldt", "Contra Costa", "Monterey", "El Dorado", "Sacramento", "Merced",
    "Santa Barbara", "Sonoma", "Kern", "Kern, San Luis Obispo", "Orange, Riverside",
    "Tulare", "Calaveras", "Madera", "Los Angeles, Ventura", "Inyo"
}

# Generate queries based on county names
QUERIES = [f"homeless shelters in {county} County, CA" for county in COUNTIES]

# Function to fetch places using the Text Search API
def fetch_places(query, api_key, page_token=None):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "key": api_key}
    if page_token:
        params["pagetoken"] = page_token

    response = requests.get(url, params=params)
    return response.json()

# Fetch all results with pagination for a single query
def fetch_all_places_for_query(query, api_key):
    all_results = []
    page_token = None

    while True:
        data = fetch_places(query, api_key, page_token)
        if data.get("status") == "OK":
            all_results.extend(data.get("results", []))
            page_token = data.get("next_page_token")

            if not page_token or len(all_results) >= 10:  # Limit per county to 10 shelters
                break

            time.sleep(2)  # Wait before requesting next page
        else:
            print(f"Error fetching data for query '{query}':", data.get("status"))
            break

    return all_results

# Fetch all results for multiple queries
def fetch_all_places(queries, api_key):
    all_results = []

    for query in queries:
        print(f"Fetching results for query: {query}")
        results = fetch_all_places_for_query(query, api_key)
        all_results.extend(results[:5])

        if len(all_results) >= 300:  # Stop at 300 shelters total
            break

    return all_results[:300]

# Function to fetch additional place details (phone, website, etc.)
def fetch_place_details(place_id, api_key):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "key": api_key}
    response = requests.get(url, params=params)
    return response.json()

# Fetch image for a shelter
def get_shelter_image(shelter_name, shelter_address):
    place_id = get_place_id(shelter_name, shelter_address)
    if place_id:
        photo_reference = get_photo_reference(place_id)
        if photo_reference:
            return get_photo_url(photo_reference)
    return None

# Fetch place_id for a shelter
def get_place_id(shelter_name, shelter_address):
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {"input": f"{shelter_name}, {shelter_address}", "inputtype": "textquery", "fields": "place_id", "key": API_KEY}

    response = requests.get(base_url, params=params).json()
    if "candidates" in response and response["candidates"]:
        return response["candidates"][0]["place_id"]
    return None

# Fetch photo reference from Place Details API
def get_photo_reference(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "fields": "photos", "key": API_KEY}

    response = requests.get(url, params=params).json()
    if "result" in response and "photos" in response["result"]:
        return response["result"]["photos"][0]["photo_reference"]
    return None

# Construct full photo URL
def get_photo_url(photo_reference):
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo_reference}&key={API_KEY}"

# Main function to collect and save data
def main():
    places_data = []
    places = fetch_all_places(QUERIES, API_KEY)

    for place in places:
        place_id = place.get("place_id")
        name = place.get("name", "N/A")
        address = place.get("formatted_address", "N/A")

        details = fetch_place_details(place_id, API_KEY)
        imageUrl = get_shelter_image(name, address)

        if details.get("status") == "OK" and imageUrl:
            details_result = details.get("result", {})
            phone = details_result.get("formatted_phone_number", "N/A")
            website = details_result.get("website", "N/A")
            rating = details_result.get("rating", "N/A")
            reviews = [review.get("text", "No review text available.") for review in details_result.get("reviews", [])]

            places_data.append({
                "name": name,
                "address": address,
                "phone": phone,
                "website": website,
                "rating": rating,
                "reviews": reviews,
                "imageUrl": imageUrl,
            })
        else:
            print(f"Error fetching details for {name}: {details.get('status')}")

    # Save results to a JSON file
    with open("shelters.json", "w", encoding="utf-8") as json_file:
        json.dump(places_data, json_file, indent=4, ensure_ascii=False)

    return places_data

# Run script
if __name__ == "__main__":
    shelter_data = main()
    print(f"\nData saved to 'shelters.json'. Total shelters fetched: {len(shelter_data)}")
