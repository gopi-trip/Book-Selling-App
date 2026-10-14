from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

# Database table for the user
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True)
    college: str

    #Relationship between User and Books
    books: list["Book"] = Relationship(back_populates="owner")


# Request Body for creating a new user
class UserCreate(SQLModel):
    name: str
    email: str
    college: str

# Response model for returning user data
class UserRead(SQLModel):
    id: int
    name: str
    email: str
    college: str



# Avoid Circular Import 
from models.book import Book
User.model_rebuild()
