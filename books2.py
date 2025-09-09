from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=100)
    author: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=5, max_length=500)
    rating: int = Field(gt=0, lt=6)


BOOKS = [
    Book(id=1, title="Title 1", author="Author 1",
         description="Description 1", rating=5),
    Book(id=2, title="Title 2", author="Author 2",
         description="Description 2", rating=4),
    Book(id=3, title="Title 3", author="Author 3",
         description="Description 3", rating=3),
]


@app.get("/books")
def read_books():
    return BOOKS


@app.post("/create_book")
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
