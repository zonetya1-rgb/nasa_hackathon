"""
app.py
-------
Orchestrates the pipeline:
  1. fetch_asteroids.py pulls data from NASA and saves data/asteroids.csv
  2. the compiled C program (./calculations) reads that CSV and writes
     data/results.json with physics estimates added
  3. this Flask app reads results.json and serves it to the Three.js
     frontend in templates/index.html
"""

import subprocess
import json
import os
from flask import Flask, render_template, request, jsonify

from fetch_asteroids import fetch_and_save

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)
RESULTS_PATH = os.path.join(BASE_DIR, "data", "results.json")
C_BINARY = os.path.join(BASE_DIR, "calculations")  # compiled C program


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_asteroids", methods=["POST"])
def get_asteroids():
    data = request.json
    start_date = data["start_date"]
    end_date = data["end_date"]

    # Step 1: fetch fresh data from NASA and write data/asteroids.csv
    try:
        fetch_and_save(start_date, end_date)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch NASA data: {e}"}), 500

    # Step 2: run the compiled C program to compute physics estimates
    if not os.path.exists(C_BINARY):
        return jsonify({
            "error": "C program not compiled yet. Run: gcc calculations.c -o calculations -lm"
        }), 500

    result = subprocess.run([C_BINARY], cwd=BASE_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        return jsonify({"error": f"C program failed: {result.stderr}"}), 500

    # Step 3: read what the C program wrote and send it to the browser
    with open(RESULTS_PATH) as f:
        asteroids = json.load(f)

    return jsonify({"asteroids": asteroids})


if __name__ == "__main__":
    app.run(debug=True, port=5050)