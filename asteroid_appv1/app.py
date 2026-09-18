from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = ""  # <-- replace with your real NASA API key

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_asteroids", methods=["POST"])
def get_asteroids():
    data = request.json
    start_date = data["start_date"]
    end_date = data["end_date"]

    response = requests.get(
        "https://api.nasa.gov/neo/rest/v1/feed",
        params={
            "start_date": start_date,
            "end_date": end_date,
            "api_key": API_KEY,
        },
    )

    if response.status_code != 200:
        return jsonify({"error": f"NASA API returned status {response.status_code}"}), 500

    raw = response.json()
    results = []

    for date, asteroids in raw["near_earth_objects"].items():
        for a in asteroids:
            approach = a["close_approach_data"][0]
            results.append({
                "date": date,
                "name": a["name"],
                "diameter_m": round(a["estimated_diameter"]["meters"]["estimated_diameter_max"], 1),
                "hazardous": a["is_potentially_hazardous_asteroid"],
                "miss_distance_km": round(float(approach["miss_distance"]["kilometers"])),
                "miss_distance_lunar": round(float(approach["miss_distance"]["lunar"]), 2),
                "speed_kph": round(float(approach["relative_velocity"]["kilometers_per_hour"])),
                "jpl_url": a["nasa_jpl_url"],
            })

    results.sort(key=lambda x: x["miss_distance_km"])
    return jsonify({"asteroids": results})

if __name__ == "__main__":
    app.run(debug=True, port=5050)