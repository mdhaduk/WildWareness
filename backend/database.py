from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
import json
from models import Base, Wildfire, TESTING

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
            date="January 7, 2025, 10:30 AM UTC",
            acres_burned="23706.6",
            images= ["https://media.nbclosangeles.com/2025/01/05_swir-image-of-burning-fires-in-altadena_08jan2025_1041am_wv3.jpg?quality=85&strip=all&fit=8113%2C5613&w=775&h=436&crop=0"]
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


# Note: The file this function relies on is not in the GIT repo b/c of its size, thus this won't work on a machine without the file
def getWildfires(local_session):
    with local_session() as ls:
        with open("cleanwildfires.json", "r") as file:
            body = json.load(file)
            for wildfire in body:
                if wildfire["thumbnail_URL"]:
                    wildfire["counties_served"] = str(wildfire["counties_served"])
                    wildfireInstance = Wildfire(**wildfire)
                    ls.add(wildfireInstance)
            ls.commit()

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    local_session = sessionmaker(bind=engine, autoflush=False, future=True)
    Base.metadata.create_all(bind=engine)
    test(local_session)
    result(local_session)
    # clear(local_session)
    # getNonprofits(local_session)
    # getFoodBanks(local_session)
    # getShelters(local_session)
