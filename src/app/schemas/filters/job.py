from pydantic import BaseModel
from typing import List, Optional

class JobFilter(BaseModel):
    job_id: Optional[int] = None
    only_open_job: Optional[bool] = None
    employer_name: Optional[str] = None
    employer_id: Optional[str] = None
