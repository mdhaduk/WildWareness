import requests
import os
from dotenv import load_dotenv

# 🔑 Google API Key and Search Engine ID (cx)
API_KEY = "AIzaSyDJPeWEbVWBXRGI_W3FIzqkffL41rQVuOA"

SEARCH_ENGINE_ID = "86eaf6939b8ea4c4a"
SEARCH_TERM = "Oak Fire wildfire"

# Construct the Google Custom Search API URL
url = f"https://www.googleapis.com/customsearch/v1?q={search_term}&searchType=image&num=1&fileType=jpg&safe=active&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
# Make the request
response = requests.get(URL)
data = response.json()

print(data)
# Extract the first image URL
if "items" in data:
    image_url = data["items"][0]["link"]
    print("Wildfire Image URL:", image_url)
else:
    image_url = None
    print("No image found.")
