from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class LoginRequestBody(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    id: int
    email: EmailStr
    user_type: str
    expire_at: datetime
    created_at: datetime
    employer_id: Optional[int] = None
    employee_id: Optional[int] = None
