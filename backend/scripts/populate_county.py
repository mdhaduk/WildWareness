#!/usr/bin/env python3
import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Shelter, Base
from scripts.test import get_county_from_address
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

def populate_county_data():
    """
    Populate the county field for all shelters in the database.
    This is a one-time operation to avoid API calls when loading shelter data.
    """
    # Create database connection
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Get all shelters
    shelters = session.query(Shelter).all()
    print(f"Found {len(shelters)} shelters")
    
    # Update county information
    for index, shelter in enumerate(shelters):
        try:
            if not shelter.county:  # Only update if county is not already set
                county = get_county_from_address(shelter.address)
                shelter.county = county
                print(f"[{index+1}/{len(shelters)}] Updated {shelter.name} with county: {county}")
                # Sleep briefly to avoid hitting API rate limits
                time.sleep(0.1)
        except Exception as e:
            print(f"Error processing {shelter.name}: {str(e)}")
    
    # Commit changes
    session.commit()
    print("County data population completed")

if __name__ == "__main__":
    populate_county_data() 