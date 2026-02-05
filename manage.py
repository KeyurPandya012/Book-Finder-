import sys
import os

def show_help():
    help_text = """
====================================================
      BookFinder: Team_VK Project CLI
====================================================
Usage: python manage.py [command]

Available Commands:
  //help          - Show this help menu
  run            - Start the FastAPI server (same as run.bat)
  clean          - Run the data cleaning script (clean_csv.py)
  ingest         - Run the data ingestion script (ingest.py)
  stats          - Show database and data statistics
  sync           - Trigger a background data sync via API
  docker         - Show Docker status and commands

Example: python manage.py //help
====================================================
    """
    print(help_text)

def start_server():
    print("Launching BookFinder API...")
    os.system("python run.py")

def clean_data():
    print("Cleaning CSV data...")
    os.system("python scripts/clean_csv.py")

def ingest_data():
    print("Ingesting book data (Deep Fetch)...")
    os.system("python scripts/ingest.py --threads 60")

def show_stats():
    print("\n--- Project Statistics ---")
    os.system("powershell -Command \"Write-Host 'Raw Records:'; (Get-Content RC_BOOK_ISBN.csv | Measure-Object -Line).Lines\"")
    os.system("powershell -Command \"Write-Host 'Cleaned Records:'; (Get-Content cleaned_books.csv | Measure-Object -Line).Lines\"")
    # Call a snippet for DB stats
    os.system("python -c \"import sqlite3; conn = sqlite3.connect('books.db'); cursor = conn.cursor(); print(f'Database Total: {cursor.execute(\\\"SELECT COUNT(*) FROM books\\\").fetchone()[0]} enriched books'); conn.close()\"")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "//help":
        show_help()
    elif cmd == "run":
        start_server()
    elif cmd == "clean":
        clean_data()
    elif cmd == "ingest":
        ingest_data()
    elif cmd == "stats":
        show_stats()
    elif cmd == "sync":
        print("Triggering sync...")
        os.system("curl -X POST http://127.0.0.1:8000/sync")
    elif cmd == "docker":
        os.system("docker ps")
    else:
        print(f"Unknown command: {cmd}")
        show_help()

if __name__ == "__main__":
    main()
