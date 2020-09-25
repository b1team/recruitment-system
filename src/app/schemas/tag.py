from pydantic import BaseModel
from typing import Optional, List

class TagBase(BaseModel):
    name: str
    description: Optional[str] = None

class PayloadTag(BaseModel):
    tags: Optional[List[str]]