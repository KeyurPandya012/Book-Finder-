import sqlite3
from typing import List, Optional

DB_NAME = "books.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10) 
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL") 
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT UNIQUE,
            title TEXT,
            description TEXT,
            author TEXT,
            cover_image TEXT,
            publish_year INTEGER
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
