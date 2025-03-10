from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
import sys
import json
import requests
import scripts.test as get_county_from_address
from models import Base, Wildfire, Shelter, NewsReport, TESTING
from dotenv import load_dotenv

DATABASE_URL = ""
if TESTING:
    DATABASE_URL = "sqlite:///test.db"
else:
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database_name = "homelessaid"
    DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@homelessaid-database.ctc8886awsgr.us-east-2.rds.amazonaws.com:5432/{database_name}"


# Note: The file this function relies on is not in the GIT repo b/c of its size, thus this won't work on a machine without the file
def addWildfires(local_session):
    allowed_keys = {"name", "county", "location", "year", "acres_burned", "url", "latitude", "longitude", "description"}
    with local_session() as ls:
        with open("fire_incidents.json", "r") as file:
            body = json.load(file)
            for wildfire in body:
                wildfire["year"] = str(wildfire["year"])
                wildfire["acres_burned"] = str(wildfire["acres_burned"])
                wildfire["latitude"] = str(wildfire["latitude"])
                wildfire["longitude"] = str(wildfire["longitude"])
                filtered_wildfire = {key: wildfire[key] for key in allowed_keys if key in wildfire}
                wildfireInstance = Wildfire(**filtered_wildfire)
                ls.add(wildfireInstance)
            ls.commit()

# Note: The file this function relies on is not in the GIT repo b/c of its size, thus this won't work on a machine without the file
def addShelters(local_session):
    with local_session() as ls:
        with open("shelters.json", "r") as file:
            body = json.load(file)
            for shelter in body:
                shelter["rating"] = str(shelter["rating"])
                shelterInstance = Shelter(**shelter)
                ls.add(shelterInstance)
            ls.commit()




def link(local_session):
    with local_session() as ls:
        # Assuming you have a session and engine setup
        wildfires = ls.query(Wildfire).all()
        shelters = ls.query(Shelter).all()

        for wildfire in wildfires:
            for shelter in shelters:
                wildfire_county = wildfire.county.lower().strip()
                shelter_county = get_county_from_address(shelter.address).replace(" county", "").strip()
                if wildfire.county == nonprofit.city:
                    # Check if the relationship already exists
                    if nonprofit not in shelter.nonprofits:
                        shelter.nonprofits.append(nonprofit)
        ls.commit()


def addNewsReports(local_session):
    allowed_keys = {"title", "description", "keywords", "snippet", "url", "image_url", "language", "published_at", "source", 
                    "categories", "author", "locations", "geo_locations", "map_urls", "reading_time", "socials", 
                    "text_summary", "related_articles", "hashtag_links", "images", "videos"}
    with local_session() as ls:
        with open("news_reports_data.json", "r") as file:
            body = json.load(file)
            for report in body:
                report["published_at"] = report["published_at"][0:10]
                report["categories"] = ", ".join(report["categories"])
                filtered_report = {key: report[key] for key in allowed_keys if key in report}
                reportInstance = NewsReport(**filtered_report)
                ls.add(reportInstance)
            ls.commit()


if __name__ == "__main__":
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    local_session = sessionmaker(bind=engine, autoflush=False, future=True)
    Base.metadata.create_all(bind=engine)
    if len(sys.argv) == 1:
        # addWildfires(local_session)
        addShelters(local_session)
        addNewsReports(local_session)
        # link(local_session)
    else:
        clear(local_session)
