import requests
import time
import random
import json

# API URL
url = "https://gis.data.cnra.ca.gov/api/download/v1/items/994d3dc4569640caadbbc3198d5a3da1/geojson?layers=0"


#This script pretty much just keeps trying to fetch data until it works using this method called "exponential backoff"

# Exponential backoff parameters
max_attempts = 5  # Maximum retry attempts
base_wait = 1  # Initial wait time in seconds (doubles each retry)

for attempt in range(max_attempts):
    try:
        response = requests.get(url, timeout=10)  # 10-second timeout

        if response.status_code == 200:
            geojson_data = response.json()

            # Save the full JSON data to a file
            file_name = "wildfire_data.json"
            with open(file_name, "w") as f:
                json.dump(geojson_data, f, indent=4)

            print(f"✅ Full JSON data saved to {file_name}")

            # Print only the first 1000 characters as a preview
            json_string = json.dumps(geojson_data, indent=4)
            print(json_string[:1000])  # Print only the first 1000 characters
            print("\n... (Full data saved to file) ...")

            break  # Exit loop if request succeeds
        else:
            print(f"⚠️ Received status {response.status_code}, retrying...")
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Request failed: {e}, retrying...")

    # Exponential backoff with jitter (randomized delay to prevent spikes)
    wait_time = base_wait * (2 ** attempt) + random.uniform(0, 0.5)
    print(f"⏳ Waiting {wait_time:.2f} seconds before retrying...")
    time.sleep(wait_time)
else:
    print("❌ Max retry attempts reached. Exiting.")
