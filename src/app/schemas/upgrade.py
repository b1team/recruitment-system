from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from src.app.schemas.employee import EmployeeBase
from src.app.schemas.employer import EmployerBase


class PayloadBase(BaseModel):
    user_id: int
    user_type: str

class PayloadEmployee(PayloadBase):
    ...

class PayloadEmployer(PayloadBase):
    name: Optional[str] = None
    description: str
    code: Optional[str] = None
    address: str
    type: str
    active: bool
    
