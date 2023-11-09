import argparse
import requests
import json
import re
import sys

def main(url):
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
            id_name_pairs.append({
                "modId": asset['id'],
                "name": asset['name']
            })

            # Search for the "dependencies" information
            dependencies = json_data['props']['pageProps']['assetVersionDetail']['dependencies']

            # Dependencies: Build a collection of "id" and "name" pairs
            for dep in dependencies:
                asset = dep['asset']
                id_name_pairs.append({
                    "modId": asset['id'],
                    "name": asset['name']
                })

            # Output the collection of "id" and "name" pairs as JSON
            print(json.dumps(id_name_pairs, indent=4))
        else:
            print("JSON data not found on the page.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract JSON data from a website.")
    parser.add_argument("url", type=str, help="The URL of the website")
    args = parser.parse_args()
    main(args.url)
