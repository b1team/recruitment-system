from pydantic import BaseModel
from typing import Optional


class EmployerUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: str
    address: str
    type: str


class EmployerCreate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: str
    address: str
    type: str
    active: bool


class EmployerInDB(EmployerCreate):
    user_id: int
