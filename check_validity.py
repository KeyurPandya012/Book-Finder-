import sqlite3

def check_counts():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT count(*) FROM books WHERE description NOT LIKE 'Description%' AND description != '' AND description IS NOT NULL")
    valid = cursor.fetchone()[0]
    
    cursor.execute("SELECT count(*) FROM books")
    total = cursor.fetchone()[0]
    
    print(f"Valid Descriptions: {valid}")
    print(f"Total Books: {total}")
    conn.close()

if __name__ == "__main__":
    check_counts()
