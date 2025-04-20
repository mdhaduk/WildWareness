import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_KEY")


# Given address, use API to get geolocation and extract county
def get_county_from_address(address):
    # Get data
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(base_url, params=params)
    data = response.json()

    # Successful response
    if data["status"] == "OK":
        for component in data["results"][0]["address_components"]:
            # Get county name
            if "administrative_area_level_2" in component["types"]:
                return component["long_name"]
    return None  # County not found

# Get score for report based on search term and what is matched in the attributes
# Attributes are on card or on instance page
def score_model(model_report, term, attributes):
    term_words = term.split()
    def exact_match(report):
        for attribute in attributes:
            if (term is (getattr(report, attribute, "") or "").lower()):
                return True
        return False

    def exact_match_in_word(report):
        for attribute in attributes:
            if (term in (getattr(report, attribute, "") or "").lower()):
                return True
        return False

    def multi_match(report):
        for attribute in attributes:
            if (all(word in (getattr(report, attribute, "") or "").lower() for word in term_words)):
                return True
        return False

    def single_match(report):
        for attribute in attributes:
            if (any(word in (getattr(report, attribute, "") or "").lower() for word in term_words)):
                return True
        return False

    def score_report(report):
        # 1. Exact phrase match (same)
        if exact_match(report):
            return 4
        # 2. Exact phrase match (within word)
        elif exact_match_in_word(report):
            return 3
        # 3. All words present (not necessarily as phrase) in any order but still phrase
        elif multi_match(report):
            return 2
        # 4. Any one word present
        elif single_match(report):
            return 1
        # 5. No match
        return 0
    return score_report(model_report)
