import requests
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set the API endpoint URL
api_url = "https://snipeit.yellow.anaconda/api/v1/hardware"

# Read the API token from the file
with open("api_token.txt", "r") as token_file:
    api_token = token_file.read().strip()

# Define query parameters to filter and limit asset results
params = {
    "limit": 50,  # Adjust the limit as needed
    "offset": 0,  # Start from the beginning
    # Add other query parameters here as needed
}

# Make a GET request to retrieve assets with the specified parameters
response = requests.get(api_url, headers={"Authorization": f"Bearer {api_token}"}, params=params, verify=False)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Process and display the retrieved assets as needed
    for asset in data['rows']:
        asset_id = asset.get('id', 'Unknown ID')
        asset_tag = asset.get('asset_tag', 'Unknown Tag')
        assigned_to = asset.get('assigned_to')
        checkout_username = assigned_to.get('username', '') if assigned_to else ''
        checkout_person = assigned_to.get('name', '').split()[0] if assigned_to else ''

        # Using formatted string for aligned output
        print(f"{asset_id:<3} {asset_tag:<20} {checkout_person:<15} {checkout_username:<15}")

else:
    print(f"Error: Unable to retrieve assets. Status Code: {response.status_code}")
