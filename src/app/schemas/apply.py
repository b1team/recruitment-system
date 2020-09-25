from pydantic import BaseModel
from typing import Optional

from src.app.constants import UserType


class ApplyBase(BaseModel):
    job_id: int
    description: Optional[str] = None
    cv: str
    status: UserType


class ApplyInDB(ApplyBase):
    employee_id: int
