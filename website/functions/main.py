import functions_framework
import requests
from urllib.parse import quote
import os
import logging

API_KEY = os.environ.get("RIOT_API_KEY")

@functions_framework.http
def get_puuid(request):
    # Handle CORS preflight request
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        }
        return ('', 204, headers)

    # Set CORS headers for actual request
    cors_headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json(silent=True)
    if not request_json or "game_name" not in request_json or "tag_line" not in request_json:
        return ({"error": "Missing game_name or tag_line"}, 400, cors_headers)

    game_name = request_json["game_name"]
    tag_line = request_json["tag_line"]
    region = request_json["region"]

    # URL encode parameters
    game_name_encoded = quote(game_name)
    tag_line_encoded = quote(tag_line)
    region_encoded = quote(region)

    
    url = f"https://{region_encoded}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name_encoded}/{tag_line_encoded}"
    headers = {"X-Riot-Token": API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return ({"puuid": data["puuid"]}, 200, cors_headers)
    else:
        return ({"error": f"Riot API error {response.status_code}: {response.text}"}, response.status_code, cors_headers)
