#!/usr/bin/env python3

import sys
import requests
import urllib3
import configparser
import time
from datetime import datetime

# stupid youre not secure error supression nothing to see here
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_user_id(api_base_url, api_token):
    # remove the endpoint part from the base url
    api_base_url = api_base_url.rsplit('/', 1)[0]
    api_url = f"{api_base_url}/users/me"
    try:
        response = requests.get(api_url, headers={"Authorization": f"Bearer {api_token}"}, verify=False)
        if response.status_code == 200:
            return response.json().get("id")
        else:
            print(f"Error: Unable to retrieve user ID. Status Code: {response.status_code}")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"Error: Unable to connect to {api_base_url}. Please check the URL and your network connection.")
        sys.exit(1)
    except Exception as e:
        print(f"Error in request: {e}")
        sys.exit(1)

def read_config():
    config = configparser.ConfigParser()
    config.read('.config')
    api_base_url = config.get('api', 'url', fallback='https://default.api.url')
    api_token = config.get('api', 'access_token', fallback='')
    user_id = get_user_id(api_base_url, api_token)
    return user_id, api_base_url, api_token

def checkin(api_base_url, api_token, asset_id, user_id):
    api_url = f"{api_base_url}/{asset_id}/checkin"
    data = {"status_id": 2, "assigned_user": user_id}
    try:
        response = requests.post(api_url, headers={"Authorization": f"Bearer {api_token}"}, json=data, verify=False)
    except:
        print("Error in request--are you connected to the right network? did you go to the right place in teh .config?")
        sys.exit(1)
    if response.status_code == 200:
        print(f"Asset {asset_id} successfully checked in")
    else:
        print(f"Error: Unable to check in asset. Status Code: {response.status_code}, Response: {response.text}")

def checkout(api_base_url, api_token, asset_id, user_id):
    api_url = f"{api_base_url}/{asset_id}/checkout"
    data = {"status_id": 2, "checkout_to_type": "user", "assigned_user": user_id}
    try:
        response = requests.post(api_url, headers={"Authorization": f"Bearer {api_token}"}, json=data, verify=False)
    except:
        print("Error in request--are you connected to the right network? did you go to the right place in teh .config?")
        sys.exit(1)
    if response.status_code in [200, 201]:
        print(f"Asset {asset_id} successfully checked out to user ID {user_id}")
    else:
        print(f"Error: Unable to checkout asset. Status Code: {response.status_code}, Response: {response.text}")

def status(api_base_url, api_token):
    api_url = f"{api_base_url}"
    params = {"limit": 500, "offset": 0}
    try:
        response = requests.get(api_url, headers={"Authorization": f"Bearer {api_token}"}, params=params, verify=False, timeout=2)
    except requests.exceptions.ConnectionError:
        print(f"Error: Unable to connect to {api_base_url}. Please check the URL and your network connection.")
        sys.exit(1)
    except Exception as e:
        print(f"Error in request: {e}")
        sys.exit(1)
    if response.status_code == 200:
        data = response.json()
        for asset in data['rows']:
            asset_id = asset.get('id', 'Unknown ID')
            asset_tag = asset.get('asset_tag', 'Unknown Tag')
            assigned_to = asset.get('assigned_to')
            checkout_username = assigned_to.get('username', '') if assigned_to else ''
            checkout_person = assigned_to.get('name', '').split()[0] if assigned_to else ''
            print(f"{asset_id:<3} {asset_tag:<20} {checkout_person:<15} {checkout_username:<15}")
    else:
        print(f"Error: Unable to retrieve assets. Status Code: {response.status_code}")

def watch(api_base_url, api_token):
    api_url = f"{api_base_url}"
    def fetch_current_status():
        params = {"limit": 50, "offset": 0}
        try:
            response = requests.get(api_url, headers={"Authorization": f"Bearer {api_token}"}, params=params, verify=False)
        except:
            print("DISCONNECTED")
            sys.exit(1)
        if response.status_code == 200:
            return response.json().get('rows', [])
        else:
            print(f"Error: Unable to retrieve assets. Status Code: {response.status_code}")
            return []
    def print_asset_status(assets):
        for asset in assets:
            asset_id = asset.get('id', 'Unknown ID')
            asset_tag = asset.get('asset_tag', 'Unknown Tag')
            assigned_to = asset.get('assigned_to')
            checkout_person = assigned_to.get('name', 'Not Checked Out') if assigned_to else ''
            print(f"{asset_id:<3} {asset_tag:<20} {checkout_person:<15}")
    #second function for the updates in slightly different ofrmat
    def print_asset_status2(assets):
        for asset in assets:
            asset_id = asset.get('id', 'Unknown ID')
            asset_tag = asset.get('asset_tag', 'Unknown Tag')
            assigned_to = asset.get('assigned_to')
            checkout_person = assigned_to.get('username', 'Not Checked Out') if assigned_to else ''
            print(f"{asset_tag} {checkout_person}")

    initial_status = fetch_current_status()
    print_asset_status(initial_status)
    last_status = {asset['id']: asset.get('assigned_to') for asset in initial_status}
    try:
        while True:
            time.sleep(3)
            current_status = fetch_current_status()
            current_status_dict = {asset['id']: asset.get('assigned_to') for asset in current_status}
            for asset_id, assigned_to in current_status_dict.items():
                if asset_id in last_status and assigned_to != last_status[asset_id]:
                    current_time = datetime.now().strftime("%a %d-%b-%Y %I:%M %p")
                    print(f"{current_time}: ", end='')
                    print_asset_status2([asset for asset in current_status if asset['id'] == asset_id])
            last_status = current_status_dict
    except KeyboardInterrupt:
        print("goodybye world")

def main():
    if len(sys.argv) < 2:
        print("Usage: python snipey.py [watch|status|ci|co] [args]")
        print("ci and co are short for checkin and checkout")
        sys.exit(1)
    user_id, api_base_url, api_token = read_config()
    command = sys.argv[1]
    if command == "watch":
        watch(api_base_url, api_token)
    elif command == "status":
        status(api_base_url, api_token)
    elif command == "ci":
        if len(sys.argv) != 3:
            print("Usage: python snipey.py checkin <asset_id>")
            sys.exit(1)
        checkin(api_base_url, api_token, sys.argv[2], user_id)
    elif command == "co":
        if len(sys.argv) != 3:
            print("Usage: python snipey.py checkout <asset_id>")
            sys.exit(1)
        checkout(api_base_url, api_token, sys.argv[2], user_id)
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()

