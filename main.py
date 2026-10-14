from fastapi import FastAPI
from routes.books import router as books_router
from routes.users import router as users_router
from database import create_db

app = FastAPI(title="DU Book App", description="A simple book management API", version="1.0.0")

app.include_router(books_router)
app.include_router(users_router)

@app.on_event("startup")
def on_startup():
    """
    Event handler for application startup.
    This function is called when the application starts.
    It creates the database tables if they do not exist.
    """
    create_db()

@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "Welcome to the Kitaab API! The API is running smoothly."}

#Handling Events
