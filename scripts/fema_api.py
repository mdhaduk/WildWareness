import requests
import json

# FEMA API URL for disaster declarations (which includes shelter information)
url = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"

# Fetch data
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # Extract disaster summaries
    disasters = data.get("DisasterDeclarationsSummaries", [])

    # Filter for California using list comprehension
    ca_disasters = [d for d in disasters if d.get("state") == "CA"]

    # Pretty-print JSON results
    print(json.dumps(ca_disasters, indent=4))

else:
    print("Failed to fetch data. Status Code:", response.status_code)

