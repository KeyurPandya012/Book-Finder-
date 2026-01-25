import sqlite3

try:
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM books")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("""
            INSERT INTO books (isbn, title, description, author, publish_year) 
            VALUES ('1234567890', 'Test Book', 'This is a manually inserted test book to verify the API.', 'Test Author', 2025)
        """)
        conn.commit()
        print("Inserted test book.")
    else:
        print(f"Database already has {count} books.")
    conn.close()
except Exception as e:
    print(e)
