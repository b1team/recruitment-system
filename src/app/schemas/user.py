from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    phone_number: Optional[str] = None


class UserInDB(UserBase):
    password: str
    token: str


class UserUpdate(UserBase):
    email: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None


class UserPublicInfo(UserBase):
    id: int
