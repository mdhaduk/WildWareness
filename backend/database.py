from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
import sys
import json
import requests
from models import Base, Wildfire, TESTING
from dotenv import load_dotenv

DATABASE_URL = ""
if TESTING:
    DATABASE_URL = "sqlite:///test.db"
else:
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database_name = "homelessaid"
    DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@homelessaid-database.ctc8886awsgr.us-east-2.rds.amazonaws.com:5432/{database_name}"


def test(local_session):
    with local_session() as ls:
        wildfire_instance = Wildfire(
            name="Palisades Fire",
            county="Los Angeles",
            location="Southeast of Palisades Drive, Pacific Palisades",
            year="January 7, 2025, 10:30 AM UTC",
            acres_burned="23706.6",
            url = "https://Google.com"
        )
        ls.add(wildfire_instance)
        ls.commit()


def result(local_session):
    with local_session() as ls:
        wildfires = ls.query(Wildfire).all()
        for wildfire in wildfires:
            print("Instance:\n", json.dumps(wildfire.as_instance(), indent=2))

def clear(local_session):
    with local_session() as ls:
        ls.query(Wildfire).delete()  # Delete all rows in the Wildfire table
        ls.commit()
        ls.execute(text("VACUUM"))  # Optional: Optimize SQLite database, clears disk space? (chat)
        print("All wildfire records have been deleted.")

def get_wildfire_image(search_term):
    """
    Fetches the first image URL for a given wildfire search term using Google Custom Search API.

    :param search_term: The wildfire name or search keyword.
    :return: URL of the first image found, or None if no image is found.
    """
    # 🔑 Google API Key and Search Engine ID (CX)
    API_KEY = "AIzaSyDJPeWEbVWBXRGI_W3FIzqkffL41rQVuOA"
    SEARCH_ENGINE_ID = "86eaf6939b8ea4c4a"

    # Construct the Google Custom Search API URL
    url = f"https://www.googleapis.com/customsearch/v1?q={search_term}&searchType=image&num=1&fileType=jpg&safe=active&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    try:
        # Make the request to Google API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues
        data = response.json()

        # Extract the first image URL
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]["link"]  # Return the first image URL
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None



# Note: The file this function relies on is not in the GIT repo b/c of its size, thus this won't work on a machine without the file
def getWildfires(local_session):
    allowed_keys = {"name", "county", "location", "year", "acres_burned", "url"}
    with local_session() as ls:
        with open("fire_incidents.json", "r") as file:
            body = json.load(file)
            for wildfire in body:
                imageUrl = get_wildfire_image(f'California {wildfire["name"]}')
                if(imageUrl):
                    wildfire["year"] = str(wildfire["year"])
                    wildfire["acres_burned"] = str(wildfire["acres_burned"])
                    wildfire["url"] = imageUrl
                    filtered_wildfire = {key: wildfire[key] for key in allowed_keys if key in wildfire}
                    wildfireInstance = Wildfire(**filtered_wildfire)
                    ls.add(wildfireInstance)
            ls.commit()

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    local_session = sessionmaker(bind=engine, autoflush=False, future=True)
    Base.metadata.create_all(bind=engine)
    if len(sys.argv) == 1:
        getWildfires(local_session)
    else:
        clear(local_session)
