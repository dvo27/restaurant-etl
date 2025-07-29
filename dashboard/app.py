```python
# dashboard/app.py

import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# --- UI Setup ---
st.set_page_config(page_title="🍽️ Date-Night Picks", layout="wide")
st.title("🍽️ Restaurant ETL – Date Night Picks")

# Resolve DB path relative to project root
def get_db_connection():
    base_dir = Path(__file__).parent.parent  # two levels up: restaurant-etl/
    db_path = base_dir / "restaurant_etl.db"
    return sqlite3.connect(db_path)

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")
location_input = st.sidebar.text_input("Location (lat,lng)", "37.7749,-122.4194")
cuisine_options = st.sidebar.multiselect(
    "Select Cuisines",
    options=["restaurant", "bar", "cafe", "food", "bakery"],
    default=[]
)
rating_threshold = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 4.0, 0.1)
reviews_range = st.sidebar.slider("Review Count Range", 0, 500, (50, 200), 10)
underrated_only = st.sidebar.checkbox("Show Underrated Only", value=False)

# --- Build Query ---
base_query = (
    "SELECT place_id, name, rating, user_ratings_total, types"
    " FROM places"
    " WHERE rating >= ?"
    " AND user_ratings_total BETWEEN ? AND ?"
)
params = [rating_threshold, reviews_range[0], reviews_range[1]]

if cuisine_options:
    placeholders = " OR ".join(["types LIKE ?" for _ in cuisine_options])
    base_query += f" AND ({placeholders})"
    params.extend([f"%{c}%" for c in cuisine_options])

# --- Fetch Data ---
conn = get_db_connection()
df = pd.read_sql_query(base_query, conn, params=params)
conn.close()

# --- Apply Underrated Filter & Sorting ---
if underrated_only:
    df = df.sort_values(
        by=["rating", "user_ratings_total"],
        ascending=[False, True]
    )
else:
    df = df.sort_values(
        by=["rating", "user_ratings_total"],
        ascending=[False, False]
    )

# Limit to top 10
if not df.empty:
    df = df.head(10)

# --- Display ---
st.subheader("Filtered Restaurant Picks")
st.dataframe(df, use_container_width=True)
```
