from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class JobBase(BaseModel):
    title: str
    slug: str
    salary: float
    address: str
    brief: Optional[str] = None
    description: str
    is_open: bool = True
    tags: List[str]


class UpdateJobModel(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    salary: Optional[float] = None
    address: Optional[str] = None
    brief: Optional[str] = None
    description: Optional[str] = None
    is_open: Optional[bool] = None
    tags: Optional[List[str]] = None


class JobModel(JobBase):
    employer_id: int


class JobPublicInfo(JobModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None


class ListJobPublic(BaseModel):
    jobs: List[JobPublicInfo]
    total: int


class CreateJobBody(BaseModel):
    title: str
    salary: float
    address: str
    brief: Optional[str] = None
    description: str
    tags: List[str]


class GetJobResponse(BaseModel):
    title: str
    slug: str
    salary: float
    address: str
    is_open: bool = True
    description: str
    tags: List[str]
    employer_id: str


class GetEmployerJobsResponse(BaseModel):
    total: int
    jobs: List[JobPublicInfo]
