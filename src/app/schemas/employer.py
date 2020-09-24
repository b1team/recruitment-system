from pydantic import BaseModel
from typing import Optional

class EmployerBase(BaseModel):
    user_id: int
    name: Optional[str] = None
    code: Optional[str] = None
    description: str
    address: str
    type: str
    active: bool




