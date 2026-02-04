import sqlite3
import requests
import re
import time
import urllib.parse
import sys
import os

# Ensure import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import get_db_connection

OPENLIBRARY_API_BASE = "https://openlibrary.org/api/books"

def clean_description(desc):
    if not desc:
        return None
    if isinstance(desc, dict):
        desc = desc.get('value', '')
    if not isinstance(desc, str):
        return None
    clean = re.sub('<.*?>', '', desc)
    clean = clean.replace('&amp;', '&').replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>')
    return clean.strip()

def fetch_work_details(work_key):
    if not work_key: return None
    url = f"https://openlibrary.org{work_key}.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def fetch_details(isbn, title):
    # 1. Try ISBN
    if isbn and not isbn.startswith("N/A"):
        url = f"{OPENLIBRARY_API_BASE}?bibkeys=ISBN:{isbn}&jscmd=details&format=json"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                key = f"ISBN:{isbn}"
                if key in data:
                    details = data[key]
                    # recursive work check
                    if 'description' not in details and 'works' in details:
                        work_key = details['works'][0]['key']
                        w_details = fetch_work_details(work_key)
                        if w_details:
                           if 'description' in w_details: details['description'] = w_details['description']
                           if 'title' not in details and 'title' in w_details: details['title'] = w_details['title']
                    return details
        except Exception as e:
            print(f"Error ISBN {isbn}: {e}")

    # 2. Try Title search fallback
    try:
        encoded_title = urllib.parse.quote(title)
        url = f"https://openlibrary.org/search.json?title={encoded_title}&limit=1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('docs'):
                return fetch_work_details(olid)
    except Exception as e:
        print(f"Error Title {title}: {e}")

    # 3. Google Books Fallback (The "Power" Move)
    if isbn and not isbn.startswith("N/A"):
        try:
             # Try Google Books
             g_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
             g_resp = requests.get(g_url, timeout=5)
             if g_resp.status_code == 200:
                 g_data = g_resp.json()
                 if 'items' in g_data:
                     info = g_data['items'][0]['volumeInfo']
                     description = info.get('description')
                     if description:
                         return {'description': description, 'title': info.get('title'), 'covers': []}
        except Exception as e:
            print(f"Error GoogleBooks {isbn}: {e}")
            
    return None

def enrich_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Select books with placeholder descriptions
    # We also re-try "No description found" (Description unavailable.) because we have a new source now
    cursor.execute("SELECT id, isbn, title FROM books WHERE description LIKE 'Description%'")
    books_to_update = cursor.fetchall()
    
    print(f"Found {len(books_to_update)} books needing descriptions.")
    
    updated_count = 0
    
    for row in books_to_update:
        book_id = row['id']
        isbn = row['isbn']
        title = row['title']
        
        print(f"Enriching ({updated_count+1}/{len(books_to_update)}): {title[:40]}...")
        
        details = fetch_details(isbn, title)
        
        new_desc = "Description unavailable."
        new_cover = None
        
        if details:
            clean = clean_description(details.get('description'))
            if clean:
                new_desc = clean
            
            if 'covers' in details and details['covers']:
                 new_cover = f"https://covers.openlibrary.org/b/id/{details['covers'][0]}-M.jpg"
            elif 'cover' in details:
                 new_cover = details['cover'].get('medium', '')
        
        # Update DB
        try:
            if new_cover:
                cursor.execute("UPDATE books SET description = ?, cover_image = ? WHERE id = ?", (new_desc, new_cover, book_id))
            else:
                 cursor.execute("UPDATE books SET description = ? WHERE id = ?", (new_desc, book_id))
            conn.commit()
            if new_desc != "Description unavailable.":
                print(f"  -> SUCCESS! Added description.")
            else:
                print(f"  -> No description found.")
        except Exception as e:
            print(f"  -> DB Error: {e}")

        updated_count += 1
        time.sleep(1.0) # Be nice to API
        
    conn.close()
    print("Enrichment complete.")

if __name__ == "__main__":
    enrich_books()
