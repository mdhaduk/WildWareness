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
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import pytextrank
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer

# Load environment variables
load_dotenv()

# Define API key (Replace with your actual API key from NewsData.io)
API_KEY = os.getenv("NEWSDATA_KEY")

# Define API endpoint
url = "https://api.thenewsapi.com/v1/news/all"

the_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Load the spaCy language model for NER
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")


# Your API key and Custom Search Engine ID (CX)
GOOGLE_API_KEY = os.getenv("GOOGLE_KEY_TWO")
CX = os.getenv("SEARCH_ENGINE_ID_TWO")


def google_search(query, search_type='web', num_results=10):
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


def get_content(query, image_url, url, num_results=10):
    articles = []
    images = []
    videos = []

    # Get articles (default search type)
    results = google_search(query, search_type='web', num_results=num_results)
    if 'items' in results:
        for item in results['items']:
            if(item['link'] != url):
                articles.append({
                    'title': item['title'],
                    'snippet': item['snippet'],
                    'link': item['link']
                })
    # Get images
    results = google_search(query, search_type='image', num_results=num_results)
    if 'items' in results:
        for item in results['items']:
            if(item['link'] != image_url):
                images.append({
                    'title': item['title'],
                    'link': item['link'],
                    'image_url': item['link'],
                    'thumbnail': item['image']['thumbnailLink'] if 'image' in item else ''
                })
    # Get videos
    results = google_search(query, search_type='video', num_results=num_results)
    if 'items' in results:
        for item in results['items']:
            if(item['link'] != image_url):
                videos.append({
                    'title': item['title'],
                    'video_url': item['link'],
                    'snippet': item['snippet']
                })

    return articles, images, videos



def get_keywords_from_content(article_text):
    doc = nlp(article_text.lower())

    # Extract key phrases using TextRank
    key_phrases = [phrase.text for phrase in doc._.phrases]
    final_keywords = set()
    index = 0
    # find the keywords that only consist of nouns
    while index < len(key_phrases) and len(final_keywords) < 11:
        key_phrase = key_phrases[index]
        doc = nlp(key_phrase)
        if all(token.pos_ in ['NOUN', 'PROPN', 'ADJ'] for token in doc):
            final_keywords.add(key_phrase)
        index += 1

    # Display key phrases
    return final_keywords


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
    summary = summarizer(truncated_text, max_length=word_count, min_length=min, do_sample=False)
    final_summary = summary[0]['summary_text']
    return final_summary

