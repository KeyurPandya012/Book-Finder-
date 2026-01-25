from fastapi import FastAPI, HTTPException, BackgroundTasks, Body
from typing import List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import crud, schemas, database
from scripts.ingest import ingest_data

app = FastAPI(title="BookFinder API", description="API for searching and retrieving book data.")


@app.on_event("startup")
def startup_event():
    database.init_db()

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to BookFinder API. Visit /docs for the interactive documentation."}



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



@app.post("/sync", tags=["Admin"])
def sync_data(background_tasks: BackgroundTasks, limit: int = 100):
    """
    Trigger data ingestion in the background.
    """
    background_tasks.add_task(ingest_data, limit=limit)
    return {"message": f"Data ingestion started in background (Limit: {limit})"}
