import requests
from bs4 import BeautifulSoup

# Your Google API Key
API_KEY = "AIzaSyC1deWzacsm0jD7h3oLxKo_Bz7W5snxbVQ"

# URL of the webpage containing the list of shelters
shelter_url = 'https://www.californiawildfirelawyer.com/fire-damage-list-of-shelters/'

def scrape_shelters():
    """Scrapes the list of shelters from the given webpage."""
    response = requests.get(shelter_url)
    response.raise_for_status()  # Ensure request was successful

    soup = BeautifulSoup(response.text, 'html.parser')
    counties = soup.find_all('h2')

    shelters = []

    for county in counties:
        county_name = county.get_text(strip=True)
        for sibling in county.find_next_siblings():
            if sibling.name == 'h2':  # Stop at the next county
                break
            if sibling.name == 'h3':
                city_name = sibling.get_text(strip=True)
            if sibling.name == 'p':
                shelter_info = sibling.get_text(strip=True)
                shelters.append({
                    'county': county_name,
                    'city': city_name,
                    'shelter': shelter_info
                })
    
    return shelters


def check_google_shelter_status(shelter_name, city, county):
    """Uses Google Places API to check if a shelter is open or closed."""
    search_query = f"{shelter_name}, {city}, {county}"
    
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_query}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "results" in data and len(data["results"]) > 0:
        place_id = data["results"][0]["place_id"]
        
        # Fetch detailed place info
        details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,opening_hours&key={API_KEY}"
        details_response = requests.get(details_url)
        details_data = details_response.json()

        if "result" in details_data and "opening_hours" in details_data["result"]:
            is_open = details_data["result"]["opening_hours"].get("open_now", "Unknown")
            return "Open" if is_open else "Closed"
    
    return "Unknown"


# Run the script
shelters = scrape_shelters()

for shelter in shelters:
    status = check_google_shelter_status(shelter['shelter'], shelter['city'], shelter['county'])
    print(f"{shelter['shelter']} ({shelter['city']}, {shelter['county']}): {status}")