def calculate_reading_time(article_text):
    word_count = len(article_text.split())
    reading_time = math.ceil(word_count / 200)   # Average reading speed of 200 words/min
    return reading_time

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
                description = article.get("description", "No description available")
                source = article.get("source", "Unknown Source")
                published_at = article.get("published_at", "Unknown Date")
                keywords = article.get("keywords", "")
                image_url = article.get("image_url", "No image URL available")
                categories = article.get("categories", [])
                # author = get_author_from_url(url, the_headers)
                article_obj = Article(url)
                article_obj.download()
                article_obj.parse()
                author_list = article_obj.authors
                
                author = source if len(author_list) == 0 else author_list[0]
                soup = BeautifulSoup(html_content, 'html.parser')

                # Assuming the article's body text is inside a <div> with a specific class
                article_text = soup.find('div', {'class': 'article-body'})
                if article_text != None:
                    article_text = article_text.get_text()
                if article_text == None or len(article_text) == 0:
                    paragraphs = soup.find_all('p')
                    article_text = ' '.join([para.get_text() for para in paragraphs])
                
                retrieved_locations = get_locations_from_article_url(article_text)
                locations = set()
                geo_locations_list = []
                map_urls = []
                geolocator = Nominatim(user_agent="location_detector")
                # Only take locations that have a valid geographical location
                for location in retrieved_locations:
                    geo_location = geolocator.geocode(location)
                    if geo_location:
                        # print(f"Geocoded {location}: {geo_location.raw}") 
                        display_name = geo_location.raw.get('display_name', "None").lower()
                        # state = address.get('state', '').lower()  # Get state and make it lowercase for comparison
                        
                        # Check if 'California' is part of the state
                        if 'california' in display_name:
                            old_size = len(locations)
                            locations.add(location.lower())
                            new_size = len(locations)
                            if(new_size > old_size):
                                geo_locations_list.append(geo_location.raw)
                                # z = zoom level, maptype-satellite, hybrid, roadmap, terrain
                                map_url = f"https://www.google.com/maps?q={geo_location.latitude},{geo_location.longitude}&z=12&maptype=satellite"
                                map_urls.append(map_url)
                        time.sleep(1)
                locations = list(locations)

                # related_articles = get_related_articles(soup)
                reading_time = calculate_reading_time(article_text)
                text_summary = article_text_summarizer(article_text)
                socials = get_social_media_links(soup)
                more_keywords = get_keywords_from_content(article_text)
                if(len(keywords) > 0):
                    keywords = set(keyword.strip().lower() for keyword in keywords.split(','))
                    keywords = keywords | more_keywords
                else:
                    keywords = more_keywords
                keywords = list(keywords)

                related_articles, images, videos = get_content(title, image_url, url, num_results=7)
                # Print articles
                # print("\nArticles:")
                # for i, art in enumerate(related_articles, start=1):
                #     print(f"{i}. Title: {art['title']}")
                #     print(f"   Link: {art['link']}")
                #     print(f"   Snippet: {art['snippet']}\n")

                # # Print images
                # print("\nImages:")
                # for i, image in enumerate(images, start=1):
                #     print(f"{i}. Title: {image['title']}")
                #     print(f"   Image URL: {image['image_url']}")
                #     print(f"   Thumbnail: {image['thumbnail']}\n")

                # # Print videos
                # print("\nVideos:")
                # for i, video in enumerate(videos, start=1):
                #     print(f"{i}. Title: {video['title']}")
                #     print(f"   Video URL: {video['video_url']}")
                #     print(f"   Snippet: {video['snippet']}\n")
                # print(f"🔹 Title: {title}")
                # print(f"📰 Source: {source}")
                # print(f"📅 Published At: {published_at}")
                # print(f"🔗 Link: {url}")
                # print(f"🔗 Image Link: {image_url}")
                # categories_string = ", ".join(categories)
                # print(f"Categories: {categories_string}")
                # print("Locations: ", locations)
                # print("Author: ", author)
                # print("Text Summary: ", text_summary)
                # # print("Related Articles: ", related_articles)
                # print("Estimated Reading Time: ", reading_time)
                # print("Socials: ", socials)
                print("=" * 80)
                articles_retrieved.add(title)
                article["search_query"] = params["search"]
                article["author"] = author
                
                if len(locations) > 0:
                    # The order of locations corrspond to order of geo_locations
                    # and map_urls (first location, first geo_location and first map_url
                    # correspond to the same location)
                    article["locations"] = locations 
                    article["geo_locations"] = geo_locations_list
                    article["map_urls"] = map_urls
                # If there is no location, default to California since
                # website is localized to wildfires in California
                else: 
                    article["locations"] = ["California"] 
                    geo_location = geolocator.geocode("California, United States")
                    article["geo_locations"] = [geo_location.raw]
                    map_url = f"https://www.google.com/maps?q={geo_location.latitude},{geo_location.longitude}&z=12&maptype=satellite"
                    article["map_urls"] = [map_url]
                # article["Related_Articles"] = related_articles
                article["reading_time"] = reading_time
                article["socials"] = socials
                if(len(text_summary.split()) < 15):
                    text_summary = "No summary, use description"
                article["text_summary"] = text_summary
                article["keywords"] = keywords
                article["related_articles"] = related_articles
                hashtag_links = []
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
                article["hashtag_links"] = hashtag_links
                article["images"] = images
                article["videos"] = videos


                # Print the updated dictionary
                # print(json.dumps(article, indent=4))
                articles_all_data.append(article)
        # print(f"Length: {len(articles)}")

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
while( index < 1):
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
print(json.dumps(articles_all_data, indent=4))

print(f"✅ Total Reports Retrieved: {total_reports}")
print(f"Data saved to {output_file}")