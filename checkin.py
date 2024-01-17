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
user_id = config.get('user', 'user_id', fallback='1')  # Default to '1' if not found
api_base_url = config.get('api', 'url', fallback='https://default.api.url')  # Default API URL

# chekc correct number of arguments
if len(sys.argv) != 2:
    print("Usage: python checkin.py <asset_id>")
    sys.exit(1)

# get argumetns
asset_id = sys.argv[1]
api_url = f"{api_base_url}/{asset_id}/checkin"  # API URL

#read token
with open("api_token.txt", "r") as token_file:
    api_token = token_file.read().strip()

# define the data payload for checkin with a static status_id of 1
data = {
    "status_id": 2,  # Static Status ID "ready to deploy"
    "assigned_user": user_id,  # User ID from the config file
}

# make post requets
response = requests.post(api_url, headers={"Authorization": f"Bearer {api_token}"}, json=data, verify=False)

# check status/sccuess
if response.status_code == 200:
    print(f"Asset {asset_id} successfully checked in")
else:
    print(f"Error: Unable to check in asset. Status Code: {response.status_code}, Response: {response.text}")

