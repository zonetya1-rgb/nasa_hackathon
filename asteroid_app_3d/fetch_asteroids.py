"""
fetch_asteroids.py
-------------------
Pulls near-Earth asteroid data from NASA's API and writes it to a plain CSV
file (data/asteroids.csv) so the C program can read it without needing a
JSON library.
"""

import requests
import csv
import os

API_KEY = "DEMO_KEY"  # <-- replace with your real NASA API key
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "asteroids.csv")


def fetch(start_date, end_date):
    response = requests.get(
        "https://api.nasa.gov/neo/rest/v1/feed",
        params={"start_date": start_date, "end_date": end_date, "api_key": API_KEY},
    )
    response.raise_for_status()
    return response.json()


def flatten(raw_json):
    """Turn NASA's nested date->list structure into one flat list of dicts."""
    rows = []
    for date, asteroids in raw_json["near_earth_objects"].items():
        for a in asteroids:
            approach = a["close_approach_data"][0]
            rows.append({
                "id": a["id"],
                "name": a["name"].replace(",", ";"),  # protect the CSV format
                "date": date,
                "diameter_m": a["estimated_diameter"]["meters"]["estimated_diameter_max"],
                "speed_kph": float(approach["relative_velocity"]["kilometers_per_hour"]),
                "miss_distance_km": float(approach["miss_distance"]["kilometers"]),
                "hazardous": int(a["is_potentially_hazardous_asteroid"]),
            })
    return rows


def save_csv(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "name", "date", "diameter_m", "speed_kph",
            "miss_distance_km", "hazardous"
        ])
        writer.writeheader()
        writer.writerows(rows)


def fetch_and_save(start_date, end_date):
    raw = fetch(start_date, end_date)
    rows = flatten(raw)
    save_csv(rows, OUTPUT_PATH)
    return rows


if __name__ == "__main__":
    # quick manual test
    data = fetch_and_save("2026-09-18", "2026-09-20")
    print(f"Saved {len(data)} asteroids to {OUTPUT_PATH}")