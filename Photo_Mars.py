import requests
import os

API_KEY = ""
rover = "curiosity"
save_folder = "mars_photos"

os.makedirs(save_folder, exist_ok=True)  # creates the folder if it doesn't exist

response = requests.get(
    f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos",
    params={"earth_date": "2026-09-01", "api_key": API_KEY}
)
data = response.json()
photos = data["photos"]

for i, p in enumerate(photos[:5]):
    img_url = p["img_src"]
    img_data = requests.get(img_url).content
    filename = os.path.join(save_folder, f"mars_{i}.jpg")
    with open(filename, "wb") as f:
        f.write(img_data)
    print(f"Saved {filename}")