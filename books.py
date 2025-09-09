from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "Fiction"},
    {"title": "Title Three", "author": "Author Three", "category": "Science"},
    {"title": "Title Four", "author": "Author Four", "category": "History"},
    {"title": "Title Five", "author": "Author Five", "category": "Science"},
    {"title": "Title Six", "author": "Author Two", "category": "Science"},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book["title"].lower() == book_title.lower():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    books_in_category = [
        book for book in BOOKS if book["category"].lower() == category.lower()]
    return books_in_category


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_by_author_in_category = [
        book for book in BOOKS
        if book["author"].lower() == book_author.lower()
        and book["category"].lower() == category.lower()
    ]
    return books_by_author_in_category


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for index, book in enumerate(BOOKS):
        if book["title"].lower() == updated_book["title"].lower():
            BOOKS[index] = updated_book
            return updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for index, book in enumerate(BOOKS):
        if book["title"].lower() == book_title.lower():
            deleted_book = BOOKS.pop(index)
            return deleted_book


@app.get("/books/byauthor/{author_name}")
async def read_books_by_author(author_name: str):
    books_by_author = [
        book for book in BOOKS if book["author"].lower() == author_name.lower()]
    return books_by_author
