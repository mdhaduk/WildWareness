import requests
import time
import os
import json
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_KEY")

# Set of counties where we want to fetch homeless shelters
COUNTIES = {
    "Alameda",
    "Butte",
    "Calaveras",
    "Colusa",
    "Contra Costa",
    "El Dorado",
    "Fresno",
    "Glenn",
    "Imperial",
    "Inyo",
    "Kern",
    "Kings",
    "Lake",
    "Lassen",
    "Los Angeles",
    "Los Angeles, Ventura",
    "Madera",
    "Mariposa",
    "Mendocino",
    "Merced",
    "Modoc",
    "Mono",
    "Monterey",
    "Napa",
    "Placer",
    "Riverside",
    "Sacramento",
    "San Benito",
    "San Bernardino",
    "San Diego",
    "San Joaquin",
    "San Luis Obispo",
    "Santa Barbara",
    "Santa Clara",
    "Shasta",
    "Siskiyou",
    "Solano",
    "Sonoma",
    "Stanislaus",
    "Tehama",
    "Tulare",
    "Tuolumne",
    "Ventura",
    "Yuba"
}

# Generate queries based on county names
QUERIES = [f"homeless shelters in {county} County, CA" for county in COUNTIES]

def fetch_places(query, api_key, page_token=None):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "key": api_key}
    if page_token:
        params["pagetoken"] = page_token

    response = requests.get(url, params=params)
    return response.json()

def fetch_all_places_for_query(query, api_key):
    all_results = []
    page_token = None

    while True:
        data = fetch_places(query, api_key, page_token)
        if data.get("status") == "OK":
            all_results.extend(data.get("results", []))
            page_token = data.get("next_page_token")

            if not page_token or len(all_results) >= 10:
                break

            time.sleep(5)
        else:
            print(f"Error fetching data for query '{query}':", data.get("status"))
            break

    return all_results

def fetch_all_places(queries, api_key):
    all_results = []

    for query in queries:
        print(f"Fetching results for query: {query}")
        results = fetch_all_places_for_query(query, api_key)
        all_results.extend(results[:5])

        if len(all_results) >= 300:
            break

    return all_results[:300]

def fetch_place_details(place_id, api_key):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "key": api_key}
    response = requests.get(url, params=params)
    return response.json()

def get_shelter_image(place_id):
    photo_reference = get_photo_reference(place_id)
    if photo_reference:
        return get_photo_url(photo_reference)
    return None

def get_photo_reference(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {"place_id": place_id, "fields": "photos", "key": API_KEY}

    response = requests.get(url, params=params).json()
    photos = response.get("result", {}).get("photos", [])
    if photos:
        return photos[0].get("photo_reference")
    return None

def get_photo_url(photo_reference):
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo_reference}&key={API_KEY}"

def main():
    places_data = []
    places = fetch_all_places(QUERIES, API_KEY)

    for place in places:
        place_id = place.get("place_id")
        name = place.get("name", "N/A")
        address = place.get("formatted_address", "N/A")

        details = fetch_place_details(place_id, API_KEY)
        imageUrl = get_shelter_image(place_id)

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
            print(f"Error fetching details or image for {name}: {details.get('status')}")

    with open("shelters.json", "w", encoding="utf-8") as json_file:
        json.dump(places_data, json_file, indent=4, ensure_ascii=False)

    return places_data

if __name__ == "__main__":
    shelter_data = main()
    print(f"\nData saved to 'shelters.json'. Total shelters fetched: {len(shelter_data)}")
