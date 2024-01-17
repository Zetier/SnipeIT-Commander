import requests
import urllib3
import sys
import configparser

# goaway stuipd errors
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
user_id = config.get('user', 'user_id', fallback='1')  # Default to '1' if not found (TST ADMIN FTW
api_base_url = config.get('api', 'url', fallback='https://default.api.url')  # Default API URL

# checks args
if len(sys.argv) != 2:
    print("Usage: python checkout.py <asset_id>")
    sys.exit(1)

# get argumetns
asset_id = sys.argv[1]
api_url = f"{api_base_url}/{asset_id}/checkout"  # API URL

#read token
with open("api_token.txt", "r") as token_file:
    api_token = token_file.read().strip()

data = {
    "status_id": 2,  # static Status ID
    "checkout_to_type": "user",  # checking out to a user
    "assigned_user": user_id,    # User ID from the config file
}

# Make a POST request to perform the checkout action
response = requests.post(api_url, headers={"Authorization": f"Bearer {api_token}"}, json=data, verify=False)

# Check if the request was successful
if response.status_code in [200, 201]:
    print(f"Asset {asset_id} successfully checked out to user ID {user_id}")
else:
    print(f"Error: Unable to checkout asset. Status Code: {response.status_code}, Response: {response.text}")

