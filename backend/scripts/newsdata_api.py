import requests
import json
import time
from bs4 import BeautifulSoup
import spacy
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from transformers import pipeline
from geopy.geocoders import Nominatim
import math
from transformers import pipeline
import pytextrank
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer
from geopy.exc import GeocoderTimedOut

# Load environment variables
load_dotenv()

# Define API keys and ID
API_KEY = os.getenv("NEWSDATA_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_KEY_TWO")
CX = os.getenv("SEARCH_ENGINE_ID_TWO")

# Define API endpoint
url = "https://api.thenewsapi.com/v1/news/all"

the_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Load the spaCy language model for NER
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")


# Function to get the article text from a URL and extract locations
def get_locations_from_article_url(article_text):
    doc = nlp(article_text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
    return locations
    
def article_text_summarizer(article_text):
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
    final_summary = ""
    if min != 0 and word_count != 0:
        summary = summarizer(truncated_text, max_length=word_count, min_length=min, do_sample=False)
        final_summary = summary[0]['summary_text']
    return final_summary

def calculate_reading_time(article_text):
    word_count = len(article_text.split())
    reading_time = math.ceil(word_count / 200)   # Average reading speed of 200 words/min
    return reading_time


articles_retrieved = set()
articles_all_data = []
# Function to fetch news
def fetch_news(api_url, query_params):
    try:
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
                url = article.get("url", "No URL available")
                
                html_content = None
                response = requests.get(url, the_headers)
                html_content = response.content
                session = requests.Session()
                if(response.status_code == 403):
                    response = session.get(url, headers=the_headers)
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
                # If unable to open url skip article
                if(response.status_code == 403):
                    pass
                # Only include article if it still exists (404 means the URL doesn't lead 
                # to existing article)
                if(title not in articles_retrieved and response.status_code != 404):
                    html_content = response.content
                    source = article.get("source", "Unknown Source")
                    soup = BeautifulSoup(html_content, 'html.parser')
                    author = ""
                    article_obj = Article(url)
                    try:
                        article_obj.download(headers=the_headers)
                        if(article_obj.download_state != 403):
                            article_obj.parse()
                            author_list = article_obj.authors
                            if len(author_list) != 0:
                                author = author_list[0]
                    except:
                        # Search for meta tags with author information
                        author_meta = soup.find('meta', {'name': 'author'}) or soup.find('meta', {'property': 'article:author'})
                        if author_meta:
                            author = author_meta.get('content')
                    author = source if len(author) == 0 else author
                    

                    # Assuming the article's body text is inside a <div> with a specific class
                    article_text = soup.find('div', {'class': 'article-body'})
                    if article_text != None:
                        article_text = article_text.get_text()
                    if article_text == None or len(article_text) == 0:
                        paragraphs = soup.find_all('p')
                        article_text = ' '.join([para.get_text() for para in paragraphs])
                    
                    retrieved_locations = get_locations_from_article_url(article_text)
                    locations = set()
                    geolocator = Nominatim(user_agent="location_detector")
                    retries = 5  # Number of retries
                    # Only take locations that have a valid geographical location
                    for location in retrieved_locations:
                        try:
                            geo_location = geolocator.geocode(location, timeout=10)
                            if geo_location:
                                display_name = geo_location.raw.get('display_name', "None").lower()
                                # Check if 'California' is part of the state
                                if 'california' in display_name:
                                    locations.add(location.lower())

                            time.sleep(5)
                        except GeocoderTimedOut as e:
                            print(f"Geocoding timed out: {e}. Retrying ({i+1}/{retries})...")
                            time.sleep(5)  # Wait for 5 seconds before retrying

                    locations = list(locations)

                    reading_time = calculate_reading_time(article_text)
                    text_summary = article_text_summarizer(article_text)

                    articles_retrieved.add(title)
                    article["author"] = author
                    
                    if len(locations) > 0:
                        # The order of locations corrspond to order of geo_locations
                        # and map_urls (first location, first geo_location and first map_url
                        # correspond to the same location)
                        article["locations"] = locations 
                    # If there is no location, default to California since
                    # website is localized to wildfires in California
                    else: 
                        article["locations"] = ["California"] 
                        geo_location = geolocator.geocode("California, United States")
                    article["reading_time"] = reading_time
                    if(len(text_summary.split()) < 15):
                        text_summary = "No summary, use description"
                    article["text_summary"] = text_summary
                    articles_all_data.append(article)

        else:
            # If the request was not successful, print the error code
            print(f"Error: Unable to fetch news (Status Code: {response.status_code})")
    except:
        pass

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

total_reports = len(articles_all_data)
# Save the formatted data to a JSON file
output_file = "news_reports_data.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(articles_all_data, file, indent=4)

# Print formatted JSON to console
# print(json.dumps(articles_all_data, indent=4))

print(f"✅ Total Reports Retrieved: {total_reports}")
print(f"Data saved to {output_file}")