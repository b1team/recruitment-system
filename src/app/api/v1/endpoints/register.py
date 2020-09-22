from fastapi import APIRouter, HTTPException

from src.app.models import User
from src.app.db.session import session_scope
from src.app.schemas.user import UserPublicInfo
from src.app.schemas.register import RegisterRequestBody, RegisterResponse

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
async def register(user: RegisterRequestBody):
    with session_scope() as db:
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_user = User(email=user.email, password=user.password, name=user.name, phone_number=user.phone_number)
        db.add(new_user)
        return user

