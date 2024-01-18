
# Asset Management Scripts

## Overview
This repository contains scripts for managing asset check-ins and check-outs using the Snipe-IT API. It includes functionality to check in and check out assets, monitor asset status, and retrieve asset information.

## Requirements
- Python 3.x
- `requests` library
- `urllib3` library
- `configparser` library

## Configuration
Create a `.config` file in the root directory with the following structure:

```ini
[user]
user_id = [Your_User_ID]

[api]
url = [Your_API_Endpoint]
```

Place your API token in a file named `api_token.txt` in the root directory.

## Scripts
- `checkin.py`: Check in an asset.
- `checkout.py`: Check out an asset.
- `retrieve_assets.py`: Retrieve a list of assets.
- `monitor_assets.py`: Continuously monitor and report changes in asset status.

## Usage
- Check in an asset: `python checkin.py <asset_id>`
- Check out an asset: `python checkout.py <asset_id>`
- Retrieve asset list: `python retrieve_assets.py`
- Monitor asset status: `python monitor_assets.py`
