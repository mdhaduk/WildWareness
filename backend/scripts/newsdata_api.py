import requests
import json
from datetime import datetime, timedelta
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


# Define API key (Replace with your actual API key from NewsData.io)
API_KEY = "4jJTsiWXz3Imehk8YIQCaeooLkdZdDaCaAO42WDa"

# Define API endpoint
url = "https://api.thenewsapi.com/v1/news/all"

the_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Load the spaCy language model for NER
nlp = spacy.load("en_core_web_sm")

# Function to extract locations from text using spaCy NER
def extract_locations_from_text(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
    return locations

# Function to get the article text from a URL and extract locations
def get_locations_from_article_url(html, the_headers):
    try:
        # Fetch the content of the article page
        # response = requests.get(url, headers=the_headers)
        # response.raise_for_status()  # Ensure the request was successful
        
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract the article's text (You may need to customize this based on the website's structure)
        article_text = ""
        paragraphs = soup.find_all('p')  # Assuming the article's content is within <p> tags
        for p in paragraphs:
            article_text += p.get_text()
        
        # Extract locations from the article text
        locations = extract_locations_from_text(article_text)
        return locations
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}{response.status_code}")
        return []


def get_author_from_url(html, the_headers):
    try:
        # Fetch the content of the article page
        # response = requests.get(url, the_headers)
        # response.raise_for_status()  # Ensure we got a successful response
        
        # Parse the HTML content
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try to find the author in common meta tags or other HTML tags
        # Example 1: Search for <meta> tags with name or property="author"
        author = soup.find('meta', {'name': 'author'}) or soup.find('meta', {'property': 'author'})
        
        if author:
            return author.get('content')
        
        # Example 2: If not found in meta tags, try looking for a specific tag (e.g., <span> with a class for author)
        # You'll need to inspect the HTML of the page to know the correct tag/class
        author = soup.find('span', class_='author-class')  # Example class name (adjust based on the site)
        
        if author:
            return author.text.strip()
        
        # Example 3: Some websites may use a <div> or <a> tag for the author
        author = soup.find('div', class_='author-container')  # Adjust the class as needed
        
        if author:
            return author.text.strip()

        return "Author not found"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article: {e}{response.status_code}")
        return "Error fetching article"


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
                # Wait for the elements to load
                wait = WebDriverWait(driver, 10)  # Timeout after 10 seconds
                html_content = driver.page_source
                # Extract the author name
                # try:
                #     author_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "author-name")))
                #     author = author_element.text
                # except:
                #     author = "Author not found"
            # 
            if(response.status_code == 403 and html_content == None):
                pass
            # Only include article if it still exists (404 means the URL doesn't lead 
            # to existing article)
            if(title not in articles_retrieved and response.status_code != 404):
                html_content = response.content
                description = article.get("description", "No description available")
                source = article.get("source", "Unknown Source")
                published_at = article.get("published_at", "Unknown Date")
                
                image_url = article.get("image_url", "No image URL available")
                categories = article.get("categories", [])
                locations = get_locations_from_article_url(html_content, the_headers)
                # author = get_author_from_url(url, the_headers)
                article_obj = Article(url)
                article_obj.download()
                article_obj.parse()
                author_list = article_obj.authors
                
                author = source if len(author_list) == 0 else author_list[0]
                    
                print(f"🔹 Title: {title}")
                print(f"📰 Source: {source}")
                print(f"📅 Published At: {published_at}")
                print(f"🔗 Link: {url}")
                print(f"🔗 Image Link: {image_url}")
                categories_string = ", ".join(categories)
                print(f"Categories: {categories_string}")
                print("Locations: ", locations)
                print("Author: ", author)
                print("=" * 80)
                articles_retrieved.add(title)
                article["Locations"] = locations
                article["Author"] = author
                # Print the updated dictionary
                print(json.dumps(article, indent=4))
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
