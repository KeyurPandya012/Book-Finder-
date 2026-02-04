import sqlite3
import pandas as pd
import os
import sys

# Ensure we can find the DB
DB_PATH = "books.db"

def show_all_data():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        # Read into pandas dataframe for nice printing
        df = pd.read_sql_query("SELECT id, isbn, title, substr(description, 1, 50) as desc_preview, publish_year FROM books", conn)
        
        if df.empty:
            print("Database is empty.")
        else:
            print(f"Total Books: {len(df)}")
            print("-" * 80)
            print(df.to_string(index=False))
            print("-" * 80)
    except Exception as e:
        print(f"Error reading database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    show_all_data()
