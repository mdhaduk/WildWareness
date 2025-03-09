import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from transformers import pipeline
from transformers import AutoTokenizer

import os
import json
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
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

# Your API key and Custom Search Engine ID (CX)
GOOGLE_API_KEY = os.getenv("GOOGLE_KEY_TWO")
CX = os.getenv("SEARCH_ENGINE_ID_TWO")


def google_search(query, search_type='web', num_results=3):
    # Base URL for Google Custom Search
    if(search_type == 'video'):
        query += " video"
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={CX}&num={num_results}'

    # Modify URL for images or videos based on search type
    if search_type == 'image':
        url += '&searchType=image'
    elif search_type == 'video':
        url += '&searchType=video'
    response = requests.get(url)
    return response.json()


def get_content(query, search_item, num_results=6):
    # images = []
    # videos = []
    media = []
    # Get images
    if(search_item == "image"):
        results = google_search(query, search_type='image', num_results=num_results)
        if 'items' in results:
            for item in results['items']:
                # if(item['link'] != image_url):
                media.append({
                    'title': item['title'],
                    'link': item['link'],
                    'image_url': item['link'],
                    'thumbnail': item['image']['thumbnailLink'] if 'image' in item else ''
                })
    # Get videos
    if(search_item == "video"):
        results = google_search(query, search_type='video', num_results=num_results)
        if 'items' in results:
            for item in results['items']:
                # if(item['link'] != image_url):
                media.append({
                    'title': item['title'],
                    'video_url': item['link'],
                    'snippet': item['snippet']
                })

    return media


def get_media_links(url, soup):
    # Find all image tags <img> and extract 'src' attributes (image URLs)
    img_tags = soup.find_all('img')
    img_urls = [urljoin(url, img['src']) for img in img_tags if 'src' in img.attrs]
    
    # Find all video tags <video> and extract 'src' attributes (video URLs)
    video_tags = soup.find_all('video')
    video_urls = [urljoin(url, video['src']) for video in video_tags if 'src' in video.attrs]
    
    # Find all iframe tags with embedded video sources (e.g., YouTube)
    iframe_tags = soup.find_all('iframe')
    iframe_video_urls = []
    for iframe in iframe_tags:
        if 'src' in iframe.attrs:
            iframe_url = iframe['src']
            if 'youtube' in iframe_url or 'vimeo' in iframe_url:  # Check for YouTube or Vimeo
                iframe_video_urls.append(urljoin(url, iframe_url))

    return img_urls, video_urls, iframe_video_urls


def get_social_media_links(soup):
    social_media_platforms = [
            'facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 'youtube.com', 'pinterest.com'
        ]
    # Find all anchor tags <a> with href attributes
    links = soup.find_all('a', href=True)
    # Filter out the social media links
    social_links = []
    for link in links:
        href = link['href']
        for platform in social_media_platforms:
            if platform in href and href not in social_links:
                social_links.append(href)
    return social_links


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

def website_text_summarizer(article_text):
    summarizer = pipeline('summarization', model = "sshleifer/distilbart-cnn-12-6")
    tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    # Model input can be at most 1024 at a time so do 1020 in case
    tokenized_text = tokenizer(article_text, truncation=True, max_length=1020, padding=False, return_tensors="pt")
    # Decode the truncated input back to text if needed (optional, but summarizer works with text)
    truncated_text = tokenizer.decode(tokenized_text['input_ids'][0], skip_special_tokens=True)
    word_count = len(truncated_text.split())
    min = 150
    if(word_count < min):
        min = word_count
    summary = summarizer(truncated_text, max_length=word_count, min_length=min, do_sample=False)
    final_summary = summary[0]['summary_text']
    return final_summary


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
        data = fetch_places(query, api_key, page_token)
        
        if data.get("status") == "OK":
            all_results.extend(data.get("results", []))
            page_token = data.get("next_page_token")
            
            if not page_token:
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
        all_results.extend(results)
        
        if len(all_results) >= 200:
            break  # Stop at 200 results
    
    return all_results[:300]

def get_place_id(shelter_name, shelter_address):
    """Fetch the place_id for a given shelter name and address."""
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": f"{shelter_name}, {shelter_address}",
        "inputtype": "textquery",
        "fields": "place_id",
        "key": API_KEY
    }
    
    response = requests.get(base_url, params=params).json()
    
    if "candidates" in response and response["candidates"]:
        return response["candidates"][0]["place_id"]
    else:
        print(f"Place ID not found for {shelter_name}.")
        return None

def get_photo_reference(place_id):
    """Fetch the photo_reference for a given place_id."""
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "photos",
        "key": API_KEY
    }
    
    response = requests.get(base_url, params=params).json()
    
    if "result" in response and "photos" in response["result"]:
        return response["result"]["photos"][0]["photo_reference"]
    else:
        return None

def get_photo_url(photo_reference):
    """Construct the image URL using the photo_reference."""
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo_reference}&key={API_KEY}"

def get_shelter_image(shelter_name, shelter_address):
    place_id = get_place_id(shelter_name, shelter_address)
    if place_id:
        photo_reference = get_photo_reference(place_id)
        # print(photo_reference)
        if photo_reference:
            return get_photo_url(photo_reference)
        else:
            return None
    else:
        return None

# Main function to collect and save data
def main():
    places_data = []

    # Fetch all places matching the queries
    places = fetch_all_places(QUERIES, API_KEY)

    for place in places:
        place_id = place.get("place_id")
        # print(place)
        name = place.get("name", "N/A")
        address = place.get("formatted_address", "N/A")

        # print
        
        # Fetch place details
        details = fetch_place_details(place_id, API_KEY)
        imageUrl = get_shelter_image(name,address)
        if details.get("status") == "OK" and imageUrl:
            details_result = details.get("result", {})
            phone = details_result.get("formatted_phone_number", "N/A")
            website = details_result.get("website", "N/A")
            rating = details_result.get("rating", "N/A")
            reviews = [review.get("text", "No review text available.") for review in details_result.get("reviews", [])]

            # Store data as dictionary
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

    # Save the results to a JSON file
    with open("shelters.json", "w", encoding="utf-8") as json_file:
        json.dump(places_data, json_file, indent=4, ensure_ascii=False)

    return places_data  # Return the collected data

# Run script
if __name__ == "__main__":
    shelter_data = main()
    print(f"\nData saved to 'shelters.json'. Total shelters fetched: {len(shelter_data)}")
