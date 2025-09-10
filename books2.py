from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="ID is not needed on create", default=None)
    title: str = Field(min_length=5, max_length=100)
    author: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=5, max_length=500)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book Title",
                "author": "Book Author",
                "description": "Book Description",
                "rating": 5,
                "published_date": 2023
            }
        }
    }


BOOKS = [
    Book(id=1, title="Title 1", author="Author 1",
         description="Description 1", rating=5, published_date=2020),
    Book(id=2, title="Title 2", author="Author 2",
         description="Description 2", rating=4, published_date=2021),
    Book(id=3, title="Title 3", author="Author 3",
         description="Description 3", rating=3, published_date=2022),
]


@app.get("/books")
def read_books():
    return BOOKS


@app.get("/books/{book_id}")
def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/")
def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    books_with_rating = [book for book in BOOKS if book.rating == rating]
    return books_with_rating


@app.get("/books/publish/")
def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    books_with_published_date = [
        book for book in BOOKS if book.published_date == published_date]
    return books_with_published_date


@app.post("/create_book")
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book/{book_id}")
def update_book(book_id: int, book_request: BookRequest):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS[index] = Book(id=book_id, author=book_request.author,
                                title=book_request.title, description=book_request.description, rating=book_request.rating)
            return BOOKS[index]
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/delete_book/{book_id}")
def delete_book(book_id: int = Path(gt=0)):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
