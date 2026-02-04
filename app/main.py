from fastapi import FastAPI, HTTPException, BackgroundTasks, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
import sys
import os

# Ensure we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import crud, schemas, database, recommender
from scripts.ingest import ingest_data

app = FastAPI(title="BookFinder API", description="API for searching and retrieving book data.")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
def startup_event():
    database.init_db()
    # Pre-load recommender
    recommender.recommender.load_data()

@app.get("/", tags=["Root"])
def read_root():
    return FileResponse('app/static/index.html')

@app.get("/books", response_model=List[schemas.Book], tags=["Books"])
def read_books(skip: int = 0, limit: int = 100):
    """
    Get a list of books with pagination.
    """
    books = crud.get_books(skip=skip, limit=limit)
    return books

@app.get("/books/{isbn}", response_model=schemas.Book, tags=["Books"])
def read_book(isbn: str):
    """
    Get a specific book by ISBN.
    """
    book = crud.get_book_by_isbn(isbn)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/recommend", tags=["Recommendations"])
def recommend_books(request: schemas.RecommendationRequest):
    """
    Recommend books based on a mood or problem description.
    """
    mood = request.mood
    if not mood:
         raise HTTPException(status_code=400, detail="Mood cannot be empty")
         
    recommended = recommender.recommender.recommend(mood)
    return recommended

@app.get("/books/{isbn}/similar", response_model=List[schemas.Book], tags=["Recommendations"])
def get_similar_books(isbn: str, limit: int = 5):
    """
    Get books similar to a specific book.
    """
    similar = recommender.recommender.get_similar_books(isbn, top_n=limit)
    if not similar:
        # If no similarity found, maybe it's not in our matrix yet
        return []
    return similar

@app.get("/books/author/{name}", response_model=List[schemas.Book], tags=["Recommendations"])
def get_books_by_author(name: str, skip_isbn: Optional[str] = None, limit: int = 5):
    """
    Get books by a specific author.
    """
    books = recommender.recommender.get_books_by_author(name, skip_isbn=skip_isbn, top_n=limit)
    return books

@app.post("/reload", tags=["Admin"])
def reload_model():
    """
    Reloads the recommendation model (useful after data ingestion).
    """
    recommender.recommender.load_data()
    return {"message": "Model reloaded"}

@app.post("/sync", tags=["Admin"])
def sync_data(background_tasks: BackgroundTasks, limit: int = 100):
    """
    Trigger data ingestion in the background.
    """
    background_tasks.add_task(ingest_data, limit=limit)
    return {"message": f"Data ingestion started in background (Limit: {limit})"}
