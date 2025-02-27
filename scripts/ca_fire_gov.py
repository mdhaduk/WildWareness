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
url = "https://www.fire.ca.gov/umbraco/api/IncidentApi/GeoJsonList?inactive=true"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "application/json",
}

# # Fetching the data
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parsing the GeoJSON data
    data = geojson.loads(response.text)
    
    # Accessing features
    for feature in data['features']:
        properties = feature['properties']
        print(f"Incident Name: {properties['Name']}")
        print(f"County: {properties['County']}")
        print(f"Acres Burned: {properties['AcresBurned']}")
        print(f"Containment: {properties['PercentContained']}%")
        print(f"Start Date: {properties['Started']}")
        print(f"Location: {getLocation(feature['geometry']['coordinates'][1],feature['geometry']['coordinates'][0])}")
        print("-" * 40)
else:
    print(f"Failed to retrieve data: {response.status_code}")
    