from pydantic import BaseModel
from typing import Optional


class ApplyBase(BaseModel):
    job_id: int
    description: Optional[str] = None
    cv: str
    status: Optional[str] = 'pending'


class ApplyInDB(ApplyBase):
    employee_id: int
