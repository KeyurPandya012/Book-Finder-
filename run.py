import uvicorn
import os
import sys

if __name__ == "__main__":
    # Ensure the current directory is in sys.path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    print("Starting BookFinder API...")
    # Run the uvicorn server programmatically
    # equivalent to: uvicorn app.main:app --reload
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
