from pydantic import BaseModel
from typing import Optional
from src.app.db.constants import ApplyStatus


class ApplyBase(BaseModel):
    id: int
    job_id: int
    description: Optional[str] = None
    cv: str
    status: Optional[str] = 'pending'


class ApplyInDB(ApplyBase):
    employee_id: int


class EmployeeUpdateApplyModel(BaseModel):
    description: Optional[str] = None
    cv: Optional[str] = None

      
class PayloadUpdateApply(BaseModel):
    apply_id: int
    status: Optional[str] = 'pending'
