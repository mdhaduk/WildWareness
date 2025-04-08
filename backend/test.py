import json

def get_unique_counties(input_file):
    # Read the JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Extract counties and store them in a set (to ensure uniqueness)
    counties = set()
    for item in data:
        if 'county' in item:
            counties.add(item['county'])

    return counties


def add_county_to_data(input_file, output_file):
    # Read the JSON file
    with open(input_file, "r") as file:
        data = json.load(file)

    # Add county to each item in the data
    for item in data:
        # Logic to determine the county based on city (this can be expanded or adjusted)
        if 'city' in item:
            city = item['city']
            if city == 'Los Angeles':
                item['county'] = 'Los Angeles County'
            elif city == 'San Francisco':
                item['county'] = 'San Francisco County'
            else:
                item['county'] = 'Unknown County'

    # Write the updated data to a new file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

# Input and output file paths
input_file = 'data.json'  # Path to your input JSON file
output_file = 'updated_data.json'  # Path to output the updated JSON file

# Run the function to add county
add_county_to_data(input_file, output_file)
