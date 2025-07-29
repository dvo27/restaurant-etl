# dashboard/app.py

import streamlit as st
import sqlite3
import pandas as pd

# --- UI Setup ---
st.set_page_config(page_title="🍽️ Date-Night Picks", layout="wide")
st.title("🍽️ Restaurant ETL – Date Night Picks")

st.sidebar.header("🔍 Filter Options")
# (Location input for future dynamic extract)
location_input = st.sidebar.text_input("Location (lat,lng)", "37.7749,-122.4194")
cuisine_options = st.sidebar.multiselect(
    "Select Cuisines",
    options=["restaurant", "bar", "cafe", "food", "bakery"],  # you can populate this dynamically
    default=[]
)
rating_threshold = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 4.0, 0.1)
reviews_range = st.sidebar.slider("Review Count Range", 0, 500, (50, 200), 10)
underrated_only = st.sidebar.checkbox("Show Underrated Only", value=False)

# --- Data Fetching ---
conn = sqlite3.connect("restaurant_etl.db")
query = """
SELECT place_id, name, rating, user_ratings_total, types
FROM places
WHERE rating >= ?
  AND user_ratings_total BETWEEN ? AND ?
"""
params = [rating_threshold, reviews_range[0], reviews_range[1]]

# Apply cuisine filter if selected
if cuisine_options:
    placeholders = " OR ".join(["types LIKE ?"] * len(cuisine_options))
    query += f" AND ({placeholders})"
    params.extend([f"%{c}%" for c in cuisine_options])

df = pd.read_sql_query(query, conn, params=params)
conn.close()

# --- Underrated Filter & Sorting ---
if underrated_only:
    # Sort by high rating, then low review count
    df = df.sort_values(by=["rating", "user_ratings_total"], ascending=[False, True])
else:
    # Default: sort by rating desc, then review count desc
    df = df.sort_values(by=["rating", "user_ratings_total"], ascending=[False, False])

# Limit to top 10
df = df.head(10)

# --- Display ---
st.subheader("Filtered Restaurant Picks")
st.dataframe(df, use_container_width=True)
