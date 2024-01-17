import requests
import urllib3
import configparser
import time

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# grab config from .config file
# >cat .config
# [user]
# user_id = 1
# 
# [api]
# url = https://snipeit.yellow.anaconda/api/v1/hardware

config = configparser.ConfigParser()
config.read('.config')
api_base_url = config.get('api', 'url', fallback='https://default.api.url')

# set url
api_url = f"{api_base_url}"

# read token
with open("api_token.txt", "r") as token_file:
    api_token = token_file.read().strip()

def fetch_current_status():
    """Fetch the current checkout status of all assets."""
    params = {"limit": 50, "offset": 0}
    response = requests.get(api_url, headers={"Authorization": f"Bearer {api_token}"}, params=params, verify=False)

    if response.status_code == 200:
        return response.json().get('rows', [])
    else:
        print(f"Error: Unable to retrieve assets. Status Code: {response.status_code}")
        return []

def print_asset_status(assets):
    """Print the checkout status of assets."""
    for asset in assets:
        asset_id = asset.get('id', 'Unknown ID')
        asset_tag = asset.get('asset_tag', 'Unknown Tag')
        assigned_to = asset.get('assigned_to')
        checkout_person = assigned_to.get('name', 'Not Checked Out') if assigned_to else ''
        print(f"{asset_id:<3} {asset_tag:<20} {checkout_person:<15}")

# store the initial status of all assets
initial_status = fetch_current_status()
print_asset_status(initial_status)
last_status = {asset['id']: asset.get('assigned_to') for asset in initial_status}

try:
    while True:
        time.sleep(3)  # dos that shti
        current_status = fetch_current_status()
        current_status_dict = {asset['id']: asset.get('assigned_to') for asset in current_status}

        for asset_id, assigned_to in current_status_dict.items():
            if asset_id in last_status and assigned_to != last_status[asset_id]:
                print(f"Status changed for Asset ID: {asset_id}")
                print_asset_status([asset for asset in current_status if asset['id'] == asset_id])
        
        last_status = current_status_dict
except KeyboardInterrupt:
    print("goodybye world")

