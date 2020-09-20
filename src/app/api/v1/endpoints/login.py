from fastapi import APIRouter, HTTPException
from src.app.schemas.login import LoginRequestBody, LoginResponse
from src.app.handlers.login import LoginHandler
from src.app.api import auth
from src.app.db.base import database

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(user: LoginRequestBody):
    login_handler = LoginHandler(database)
    user_in_db = login_handler.check_user(user)
    user_in_db = {"password": "1", "username": "vuonglv"}
    # TODO: Get user
    if not user_in_db or user_in_db.get("password") != user.password:
        raise HTTPException(status_code=401, detail="Username or password is incorrect!")

    token = auth.create_token(username=user.username)
    return LoginResponse(**token.dict(), username=user.username)
