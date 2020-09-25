from pydantic import BaseModel
from typing import List


class JobBase(BaseModel):
    title: str
    salary: float
    address: str
    description: str
    is_open: bool = True
    tags: List[str]


class JobModel(JobBase):
    employer_id: int


class JobPublicInfo(JobModel):
    id: int
