from fastapi import APIRouter, HTTPException
from src.app.schemas.login import LoginRequestBody, LoginResponse
from src.app.api import auth
from src.app.models import User
from src.app.db.session import session_scope

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(user: LoginRequestBody):
    with session_scope() as db:
        db_user = db.query(User).filter(User.email == user.email, User.password == user.password).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Email or Password is incorrect")
        
        payload = {
            "id": db_user.id,
            "email": db_user.email,
            "name": db_user.name,
            "user_type": db_user.user_type
        }
        token = auth.create_token(payload)
        response = LoginResponse(**token.dict(), **payload)
        return response
