# restaurant-etl

yelp-date-night-etl/
├── README.md
├── .gitignore
├── .env
├── extract/
│   └── nearby_search.py
├── transform/
│   ├── normalize.py
│   └── sentiment.py   # optional
├── load/
│   └── load_to_db.py
├── recommend/
│   └── recommend.py
├── dashboard/
│   └── app.py
└── data/
    └── raw/