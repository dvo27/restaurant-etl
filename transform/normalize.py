import os, json, csv
from pathlib import Path

RAW_PATH = Path('data/raw/nearby_first_page.json')
OUT_DIR = Path('data/normalized')
OUT_PATH = OUT_DIR / 'places.csv'

def normalize_places():
    # Load raw JSON
    with RAW_PATH.open() as f:
        payload = json.load(f)
    results = payload.get('results', [])
    
    # Make sure output directory exists
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Define CSV headers
    headers = [
        'place_id',
        'name',
        'rating',
        'user_ratings_total',
        'latitude',
        'longitude',
        'price_level',
        'types'
    ]
    
    # Write CSV
    with OUT_PATH.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        
        # Write rows per restaurant filling out the categories
        for place in results:
            geom = place.get('geometry', {}).get("location", {})
            writer.writerow({
                'place_id': place.get('place_id', ""),
                'name': place.get('name', '').replace(',', ''),
                'rating': place.get('rating', ''),
                'user_ratings_total': place.get('user_ratings_total', 0),
                'latitude': geom.get('lat', ''),
                'longitude': geom.get('lng', ''),
                'types': '|'.join(place.get('types', [])),
                'price_level': place.get('price_level', '')
                
            })
    
    print(f"Wrote {len(results)} rows to {OUT_PATH}")
    
if __name__ == "__main__":
    normalize_places()