import requests
import json

# Define API key (Replace with your actual API key from NewsData.io)
API_KEY = "pub_6943866b817c01aa61a6ab1a3737e61fadd27"

# Define API endpoint
url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&q=California%20wildfires&country=us&category=environment&language=en"

# Define query parameters
params = {
    "apikey": API_KEY,
    "q": "California wildfires",  # Search for California wildfires
    "country": "us",  # Fetch news only from the US
    "category": "disaster",  # Filter for disaster-related news
    "language": "en",  # English articles only
}

# Make the request to NewsData.io
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    news_data = response.json()  # Convert response to JSON

    # Extract and display news articles
    articles = news_data.get("results", [])  # Extract the "results" field (list of articles)

    # Process and print each article in a structured way
    for article in articles:
        title = article.get("title", "No title available")
        source = article.get("source_id", "Unknown Source")
        publication_date = article.get("pubDate", "Unknown Date")
        link = article.get("link", "No link available")
        content = article.get("content", "No content available")

        print(f"🔹 Title: {title}")
        print(f"📰 Source: {source}")
        print(f"📅 Date: {publication_date}")
        print(f"🔗 Link: {link}")
        print("=" * 80)

else:
    print(f"Error: Unable to fetch news (Status Code: {response.status_code})")
