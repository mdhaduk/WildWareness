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


def score_model(model, term, attributes):
    term_words = term.split()
    def exact_match(report):
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
        # 1. Exact phrase match
        if exact_match(report):
            return 3
        # 2. All words present (not necessarily as phrase) in any order but still phrase
        elif multi_match(report):
            return 2
        # 3. Any one word present
        elif single_match(report):
            return 1
        # 4. No match
        return 0
    return score_report(model)
