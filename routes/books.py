from fastapi import Depends, HTTPException, APIRouter, Query
from auth import verify_api_key
from sqlmodel import Session, select
from typing import Optional
from models.book import Book, BookRead, BookCreate, BookUpdate
from models.user import User
from database import get_session

router = APIRouter(
    prefix="/books",
    tags=["books"],
)   

@router.get("/", response_model=list[BookRead])
def get_books(
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
    title: Optional[str] | None = Query(default=None, description="Filter books by title"),
    author: Optional[str] | None = Query(default=None, description="Filter books by author"),
):
    query = select(Book).where(
        Book.is_sold == False  # Only fetch books that are not sold
    )

    if title:
        query = query.where(Book.title.contains(title))

    if author:
        query = query.where(Book.author.contains(author))

    books = session.exec(query).all()
    return books

@router.post("/", response_model=BookRead)
def create_book(
    book_data: BookCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    """
    Create a new book entry in the system.
    """
    # Match the API Key with the one in the .env file
    if(api_key != "my_secret_api_key"):  # I know this should be in the .env file but for the sake of this example, I am hardcoding it here
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Check if the user exists
    user = session.get(User, book_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create a new book instance
    book = Book.model_validate(book_data)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book

@router.patch("/{book_id}/sell", response_model=BookRead)
def mark_book_as_sold(
    book_id: int,
    book_data: BookUpdate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    """
    Mark a book as sold.
    """
    # Match the API Key with the one in the .env file
    if(api_key != "my_secret_api_key"):  # I know this should be in the .env file but for the sake of this example, I am hardcoding it here
        raise HTTPException(status_code=401, detail="Invalid API Key")

    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")   

    book_data = book_data.model_dump(exclude_unset=True)  # Exclude unset fields to avoid overwriting existing values

    for key, value in book_data.items():
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book

# Mark the book as sold
@router.patch("/{book_id}/sold", response_model=BookRead)
def mark_book_as_sold(
    book_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    """
    Mark a book as sold.
    """
    # Match the API Key with the one in the .env file
    if(api_key != "my_secret_api_key"):  # I know this should be in the .env file but for the sake of this example, I am hardcoding it here
        raise HTTPException(status_code=401, detail="Invalid API Key")

    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.is_sold = True

    session.add(book)
    session.commit()
    session.refresh(book)

    return book