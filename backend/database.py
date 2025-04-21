from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
import json
from scripts.helper_scripts import get_county_from_address
from models import Base, Wildfire, Shelter, NewsReport, TESTING
from dotenv import load_dotenv
from pathlib import Path
from collections import defaultdict

# Load environment variables
env_path = Path("/Users/milandhaduk/CS373/cs373-spring-2025-group-03/.env")
load_dotenv(dotenv_path=env_path)

# Set the database connection URL
DATABASE_URL = ""
if TESTING:
    DATABASE_URL = "sqlite:///test.db"
else:
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database_name = "wildfiredb"
    DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@wildwarenessdb.czwce00s2t3z.us-east-2.rds.amazonaws.com/{database_name}"


# Load wildfire data from JSON and insert into DB
def addWildfires(local_session):
    # Extract particular keys
    allowed_keys = {"name", "county", "location", "year", "acres_burned", 
                    "url", "latitude", "longitude", "description", "status"}

    with local_session() as ls:
        with open("fire_incidents.json", "r") as file:
            body = json.load(file)
            for wildfire in body:
                # Update any fields appropriately
                wildfire["year"] = str(wildfire["year"])
                wildfire["acres_burned"] = str(wildfire["acres_burned"])
                wildfire["latitude"] = str(wildfire["latitude"])
                wildfire["longitude"] = str(wildfire["longitude"])
                wildfire["status"] = "Active" if wildfire["active"] else "Inactive"

                filtered_wildfire = {key: wildfire[key] for key in allowed_keys if key in wildfire}
                wildfireInstance = Wildfire(**filtered_wildfire)
                ls.add(wildfireInstance)
            ls.commit()

# Load shelter data from JSON and insert into DB
def addShelters(local_session):
    with local_session() as ls:
        with open("shelters.json", "r") as file:
            body = json.load(file)
            for shelter in body:
                # Convert rating to string and modify if needed
                shelter["rating"] = str(shelter["rating"])
                if("N/A" in shelter["rating"]):
                    shelter["rating"] = "N/A"
                shelter["county"] = str(get_county_from_address(str(shelter["address"])))
                shelterInstance = Shelter(**shelter)
                ls.add(shelterInstance)
            ls.commit()

# Load news data from JSON and insert into DB
def addNewsReports(local_session):
    # Extract particular keys
    allowed_keys = {"title", "description", "url", "image_url", "published_at", "source", 
                    "categories", "author", "locations", "reading_time","text_summary", "county"}
    
    with local_session() as ls:
        with open("news_reports_data.json", "r") as file:
            body = json.load(file)
            for report in body:
                # Take the date of the field (not including time)
                report["published_at"] = report["published_at"][0:10]
                # Default to general category if no categories listed
                if(len(report["categories"]) == 0):
                    report["categories"] = "general"
                else:
                    report["categories"] = ", ".join(report["categories"])

                filtered_report = {key: report[key] for key in allowed_keys if key in report}
                reportInstance = NewsReport(**filtered_report)
                ls.add(reportInstance)
            ls.commit()

# Link wildfires, shelters, and news reports based on their county
def link(local_session):
    with local_session() as ls:
        # Fetch all wildfires, shelters, reports
        wildfires = ls.query(Wildfire).all()
        shelters = ls.query(Shelter).all()
        newsdatas = ls.query(NewsReport).all()

        # Create a dictionary mapping counties to wildfires
        wildfire_dict = defaultdict(list)
        for wildfire in wildfires:
            county = wildfire.county.lower().strip()
            wildfire_dict[county].append(wildfire)

        # Create a dictionary mapping counties to shelters
        shelters_dict = defaultdict(list)
        for shelter in shelters:
            county = get_county_from_address(str(shelter.address)).replace(" County", "").lower().strip()
            shelters_dict[county].append(shelter)

        # Link shelters to wildfires based on county
        for shelter in shelters:
            shelter_county = get_county_from_address(str(shelter.address))
            if not shelter_county:
                continue
            shelter_county = shelter_county.replace(" County", "").lower().strip()

            if shelter_county in wildfire_dict:
                for wildfire in wildfire_dict[shelter_county]:
                    if shelter not in wildfire.shelters:  # Prevent duplicates
                        wildfire.shelters.append(shelter)

        # Link news to wildfires based on county
        for news in newsdatas:
            news_county = news.county.lower().strip()
            if news_county in wildfire_dict:
                for wildfire in wildfire_dict[news_county]:
                    if news not in wildfire.newsreports:  # Prevent duplicates
                        wildfire.newsreports.append(news)

        # Link news to shelters based on county
        for news in newsdatas:
            news_county = news.county.lower().strip()
            if news_county in shelters_dict:
                for shelter in shelters_dict[news_county]:
                    if news not in shelter.newsreports:  # Prevent duplicates
                        shelter.newsreports.append(news)

        # Commit the changes
        ls.commit()



if __name__ == "__main__":
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    local_session = sessionmaker(bind=engine, autoflush=False, future=True)

    # Drop all tables in the database
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)

    # Populate data from local JSON files
    addWildfires(local_session)
    addShelters(local_session)
    addNewsReports(local_session)

    link(local_session)
