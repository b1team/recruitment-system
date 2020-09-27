from pydantic import BaseModel
from typing import List, Optional


class ApplyFilter(BaseModel):
    apply_status: Optional[List[str]] = None
