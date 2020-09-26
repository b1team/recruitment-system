from pydantic import BaseModel
from typing import List, Optional

class EmployeeFilter(BaseModel):
    employee_id: Optional[str] = None
