from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="Library API",
    description="یک سیستم کتابداری ساده با FastAPI (داده‌ها در حافظه نگه‌داری می‌شوند)",
    version="1.0.0",
)

# -------------------- Models --------------------

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, examples=["شاهنامه"])
    author: str = Field(..., min_length=1, max_length=100, examples=["فردوسی"])
    year: Optional[int] = Field(None, ge=0, le=2100, examples=[1010])
    isbn: Optional[str] = Field(None, max_length=20, examples=["978-964-00-0000-0"])


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=0, le=2100)
    isbn: Optional[str] = Field(None, max_length=20)


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    created_at: datetime


# -------------------- In-memory storage --------------------

books: List[Book] = []
next_id: int = 1


def get_book_or_404(book_id: int) -> Book:
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"کتاب با شناسه {book_id} پیدا نشد",
    )


# -------------------- Endpoints --------------------

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "به API کتابخانه خوش آمدید",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/books", response_model=List[Book], tags=["Books"])
def get_books():
    """دریافت لیست تمام کتاب‌ها"""
    return books


@app.post(
    "/books",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
)
def create_book(book_data: BookCreate):
    """اضافه کردن کتاب جدید"""
    global next_id
    new_book = Book(
        id=next_id,
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        isbn=book_data.isbn,
        created_at=datetime.utcnow(),
    )
    books.append(new_book)
    next_id += 1
    return new_book


@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
def get_book(book_id: int):
    """گرفتن اطلاعات یک کتاب خاص"""
    return get_book_or_404(book_id)


@app.patch("/books/{book_id}", response_model=Book, tags=["Books"])
def update_book(book_id: int, book_data: BookUpdate):
    """تغییر اطلاعات یک کتاب خاص (فقط فیلدهای ارسال‌شده به‌روز می‌شوند)"""
    book = get_book_or_404(book_id)
    update_data = book_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    return book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
)
def delete_book(book_id: int):
    """حذف یک کتاب خاص"""
    book = get_book_or_404(book_id)
    books.remove(book)
    return None
