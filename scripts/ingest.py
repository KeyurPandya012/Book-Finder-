import pandas as pd
import requests
import sqlite3
import sys
import os
import re
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import get_db_connection, init_db

CSV_PATH = "cleaned_books.csv"
OUTPUT_CSV_ENRICHED = "books_enriched.csv"
OPENLIBRARY_API_BASE = "https://openlibrary.org/api/books"

print_lock = Lock()

def safe_print(msg):
    with print_lock:
        try:
            print(msg)
        except UnicodeEncodeError:
            try:
                print(msg.encode('ascii', 'ignore').decode('ascii'))
            except:
                pass

def clean_description(desc):
    if not desc: return None
    if isinstance(desc, dict): desc = desc.get('value', '')
    if not isinstance(desc, str): return None
    # Basic cleaning
    clean = re.sub('<.*?>', '', desc)
    clean = clean.replace('&amp;', '&').replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>')
    # Remove excessive whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean if len(clean) > 20 else None

def get_with_retry(url, timeout=5, retries=2):
    """Fetch URL with basic retry logic."""
    for i in range(retries + 1):
        try:
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200:
                return resp
            if resp.status_code == 429:
                time.sleep(2 * (i + 1)) # Wait longer for rate limits
        except:
            if i < retries:
                time.sleep(1)
    return None

def fetch_details_ultimate(isbn, title, author):
    """Ultimate Fetch worker: Exhaustive search across multiple APIs and methods."""
    description = None
    cover_image = ""
    result_title = title

    # HELPER: Scan Google Books Items
    def scan_google(query, limit=3):
        nonlocal description, cover_image, result_title
        try:
            g_url = f"https://www.googleapis.com/books/v1/volumes?q={urllib.parse.quote(query)}&maxResults={limit}"
            resp = get_with_retry(g_url, timeout=4)
            if resp:
                data = resp.json()
                if 'items' in data:
                    for item in data['items']:
                        info = item['volumeInfo']
                        desc = clean_description(info.get('description'))
                        if desc:
                            description = desc
                            result_title = info.get('title', title)
                            if not cover_image and 'imageLinks' in info:
                                cover_image = info['imageLinks'].get('thumbnail', '')
                            return True
        except: pass
        return False

    # Method 1: Google Books ISBN
    if isbn and not str(isbn).startswith("N/A"):
        if scan_google(f"isbn:{isbn}"): pass

    # Method 2: OpenLibrary ISBN
    if not description and isbn and not str(isbn).startswith("N/A"):
        try:
            url = f"{OPENLIBRARY_API_BASE}?bibkeys=ISBN:{isbn}&jscmd=details&format=json"
            resp = get_with_retry(url, timeout=3)
            if resp:
                data = resp.json()
                key = f"ISBN:{isbn}"
                if key in data:
                    det = data[key].get('details', {})
                    description = clean_description(det.get('description'))
                    if 'covers' in data[key]:
                        cover_image = f"https://covers.openlibrary.org/b/id/{data[key]['covers'][0]}-M.jpg"
                    if not description and 'works' in data[key]:
                        work_key = data[key]['works'][0].get('key')
                        w_resp = get_with_retry(f"https://openlibrary.org{work_key}.json", timeout=3)
                        if w_resp:
                            description = clean_description(w_resp.json().get('description'))
        except: pass

    # Method 3: Google Books Title + Author
    if not description:
        query = f"intitle:{title}"
        if author and not pd.isna(author):
            safe_author = str(author).split(',')[0].strip()
            query += f" inauthor:{safe_author}"
        scan_google(query, limit=3)

    # Method 4: Google Books Title ONLY (Broad)
    if not description:
        scan_google(title, limit=3)

    # Method 5: OpenLibrary Title Search (Multi-doc)
    if not description:
        try:
            encoded_title = urllib.parse.quote(title)
            url = f"https://openlibrary.org/search.json?title={encoded_title}&limit=3"
            resp = get_with_retry(url, timeout=4)
            if resp:
                data = resp.json()
                if data.get('docs'):
                    for doc in data['docs']:
                        work_key = doc.get('key')
                        if work_key:
                            w_resp = get_with_retry(f"https://openlibrary.org{work_key}.json", timeout=3)
                            if w_resp:
                                desc = clean_description(w_resp.json().get('description'))
                                if desc:
                                    description = desc
                                    break
        except: pass

    return {
        'title': result_title,
        'description': description,
        'cover_image': cover_image,
        'isbn': isbn,
        'has_description': description is not None
    }

def ingest_data(limit=40000, threads=65):
    start_time = time.time()
    init_db()
    
    if not os.path.exists(CSV_PATH):
        safe_print(f"Error: {CSV_PATH} not found.")
        return

    df = pd.read_csv(CSV_PATH)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT isbn FROM books")
    existing_isbns = {str(row[0]).strip() for row in cursor.fetchall()}
    conn.close()

    rows_to_process = []
    for _, row in df.iterrows():
        isbn = str(row['ISBN']).strip()
        if isbn in existing_isbns: continue
        rows_to_process.append((isbn, str(row['Title']), row['Author/Editor'], row['Year']))
        if len(rows_to_process) >= limit: break

    total_to_process = len(rows_to_process)
    safe_print(f"🚀 ULTIMATE COVERAGE MODE: Hunting {total_to_process} missing books with {threads} threads...")

    inserted_count = 0
    processed_count = 0
    batch_data = []

    def commit_batch(data_list):
        db_conn = get_db_connection()
        db_cursor = db_conn.cursor()
        for b in data_list:
            try:
                db_cursor.execute('''
                    INSERT INTO books (isbn, title, description, author, cover_image, publish_year)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (b['isbn'], b['title'], b['description'], b['author'], b['cover_image'], b['publish_year']))
            except sqlite3.IntegrityError: pass
        db_conn.commit()
        db_conn.close()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_book = {executor.submit(fetch_details_ultimate, r[0], r[1], r[2]): r for r in rows_to_process}
        
        for future in as_completed(future_to_book):
            processed_count += 1
            orig_row = future_to_book[future]
            try:
                res = future.result()
                if res['has_description']:
                    batch_data.append({
                        'isbn': res['isbn'], 'title': res['title'], 'description': res['description'],
                        'author': orig_row[2], 'cover_image': res['cover_image'], 'publish_year': orig_row[3]
                    })
            except Exception:
                pass

            if len(batch_data) >= 3:
                commit_batch(batch_data)
                inserted_count += len(batch_data)
                elapsed = time.time() - start_time
                rate = (inserted_count / elapsed) * 60
                safe_print(f"  ✨ Added {len(batch_data)} (Total: {inserted_count}) | Checked: {processed_count}/{total_to_process} | Speed: {rate:.1f}/min")
                batch_data = []

            # Heartbeat logging
            if processed_count % 10 == 0:
                 safe_print(f"  💓 Scanning... {processed_count}/{total_to_process} checked. Found {inserted_count + len(batch_data)} in this run.")

    if batch_data:
        commit_batch(batch_data)
        inserted_count += len(batch_data)

    safe_print(f"🏁 ULTIMATE FETCH COMPLETE! Added {inserted_count} books. Total time: {time.time()-start_time:.1f}s")
    
    # Final Export
    conn = get_db_connection()
    pd.read_sql_query("SELECT * FROM books", conn).to_csv(OUTPUT_CSV_ENRICHED, index=False)
    conn.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=40000)
    parser.add_argument("--threads", type=int, default=65)
    args = parser.parse_args()
    ingest_data(limit=args.limit, threads=args.threads)
