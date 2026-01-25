import pandas as pd
import re
import os

INPUT_CSV = "RC_BOOK_ISBN.csv"
OUTPUT_CSV = "cleaned_books.csv"

def clean_isbn(isbn):
    if pd.isna(isbn):
        return None
    # Remove non-alphanumeric characters except X
    cleaned = re.sub(r'[^0-9X]', '', str(isbn).upper())
    # Basic length check
    if len(cleaned) in [10, 13]:
        return cleaned
    return None

def process_csv():
    if not os.path.exists(INPUT_CSV):
        print(f"Error: {INPUT_CSV} not found.")
        return

    print(f"Reading {INPUT_CSV}...")
    try:
        df = pd.read_csv(INPUT_CSV, encoding='latin1', on_bad_lines='skip')
    except Exception as e:
        print(f"Latin1 failed: {e}, trying cp1252")
        df = pd.read_csv(INPUT_CSV, encoding='cp1252', on_bad_lines='skip')

    print(f"Original Row Count: {len(df)}")

    # Create a cleaner ISBN column for deduplication check
    df['Cleaned_ISBN'] = df['ISBN'].apply(clean_isbn)

    # Valid ISBNs only
    df_valid = df.dropna(subset=['Cleaned_ISBN'])
    print(f"Rows with valid ISBN format: {len(df_valid)}")

    # Deduplicate
    df_dedup = df_valid.drop_duplicates(subset=['Cleaned_ISBN'], keep='first')
    
    print(f"Rows after removing duplicates: {len(df_dedup)}")

    df_dedup['ISBN'] = df_dedup['Cleaned_ISBN']
    df_dedup = df_dedup.drop(columns=['Cleaned_ISBN'])

    print(f"Saving to {OUTPUT_CSV}...")
    df_dedup.to_csv(OUTPUT_CSV, index=False)
    print("Done.")

if __name__ == "__main__":
    process_csv()
