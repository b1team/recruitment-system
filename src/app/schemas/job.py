from pydantic import BaseModel
from typing import List


class JobBase(BaseModel):
    title: str
    salary: float
    address: str
    description: str
    is_open: bool = True


class JobModel(JobBase):
    tags: List[str]


class JobPublicInfo(JobModel):
    id: int
    employer_id: int
