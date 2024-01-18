# Snipey Python Tool

This Python tool, "Snipey", is designed to interact with a snipeit API to perform various operations. The tool can perform actions such as `watch`, `status`, `checkin`, `checkout`.

## Configuration

Before running the script, you need to set up a configuration file called `.config` in the same directory where the script is run. This file should have the following structure:

```
[user]
user_id = your_user_id (just a single number, like "1" without the quotes)

[api]
url = your_api_base_url
access_token = your_api_token
```

Replace `your_user_id`, `your_api_base_url` and `your_api_token` with appropriate values.

## Usage

Run the script from the command line using one of the following commands:

- `python snipey.py watch`

  This command will fetch the current status of the assets and keep watching for any changes in the asset status. It will display a message whenever there is a change in the status of any asset.

- `python snipey.py status`

  This command will fetch and print the current status of all assets.

- `python snipey.py checkin <asset_id>`

  This command will check-in the asset with the given asset_id.

- `python snipey.py checkout <asset_id>`

  This command will checkout the asset with the given asset_id.

## Requirements

This tool requires Python 3 and the following Python libraries:

- `requests`
- `urllib3`
- `configparser`
- `time`
- `sys`

Use pip to install any missing libraries.

```bash
pip install requests urllib3 configparser
```

