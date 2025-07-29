# restaurant‑etl

An end‑to‑end ETL pipeline and interactive dashboard that pulls restaurant data from the Google Places API, normalizes and loads it into a local SQLite database, and surfaces personalized “date‑night” picks via Streamlit. Filter by rating, review count, cuisine, and “underrated” status in a lightweight, Python‑only app.

---

## 🚀 Features

- **Extract**: fetch the first page of nearby restaurants for any latitude/longitude & radius  
- **Transform**: normalize raw JSON into a flat CSV with core attributes (ID, name, rating, location, types)  
- **Load**: ingest CSV into a local SQLite database (`restaurant-etl.db`) with idempotent upserts  
- **Recommend**: simple ranking by rating & review volume, with an “underrated” option  
- **Dashboard**: Streamlit interface to filter and display top picks, with dynamic review‑count bounds  

---

## 🛠️ Prerequisites

- Python 3.8+  
- A Google Cloud API key with **Places API** enabled and a billing account attached (free \$200/month credit)  
- (Optional) [Streamlit](https://streamlit.io/) for dashboard  

---

## ⚙️ Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/<your‑username>/restaurant‑etl.git
   cd restaurant‑etl
2. **Create & activate a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate    # macOS/Linux
    .venv\Scripts\activate       # Windows
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
4. **Configure Your API Key**
    Copy .env.example → .env
    Open .env and set your key:
    GOOGLE_API_KEY=your_real_key_here

##  🔄 Directory Structure
restaurant-etl/
├── README.md
├── .env.example
├── requirements.txt
├── extract/
│   └── nearby_search.py
├── transform/
│   └── normalize.py
├── load/
│   └── load_to_db.py
├── recommend/
│   └── recommend.py
├── dashboard/
│   └── app.py
├── data/
│   └── raw/             # raw JSON from extractor
│   └── normalized/      # flattened CSVs
└── restaurant-etl.db    # SQLite DB (created by loader)

## 🏁 Usage
TODO...
   

