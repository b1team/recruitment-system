from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.app.db.constants import ApplyStatus


class ApplyJobInfo(BaseModel):
    id: str
    is_open: bool
    slug: Optional[str] = None
    created_at: Optional[datetime] = None


class GetApplyResponse(BaseModel):
    id: int
    job: ApplyJobInfo
    description: Optional[str] = None
    cv: str
    status: Optional[str] = 'pending'
    created_at: datetime
    

class ApplyBase(BaseModel):
    job_id: int
    description: Optional[str] = None
    cv: str
    status: Optional[str] = "pending"


class ApplyInDB(ApplyBase):
    employee_id: int


class EmployeeUpdateApplyModel(BaseModel):
    description: Optional[str] = None
    cv: Optional[str] = None

      
class PayloadUpdateApply(BaseModel):
    apply_id: int
    status: Optional[str] = 'pending'


class CreateApplyPayload(BaseModel):
    job_id: int
    description: Optional[str] = None
    cv: str