import requests

API_KEY = "YOUR_KEY_HERE"
url = "https://api.nasa.gov/neo/rest/v1/feed"

params = {
    "start_date": "2026-09-18",
    "end_date": "2026-09-19",
    "api_key": API_KEY
}

response = requests.get(url, params=params)
print(response.status_code)
print(response.json())