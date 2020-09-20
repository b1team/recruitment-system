from pydantic import BaseModel
from datetime import datetime


class Payload(BaseModel):
    username: str
    exp: datetime
    iat: datetime


class Token(BaseModel):
    access_token: str
    expire_at: datetime
    created_at: datetime
