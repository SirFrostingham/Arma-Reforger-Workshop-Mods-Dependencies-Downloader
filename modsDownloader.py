import argparse
import requests
import json
import re
import sys

def main(url, include_version):
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
            id_name_pairs = []

            # Add parent mod to the collection
            parent_mod = {
                "modId": asset['id'],
                "name": asset['name']
            }
            
            version = json_data['props']['pageProps']['assetVersionDetail'].get('version', None)
            if include_version and version is not None:
                parent_mod["version"] = version
            
            id_name_pairs.append(parent_mod)

            # Search for the "dependencies" information
            dependencies = json_data['props']['pageProps'].get('assetVersionDetail', {}).get('dependencies', [])
            scenarioId = json_data['props']['pageProps'].get('assetVersionDetail', {}).get('scenarios', [{}])[0].get('gameId', None)
            gameMode = json_data['props']['pageProps'].get('assetVersionDetail', {}).get('scenarios', [{}])[0].get('gameMode', None)
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

                id_name_pairs.append(dep_mod)

            # Output the collection of "id" and "name" pairs as JSON
            print("Mods list:")
            print(json.dumps(id_name_pairs, indent=4))

            # Output Scenario ID
            if scenarioId is not None:
                print(f"Scenario ID: {scenarioId}")
            if gameMode is not None:
                print(f"Game Mode: {gameMode}")
            if playerCount is not None:
                print(f"Player Count: {playerCount}")

        else:
            print("JSON data not found on the page.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract JSON data from a website.")
    parser.add_argument("url", type=str, help="The URL of the website")
    parser.add_argument("--version", action="store_true", help="Include version information")
    args = parser.parse_args()
    main(args.url, args.version)
