#!/usr/bin/env python3
import sys
import os

# Add the parent directory to the path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text

def add_county_column():
    """
    Add a county column to the shelters table if it doesn't already exist.
    """
    # Create database connection
    engine = create_engine('sqlite:///test.db')
    
    # Connect to the database
    conn = engine.connect()
    
    try:
        # Check if the county column already exists
        result = conn.execute(text("PRAGMA table_info(shelters)")).fetchall()
        columns = [row[1] for row in result]
        
        if 'county' not in columns:
            # Add the county column
            conn.execute(text("ALTER TABLE shelters ADD COLUMN county TEXT"))
            print("County column added to shelters table")
        else:
            print("County column already exists in shelters table")
    except Exception as e:
        print(f"Error adding county column: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_county_column() 