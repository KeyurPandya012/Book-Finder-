from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    isbn: str
    title: str
    description: Optional[str] = None
    author: Optional[str] = None
    cover_image: Optional[str] = None
    publish_year: Optional[int] = None

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class RecommendationRequest(BaseModel):
    mood: str
