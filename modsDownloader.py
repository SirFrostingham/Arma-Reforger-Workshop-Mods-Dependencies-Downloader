import argparse
import requests
import json
import re
import sys

def main(url, include_version, only_mods):
    if not url:
        print("Please provide a URL as an argument.")
        sys.exit(1)

    try:
        # Send an HTTP GET request and store the response
        response = requests.get(url)
        response.raise_for_status()

        # Extract the JSON data from the response content
        regex_pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
        match = re.search(regex_pattern, response.text)

        if match:
            json_string = match.group(1)
            json_data = json.loads(json_string)

            # Search for the "asset" information and store "id" and "name"
            asset = json_data['props']['pageProps']['asset']

            # Build a collection of "id" and "name" pairs
            dep_mods_set = set()

            # Add parent mod to the collection
            parent_mod = {
                "modId": asset['id'],
                "name": asset['name']
            }

            version = json_data['props']['pageProps']['asset']['currentVersionNumber']
            if include_version and version is not None:
                parent_mod["version"] = version

            dep_mods_set.add(json.dumps(parent_mod, sort_keys=True))

            # Search for the "dependencies" information
            dependencies = json_data['props']['pageProps'].get('assetVersionDetail', {}).get('dependencies', [])
            scenarioId = json_data['props']['pageProps'].get('assetVersionDetail', {}).get('scenarios', [{}])[0].get('gameId', None)
            playerCount = json_data['props']['pageProps'].get('assetVersionDetail', {}).get('scenarios', [{}])[0].get('playerCount', None)

            # Dependencies: Build a collection of "id" and "name" pairs
            for dep in dependencies:
                dep_asset = dep['asset']
                dep_mod = {
                    "modId": dep_asset['id'],
                    "name": dep_asset['name']
                }

                dep_version = dep.get('version', None)
                if include_version and dep_version is not None:
                    dep_mod["version"] = dep_version

                dep_mods_set.add(json.dumps(dep_mod, sort_keys=True))

                dep_dependencies = dep.get('dependencies', [])
                for dep_dep in dep_dependencies:
                    dep_dep_asset = dep_dep['asset']
                    dep_dep_mod = {
                        "modId": dep_dep_asset['id'],
                        "name": dep_dep_asset['name']
                    }

                    dep_dep_version = dep_dep.get('version', None)
                    if include_version and dep_dep_version is not None:
                        dep_dep_mod["version"] = dep_dep_version

                    dep_mods_set.add(json.dumps(dep_dep_mod, sort_keys=True))

                    dep_dep_dependencies = dep_dep.get('dependencies', [])
                    for dep_dep_dep in dep_dep_dependencies:
                        dep_dep_dep_asset = dep_dep_dep['asset']
                        dep_dep_dep_mod = {
                            "modId": dep_dep_dep_asset['id'],
                            "name": dep_dep_dep_asset['name']
                        }

                        dep_dep_dep_version = dep_dep_dep.get('version', None)
                        if include_version and dep_dep_dep_version is not None:
                            dep_dep_dep_mod["version"] = dep_dep_dep_version

                        dep_mods_set.add(json.dumps(dep_dep_dep_mod, sort_keys=True))

            # Output only the mods array if only_mods is specified
            if only_mods:
                mods_array = [json.loads(entry) for entry in dep_mods_set]
                print(json.dumps(mods_array, indent=4))
            else:
                # Output the full JSON structure
                output_data = {
                    "bindAddress": "",
                    "bindPort": 2001,
                    "publicAddress": "[EXTERNAL_SCRIPT_REPLACES_THIS]",
                    "publicPort": 2001,
                    "a2s": {
                        "address": "0.0.0.0",
                        "port": 17777
                    },
                    "game": {
                        "passwordAdmin": "CHANGEME",
                        "name": "[SERVER] TITLE",
                        "password": "",
                        "scenarioId": scenarioId,
                        "maxPlayers": playerCount,
                        "visible": True,
                        "crossPlatform": True,
                        "supportedPlatforms": ["PLATFORM_PC", "PLATFORM_XBL"],
                        "gameProperties": {
                            "serverMaxViewDistance": 2500,
                            "serverMinGrassDistance": 50,
                            "networkViewDistance": 1000,
                            "disableThirdPerson": False,
                            "fastValidation": True,
                            "battlEeye": True,
                            "VONDisableUI": False,
                            "VONDisableDirectSpeechUI": False
                        },
                        "mods": [json.loads(entry) for entry in dep_mods_set]
                    }
                }

                print(json.dumps(output_data, indent=4))

        else:
            print("JSON data not found on the page.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract JSON data from a website.")
    parser.add_argument("url", type=str, help="The URL of the website")
    parser.add_argument("--version", action="store_true", help="Include version information")
    parser.add_argument("--onlyMods", action="store_true", help="Output only the mods array")
    args = parser.parse_args()
    main(args.url, args.version, args.onlyMods)
