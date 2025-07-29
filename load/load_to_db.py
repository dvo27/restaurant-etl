import os
import sqlite3
import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / 'data' / 'normalized' / 'places.csv'
DB_PATH = BASE_DIR / 'restaurant-etl.db'


def load_places_to_sqlite():
    # Connect/create SQLite Database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS places (
    place_id TEXT PRIMARY KEY,
    name TEXT,
    rating REAL,
    user_ratings_total INTEGER,
    latitude REAL,
    longitude REAL,
    price_level INTEGER,
    types TEXT
    )
    """)

    # Read CSV and load rows
    with open(CSV_PATH, newline="", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            rows.append((
                row['place_id'],
                row['name'],
                float(row['rating']) if row['rating'] else None,
                int(row['user_ratings_total']),
                float(row['latitude']),
                float(row['longitude']),
                int(row['price_level']) if row['price_level'] else None,
                row['types']
            ))

    cursor.executemany("""
    INSERT OR REPLACE INTO places
    (place_id, name, rating, user_ratings_total, latitude, longitude, price_level, types)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
    
    conn.commit()
    print(f"Loaded {len(rows)} places into {DB_PATH}")

    # Optionally, print a couple of samples
    cursor.execute("SELECT name, rating, types FROM places LIMIT 5")
    for name, rating, types in cursor.fetchall():
        print(f"- {name} ({rating}★) [{types}]")

    conn.close()


if __name__ == "__main__":
    load_places_to_sqlite()
