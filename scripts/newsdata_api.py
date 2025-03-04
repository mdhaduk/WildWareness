import requests
import json
from datetime import datetime, timedelta
import time

# Define API key (Replace with your actual API key from NewsData.io)
API_KEY = "4jJTsiWXz3Imehk8YIQCaeooLkdZdDaCaAO42WDa"

# Define API endpoint
url = "https://api.thenewsapi.com/v1/news/all"





articles_retrieved = set()
articles_all_data = []
# Function to fetch news
def fetch_news(api_url, query_params):
    # Send a GET request to the API
    response = requests.get(api_url, params=query_params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the list of articles from the response
        articles = data.get("data", [])

        # Process and display each article
        for article in articles:
            
            title = article.get("title", "No title available")
            if(title not in articles_retrieved):
                description = article.get("description", "No description available")
                source = article.get("source", "Unknown Source")
                published_at = article.get("published_at", "Unknown Date")
                url = article.get("url", "No URL available")
                categories = article.get("categories", [])

                print(f"🔹 Title: {title}")
                print(f"📰 Source: {source}")
                print(f"📅 Published At: {published_at}")
                print(f"🔗 Link: {url}")
                categories_string = ", ".join(categories)
                print(f"Categories: {categories_string}")
                print("=" * 80)
                articles_retrieved.add(title)
                articles_all_data.append(article)

        print(f"Length: {len(articles)}")

    else:
        # If the request was not successful, print the error code
        print(f"Error: Unable to fetch news (Status Code: {response.status_code})")

# Set the number of times you want to repeat the request
max_retries = 1  # Set a limit for the number of requests

# Start a loop to repeatedly send requests
i = 0
index = 0
search_queries = ["California+wildfires", "california+fires", "california+wildfires+emergency", 
                  "California+wildfires+shelters", "California+fires+disaster", "california+wildfires+rescue", 
                  "california+wildfires+homes", "California+wildfires+animals", "california+wildfires+firefighters", 
                  "california+destroyed+fires", "california+wildfires+people", "California+planes+wildfires", 
                  "california+wildfires+burned", "california+wildfires+aid", "california+wildfires+fatalities", 
                  "california+wildfires+displaced", "california+wildfires+lost", "california+wildfires+spread", 
                  "california+wildfires+destruction", "california+wildfires+land", "california+wildfires+government",
                   "california+wildfires+donations", "california+wildfires+volunteer", "california+wildfires+insurance",
                     "california+wildfires+relief", "california+wildfires+evacuation", "california+wildfires+climate",
                     "california+wildfires+news", "california+wildfires+smoke", "california+wildfires+pollution", 
                     "california+wildfires+debris", "california+wildfires+updates", "california+wildfires+containment",
                     "california+wildfires+prevention", "california+wildfires+rebuilding", "california+wildfires+restoration", 
                     "california+wildfires+assistance", "california+wildfires+forest", "california+wildfires+wildlife", 
                     "california+wildfires+impact", "california+wildfires+air", "california+wildfires+reports", "california+wildfires+causes", 
                     "california+wildfires+latest", "california+wildfires+zone", "california+wildfires+removal", "california+wildfires+resources",
                     "california+wildfires+programs", "california+wildfires+efforts", "california+wildfires+grief", "california+wildfires+funds", 
                     "california+wildfires+health", "california+wildfires+cost", "california+wildfires+warning", "california+wildfires+legal", 
                     "california+wildfires+management", "california+wildfires+aftermath", "california+wildfires+food", "california+wildfires+alerts", 
                     "california+wildfires+community", "california+wildfires+weather", "california+wildfires+environment", 
                     "california+wildfires+policy", "california+wildfires+fuel", "california+wildfires+drone", "california+wildfires+strategies", 
                     "california+wildfires+centers", "california+wildfires+county", "california+wildfires+preservation", 
                     "california+wildfires+housing", "california+wildfires+mental+health", "california+wildfires+history", "california+wildfires+catastrophe", 
                     "california+wildfires+affected", "california+wildfires+areas", "california+wildfires+companies", "california+wildfires+support", 
                     "california+wildfires+forecast", "california+wildfires+injuries", "california+wildfires+resilience", "california+wildfires+search", 
                     "california+wildfires+safety", "california+wildfires+robbery", "california+wildfires+outage", "california+wildfires+police", 
                     "california+wildfires+fear", "california+wildfires+season", "california+wildfires+heroes", "california+wildfires+families", 
                     "california+wildfires+risks", "california+wildfires+guidelines", "california+wildfires+orders", "california+wildfires+energy", 
                     "california+wildfires+tragedy", "california+wildfires+homeless", "california+wildfires+operations", "california+wildfires+local", 
                     "california+wildfires+organizations", "california+wildfires+missions", "california+wildfires+help", "california+wildfires+supplies", 
                     "california+wildfires+hazards", "california+wildfires+study", "california+wildfires+research", "california+wildfires+detection", 
                     "california+wildfires+technology", "california+wildfires+fundraising", "california+wildfires+danger", 
                     "california+wildfires+anger", "california+wildfires+service", "california+wildfires+teams", "california+wildfires+temperature", 
                     "california+wildfires+economy", "california+wildfires+businesses", "california+wildfires+humanitarian", 
                     "california+wildfires+fema", "california+wildfires+victims", "california+wildfires+international"]
while( index < len(search_queries)):
    print(f"Fetching news, attempt {i+1}...")
    # Define the query parameters including the API token and other filters
    params = {
        "api_token": API_KEY,  # Your API token
        "search": search_queries[index],
        "locale": "us",  # Fetch news from the US
        "language": "en", 
        "published_after": "2025-01-01",
    }
    fetch_news(url, params)
    index += 1
    i += 1
    # Pause for a while before sending the next request (e.g., 5 seconds)
    time.sleep(5)  # Wait for 5 seconds before making another request
print(len(articles_retrieved))
