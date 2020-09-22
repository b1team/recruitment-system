from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequestBody(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: str
    phone_number: Optional[str] = None


class RegisterResponse(BaseModel):
    email: EmailStr
    name: str
    phone_number: str
