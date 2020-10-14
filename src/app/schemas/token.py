from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Identities(BaseModel):
    id: int
    email: EmailStr
    user_type: str
    name: Optional[str] = None
    updated: str
    employer_id: Optional[int] = None
    employee_id: Optional[int] = None


class Payload(Identities):
    exp: datetime
    iat: datetime


class Token(BaseModel):
    access_token: str
    expire_at: datetime
    created_at: datetime
