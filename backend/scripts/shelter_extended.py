import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()
# Replace with your API key
API_KEY = os.getenv("GOOGLE_KEY")

# List of queries to cover different regions in California
QUERIES = [
    "homeless shelters in Los Angeles, CA",
    "homeless shelters in San Francisco, CA",
    "homeless shelters in San Diego, CA",
    "homeless shelters in Sacramento, CA",
    "homeless shelters in Oakland, CA",
    "homeless shelters in San Jose, CA",
    "homeless shelters in Fresno, CA",
    "homeless shelters in Long Beach, CA",
    "homeless shelters in Bakersfield, CA",
    "homeless shelters in Anaheim, CA"
]

# Function to fetch places using the Text Search API
def fetch_places(query, api_key, page_token=None):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": api_key
    }
    if page_token:
        params["pagetoken"] = page_token
    
    response = requests.get(url, params=params)
    return response.json()

# Function to fetch place details using the Place Details API
def fetch_place_details(place_id, api_key):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": api_key
    }
    response = requests.get(url, params=params)
    return response.json()

# Fetch all results with pagination for a single query
def fetch_all_places_for_query(query, api_key):
    all_results = []
    page_token = None
    
    while True:
        # Fetch a page of results
        data = fetch_places(query, api_key, page_token)
        
        if data.get("status") == "OK":
            all_results.extend(data.get("results", []))
            page_token = data.get("next_page_token")
            
            # If there's no next page, stop
            if not page_token:
                break
            
            # Wait for the next_page_token to become valid
            time.sleep(2)
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
        all_results.extend(results)
        
        # Stop if we have at least 100 results
        if len(all_results) >= 300:
            break
    
    return all_results[:300]  # Return exactly 100 results

# Main script
if __name__ == "__main__":
    # Fetch all places matching the queries
    places = fetch_all_places(QUERIES, API_KEY)
    
    # Process and print details for each place
    for i, place in enumerate(places, start=1):
        place_id = place.get("place_id")
        name = place.get("name", "N/A")
        address = place.get("formatted_address", "N/A")
        
        print(f"\nResult {i}: {name}")
        print("Address:", address)
        
        # Fetch and print detailed information
        details = fetch_place_details(place_id, API_KEY)
        if details.get("status") == "OK":
            details_result = details.get("result", {})
            phone = details_result.get("formatted_phone_number", "N/A")
            website = details_result.get("website", "N/A")
            rating = details_result.get("rating", "N/A")
            reviews = details_result.get("reviews", [])
            
            print("Phone:", phone)
            print("Website:", website)
            print("Rating:", rating)
            
            if reviews:
                print("Reviews:")
                for review in reviews:
                    author = review.get("author_name", "Anonymous")
                    text = review.get("text", "No review text available.")
                    print(f"- {author}: {text}")
        else:
            print("Error fetching details for this place:", details.get("status"))
    
    print(f"\nTotal places fetched: {len(places)}")