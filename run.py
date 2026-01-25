import uvicorn
import os
import sys

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    print("Starting BookFinder API...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
