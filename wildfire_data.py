import json

# Load the JSON file
file_name = "wildfire_data.json"

with open(file_name, "r") as f:
    geojson_data = json.load(f)

# Extract features
features = geojson_data.get("features", [])  # Default to an empty list if "features" is missing

# Check how many features exist
print(f"✅ Total Features: {len(features)}")

# Extract key attributes from each feature
parsed_data = [
    {
        "ID": feature.get("id"),
        "Damage": feature["properties"].get("DAMAGE", "Unknown"),
        "Address": f"{feature['properties'].get('STREETNUMBER', '')} {feature['properties'].get('STREETNAME', '')} {feature['properties'].get('STREETTYPE', '')}".strip(),
        "City": feature["properties"].get("CITY", "Unknown"),
        "County": feature["properties"].get("COUNTY", "Unknown"),
        "Incident": feature["properties"].get("INCIDENTNAME", "Unknown"),
        "Coordinates": feature["geometry"].get("coordinates", "Unknown"),
    }
    for feature in features #List comprehension, will iterate over features(iterable) and filter based on the conditional below
    if "Affected" in feature["properties"].get("DAMAGE", "").strip()

]

# Print a small sample (first 5 items)
for i, item in enumerate(parsed_data[:5], start=1):
    print(f"\nFeature {i}:")
    print(json.dumps(item, indent=4))
