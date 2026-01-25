from .database import get_db_connection
from .schemas import Book

def get_books(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE description IS NOT NULL AND description != 'Description not available.' LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_book_by_isbn(isbn: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_recent_books(limit: int = 1000):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
