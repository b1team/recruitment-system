from fastapi import status, HTTPException, Header
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from src.app.config import settings
from src.app.schemas.token import Token, Payload, Identities
from datetime import datetime, timedelta


def check_token(bearer_token: str = Header(..., alias="Authorization")):
    if not bearer_token.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")
    _, _, token = bearer_token.partition("Bearer ")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")
    try:
        decoded = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=["HS256"])
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied")
    else:
        return Identities(**decoded)


def create_token(identities: dict) -> Token:
    created_at = datetime.utcnow()
    expire_at = created_at + timedelta(hours=settings.TOKEN_LIFETIME)
    payload = Payload(**identities, exp=expire_at, iat=created_at)
    access_token = jwt.encode(payload.dict(), key=settings.TOKEN_SECRET_KEY, algorithm="HS256")
    token = Token(access_token=access_token,
                  expire_at=expire_at,
                  created_at=created_at)
    return token
