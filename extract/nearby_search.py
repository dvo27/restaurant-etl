import os, requests, json
from dotenv import load_dotenv, find_dotenv

# Init environment vars
load_dotenv(find_dotenv())
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Config
LOCATION = '33.64348135255402, -117.82794659989894'
RADIUS = 8000
PLACE_TYPE = 'restaurant'
OUTPUT_PATH = 'data/raw/nearby_first_page.json'

def fetch_local_restaurants():
    """
    Fetch only the first page of local restaurants in a 5mi radius from Google Places API
    """
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': LOCATION,
        'radius': RADIUS,
        'type': PLACE_TYPE,
        'key': GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Write JSON for first page of results
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data.get('results', []))} restaurants to {OUTPUT_PATH}")

if __name__ == '__main__':
    fetch_local_restaurants()
