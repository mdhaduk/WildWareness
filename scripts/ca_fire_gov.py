import requests
import geojson

#Google API for location
API_KEY = "AIzaSyC1deWzacsm0jD7h3oLxKo_Bz7W5snxbVQ"
def getLocation(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "results" in data:
        return data["results"][0]["formatted_address"] # Returns location name
    else:
        return "Error in obtaining location"
# GeoJSON endpoint
baseUrl = "https://www.fire.ca.gov/umbraco/api/IncidentApi/GeoJsonList"

# Headers to avoid 403 errors
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
}

responses = []
total_fires = 0
# Fetch data for years 2025 to 2024 (this will only run once for 2025)
for i in range(2025, 2022, -1):
    response = requests.get(f"{baseUrl}?year={i}", headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()  # Convert JSON directly instead of using `.text`
            responses.append(data)  # Append parsed JSON data
        except requests.exceptions.JSONDecodeError:
            print(f"Failed to parse JSON for year {i}")
    else:
        print(f"Failed to retrieve data for year {i}: {response.status_code}")

# Parsing the GeoJSON data
for data in responses:
    if 'features' in data:  # Check if 'features' exist
        total_fires += len(data["features"])  # Count fires
        for feature in data["features"]:
            properties = feature["properties"]
            print(f"Incident Name: {properties.get('Name', 'N/A')}")
            print(f"County: {properties.get('County', 'N/A')}")
            print(f"Acres Burned: {properties.get('AcresBurned', 'N/A')}")
            print(f"Containment: {properties.get('PercentContained', 'N/A')}%")
            print(f"Start Date: {properties.get('Started', 'N/A')}")
            print(f"Location: ({feature['geometry']['coordinates'][1]}, {feature['geometry']['coordinates'][0]})")
            print("-" * 40)

print(total_fires)

    