from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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
    

class GetEmployerResponse(BaseModel):
    name: str
    code: str
    description: str
    address: str
    type: str
    created_at: datetime
    id: int
