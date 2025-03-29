import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_KEY")
def get_county_from_address(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    if data["status"] == "OK":
        for component in data["results"][0]["address_components"]:
            if "administrative_area_level_2" in component["types"]:
                return component["long_name"]
    return None  # County not found