import requests

API_KEY = "YzxsLGsXCuZRka6j6fS8kxt2SPnwbsZtsvfnw2Kr"
url = "https://api.nasa.gov/neo/rest/v1/feed"

params = {
    "start_date": "2026-09-12",
    "end_date": "2026-09-19",
    "api_key": API_KEY
}

response = requests.get(url, params=params)
print(response.status_code)
data = response.json()


# near_earth_objects is a dict keyed by date, each value is a LIST of asteroids
for date, asteroids in data["near_earth_objects"].items():
    print(f"\n📅 {date}")
    for a in asteroids:
        name = a["name"]
        diameter_m = a["estimated_diameter"]["meters"]["estimated_diameter_max"]
        hazardous = a["is_potentially_hazardous_asteroid"]
        approach = a["close_approach_data"][0]  # list with one entry per date here
        miss_km = float(approach["miss_distance"]["kilometers"])
        speed_kph = float(approach["relative_velocity"]["kilometers_per_hour"])

        print(f"  {name}")
        print(f"    max diameter: {diameter_m:.1f} m")
        print(f"    hazardous?: {hazardous}")
        print(f"    miss distance: {miss_km:,.0f} km")
        print(f"    speed: {speed_kph:,.0f} km/h")


#git status (check what changed)
#git add . (modify change)
#git commit -m" "
#git push