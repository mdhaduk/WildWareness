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
        
        # Stop if we have at least 300 results
        if len(all_results) >= 300:
            break
    
    return all_results[:300]  # Return exactly 100 results

# Main script
if __name__ == "__main__":
    # Fetch all places matching the queries
    places = fetch_all_places(QUERIES, API_KEY)
    shelter_data = []
    the_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    # Process and print details for each place
    for i, place in enumerate(places, start=1):
        shelter = {}
        place_id = place.get("place_id")
        # print(place)
        # name = place.get("name", "N/A")
        # address = place.get("formatted_address", "N/A")

        # print
        
        # print(f"\nResult {i}: {name}")
        # print("Address:", address)
        
        # Fetch and print detailed information
        details = fetch_place_details(place_id, API_KEY)
        # print(details)
        if details.get("status") == "OK":
            details_result = details.get("result", {})
            if details_result:
                shelter["place_id"] = place_id
                shelter["name"] = place.get("name", "N/A")
                shelter["address"] = place.get("formatted_address", "N/A")

                details_result = details.get("result", {})
                phone = details_result.get("formatted_phone_number", "N/A")
                shelter["phone_number"] = phone
                website = details_result.get("website", "N/A")
                shelter["website"] = website
                shelter["description"] = "N/A"
                rating = details_result.get("rating", "N/A")
                shelter["rating"] = rating
                reviews = details_result.get("reviews", [])
                total_user_ratings = details_result.get("user_ratings_total", "N/A")
                shelter["total_user_ratings"] = total_user_ratings
                details_geometry = details_result.get("geometry", {})
                # For embedded map in website. If not present, use provided google
                # maps url
                shelter["embedded_map_url"] = "N/A"
                if details_geometry:
                    latitude = details_geometry.get("location").get("lat")
                    longitude = details_geometry.get("location").get("lng")
                    map_url = f"https://www.google.com/maps?q={latitude},{longitude}&z=12&maptype=satellite"
                    shelter["embedded_map_url"] = map_url
                hours = details_result.get('opening_hours')
                if hours:
                    hours = hours.get("weekday_text")
                else:
                    shelter["hours"] = "N/A"
                shelter["google_maps_url"] = details_result.get('url')
                shelter["icon_image"] = details_result.get("icon", "N/A")
                shelter["city"] = "N/A"
                shelter["county"] = "N/A"
                # Indicates if the shelter is still open, not closed
                shelter["business_status"] = details_result.get("business_status", "N/A")
                address_components = details_result.get("address_components", [])
                for address_component in address_components:
                    if(address_component["types"][0] == "locality"):
                        shelter["city"] = address_component["long_name"]
                    if(address_component["types"][0] == "administrative_area_level_2"):
                        shelter["county"] = address_component["long_name"]
                photos_list = details_result.get("photos")
                photo_urls = []
                shelter["additional_images"] = []
                shelter["videos"] = []
                shelter["embedded_content"] = []
                shelter["socials"] = []
                if photos_list:
                    for photo in photos_list:
                        photo_reference = photo["photo_reference"]
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={API_KEY}"
                        # print(photo_url)
                        photo_urls.append(photo_url)
                # If there is no website, search the web for media
                if website == "N/A":
                    if len(photo_urls) < 4:
                        images = get_content(shelter["name"]+" shelter California", "image", num_results=4)
                        shelter["additional_images"] = images
                    videos = get_content(shelter["name"]+ " shelter California", "video", num_results=4)
                    shelter["videos"] = videos
                else:
                    # Send a GET request to the website
                    response = requests.get(website, the_headers)
                    session = requests.Session()
                    html_content = response.content
                    if(response.status_code == 403):
                        response = session.get(website, headers=the_headers)
                        html_content = response.content
                    if(response.status_code == 403):
                        # Set up ChromeOptions to run the browser in headless mode
                        chrome_options = Options()
                        chrome_options.add_argument("--headless")  # Ensure the browser window doesn't open
                        chrome_options.add_argument("--disable-gpu")  # Disables GPU acceleration (useful in headless mode)
                        # Initialize the WebDriver
                        driver = webdriver.Chrome(options=chrome_options)
                        element_present = EC.presence_of_element_located((By.ID, 'some_element_id'))
                        WebDriverWait(driver, 10).until(element_present)
                        html_content = driver.page_source
                    # Check if the request was successful
                    # if response.status_code !:
                        # print(f"Failed to retrieve {url}")
                        # Parse the HTML using BeautifulSoup
                    soup = BeautifulSoup(html_content, 'html.parser')
                    shelter["socials"] = get_social_media_links(soup)
                    img_urls, video_urls, iframe_video_urls = get_media_links(website, soup)
                    shelter["additional_images"] = img_urls
                    shelter["videos"] = video_urls
                    shelter["embedded_content"] = iframe_video_urls
                    # Assuming the article's body text is inside a <div> with a specific class
                    article_text = soup.find('div', {'class': 'article-body'})
                    if article_text != None:
                        article_text = article_text.get_text()
                    if article_text == None or len(article_text) == 0:
                        paragraphs = soup.find_all('p')
                        article_text = ' '.join([para.get_text() for para in paragraphs])
                    shelter["description"] = website_text_summarizer(article_text)
                    
                shelter["photo_urls"] = photo_urls
                hashtag_links = []
                keywords = ["california", "cali", "californiawildfires", "californiashelters"]
                if(shelter["city"] != "N/A"):
                    keywords.append(shelter["city"])
                if(shelter["county"] != "N/A"):
                    keywords.append(shelter["county"])
                if(shelter["name"] != "N/A"):
                    keywords.append(shelter["name"])
                for keyword in keywords:
                    keyword = keyword.replace(" ", "")     
                    twitter_link = f"https://twitter.com/hashtag/{keyword}"
                    facebook_link = f"https://www.facebook.com/hashtag/{keyword}"
                    hashtag_info = {"hashtag": keyword, "twitter_link": twitter_link, 
                                    "facebook_link": facebook_link}
                    hashtag_links.append(hashtag_info)
                    # if "california" not in keyword.lower() and keyword not in locations:
                    #     detailed_keyword = "california" + keyword
                    #     twitter_link = f"https://twitter.com/hashtag/{detailed_keyword}"
                    #     facebook_link = f"https://www.facebook.com/hashtag/{detailed_keyword}"
                    #     hashtag_info = {"hashtag": detailed_keyword, "twitter_link": twitter_link, 
                    #                 "facebook_link": facebook_link}
                        # hashtag_links.append(hashtag_info)
                shelter["hashtag_links"] = hashtag_links

                # print("Phone:", phone)
                # print("Website:", website)
                # print("Rating:", rating)
                
                if reviews:
                    shelter["reviews"] = reviews
                #     print("Reviews:")
                #     for review in reviews:
                        # author = review.get("author_name", "Anonymous")
                        # text = review.get("text", "No review text available.")

                        # print(f"- {author}: {text}")
                shelter_data.append(shelter)
            else:
                print("Error fetching details for this place:", details.get("status"))
    
    # print(f"\nTotal places fetched: {len(places)}")
    total_shelters = len(shelter_data)
    # Save the formatted data to a JSON file
    output_file = "shelters_data.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(shelter_data, file, indent=4)

    # Print formatted JSON to console
    print(json.dumps(shelter_data, indent=4))