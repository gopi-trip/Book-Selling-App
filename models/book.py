from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    author: str = Field(index=True)
    price: int
    is_sold: bool = Field(default=False)

    #Foreign key to link the book to its owner (User)
    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="books")


# Request Body for creating a new book
class BookCreate(SQLModel):
    title: str
    author: str
    price: int
    user_id: int  # Foreign key to link the book to its owner (User)


# Response model for returning book data
class BookRead(SQLModel):
    id: int
    title: str  
    author: str
    price: int
    is_sold: bool
    user_id: int  # Foreign key to link the book to its owner (User)

class BookUpdate(SQLModel):
    is_sold: Optional[bool] = None
    price: Optional[int] = None

from models.user import User
Book.model_rebuild()