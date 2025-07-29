import sqlite3

DB_PATH = 'restaurant-etl.db'
TOP_N = 5

def get_top_n_restaurants(n=TOP_N):
    """Gets the top n restaurants from the database, ranked by 
    restauarant rating and then total number of user ratings

    Args:
        n (int, optional): number of restaurants. Defaults to TOP_N.
    """ 
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT name, rating, user_ratings_total
    FROM places
    WHERE rating IS NOT NULL
    ORDER BY rating DESC, user_ratings_total DESC
    LIMIT ?
    """, (n,))
    
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    picks = get_top_n_restaurants()
    print("🍽️ Your Top Picks:")
    for rank, (name, rating, count) in enumerate(picks, start=1):
        print(f"{rank}. {name} — {rating}★ ({count} reviews)")
