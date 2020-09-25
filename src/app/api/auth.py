from fastapi import status, HTTPException, Header
from typing import Optional
import jwt
from jwt.exceptions import InvalidTokenError
from src.app.config import settings
from src.app.schemas.token import Token, Payload, Identities
from datetime import datetime, timedelta
from src.app.models import User
from src.app.db.session import session_scope, Session

from src.app.exceptions import AuthenticationError


def check_token(bearer_token: str = Header(..., alias="Authorization")):
    if not bearer_token.startswith("Bearer "):
        raise AuthenticationError
    _, _, token = bearer_token.partition("Bearer ")
    if not token:
        raise AuthenticationError
    try:
        decoded = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=["HS256"])
    except InvalidTokenError:
        raise AuthenticationError
    else:
        identities = Identities(**decoded)
        with session_scope() as db:
            if is_out_of_date(db, identities):
                raise AuthenticationError
        return identities


def is_out_of_date(db, identities):
    user = db.query(User.updated_at).filter(User.id == identities.id).first()
    if not user:
        return False
    user_updated_time = user.updated_at.isoformat()
    return user_updated_time != identities.updated


def get_user_updated_time(user_id):
    with session_scope() as db:
        user = db.query(User.updated_at).filter(User.id == user_id).first()
        updated = user.updated_at.isoformat()
        return updated
        

def create_token(identities: dict) -> Token:
    updated_at = get_user_updated_time(identities['id'])
    created_at = datetime.utcnow()
    expire_at = created_at + timedelta(hours=settings.TOKEN_LIFETIME)
    payload = Payload(**identities, exp=expire_at, iat=created_at, updated=updated_at)
    access_token = jwt.encode(payload.dict(), key=settings.TOKEN_SECRET_KEY, algorithm="HS256")
    token = Token(access_token=access_token,
                  expire_at=expire_at,
                  created_at=created_at)
    return token
