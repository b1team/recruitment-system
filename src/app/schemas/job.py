from pydantic import BaseModel
from typing import List, Optional


class JobBase(BaseModel):
    title: str
    salary: float
    address: str
    description: str
    is_open: bool = True
    tags: List[str]


class UpdateJobModel(BaseModel):
    title: Optional[str] = None
    salary: Optional[float] = None
    address: Optional[str] = None
    description: Optional[str] = None
    is_open: Optional[bool] = None
    tags: Optional[List[str]] = None


class JobModel(JobBase):
    employer_id: int


class JobPublicInfo(JobModel):
    id: Optional[int] = None


class ListJobPublic(BaseModel):
    jobs: List[JobPublicInfo]
    total: int
