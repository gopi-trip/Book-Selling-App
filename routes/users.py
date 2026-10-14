from fastapi import Depends, HTTPException, APIRouter
from auth import verify_api_key
from sqlmodel import Session, select
from models.user import User, UserRead, UserCreate
from database import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/", response_model=UserRead)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    """
    Register a new user in the system.
    """
    #Match the API Key with the one in the .env file
    if(api_key != "my_secret_api_key"): # I know this should the .env file but for the sake of this example, I am hardcoding it here
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Check if the email already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user instance
    user = User.model_validate(user_data)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    """
    Get user details by user ID.
    """
    #Match the API Key with the one in the .env file
    if(api_key != "my_secret_api_key"): # I know this should the .env file but for the sake of this example, I am hardcoding it here
        raise HTTPException(status_code=401, detail="Invalid API Key")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
