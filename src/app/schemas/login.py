from pydantic import BaseModel
from datetime import datetime


class LoginRequestBody(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    username: str
    expire_at: datetime
    created_at: datetime
