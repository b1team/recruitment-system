from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    user_id: int
