from typing import Optional
from datetime import datetime

from slugify import slugify

from fastapi import APIRouter, Body, Depends, Query
from src.app.db.session import session_scope
from src.app.crud.job import CRUDJob
from src.app.schemas.job import JobPublicInfo, JobModel, ListJobPublic, UpdateJobModel, CreateJobBody
from src.app.api import auth
from src.app.exceptions import *
from src.app.constants import UserType
from src.app.models import Employer, Job
from src.app.schemas.filters.job import JobFilter
from src.app.api.dependencies import job_filter

router = APIRouter()


@router.post("/jobs", response_model=JobPublicInfo)
async def create_job(job_info: CreateJobBody = Body(...), identities=Depends(auth.check_token)):
    if identities.user_type != UserType.employer.value:
        raise AuthorizationError()

    with session_scope() as db:
        employer = db.query(Employer.id).filter(Employer.user_id == identities.id).first()
        if not employer:
            raise BadRequestsError("User is not employer")
        crud = CRUDJob(db)
        now = str(int(datetime.utcnow().timestamp()))
        slug = "-".join([slugify(job_info.title), now])
        job = JobModel(**job_info.dict(), slug=slug, employer_id=employer.id)
        crud.create(job)
    return job


@router.get("/jobs", response_model=ListJobPublic)
async def get_all_jobs(offset: Optional[int] = Query(None, gte=0),
                       limit: Optional[int] = Query(None, gte=0),
                       job: JobFilter = Depends(job_filter)):
    with session_scope() as db:
        crud = CRUDJob(db)
        jobs, total = crud.get_many(offset=offset, limit=limit, job_filter=job)
    return {
        "jobs": jobs,
        "total": total
    }


@router.get("/jobs/{job_id}", response_model=JobPublicInfo)
async def get_job(job_id: str):
    with session_scope() as db:
        crud = CRUDJob(db)
        job = crud.get(job_id)
    if not job:
        return {}
    return job


@router.put("/jobs/{job_id}")
async def update(job_id: str, job_info: UpdateJobModel = Body(...), identities=Depends(auth.check_token)):
    if identities.user_type != UserType.employer.value:
        raise AuthorizationError()
    with session_scope() as db:
        job = db.query(Job.employer_id, Employer.user_id).join(Employer.jobs).filter(Job.id == job_id).first()
        if not job:
            raise JobNotFoundError(job_id)
        if job.user_id != identities.id:
            raise AuthorizationError()
        crud = CRUDJob(db)
        crud.update(job_id, **job_info.dict(exclude_unset=True))
    return {
        "status": "updated",
        "job_id": job_id,
        "updated": job_info.dict(exclude_unset=True)
    }

@router.delete("/jobs/{job_id}")
async def delete(job_id: str, identities=Depends(auth.check_token)):
    if identities.user_type != UserType.employer.value:
        raise AuthorizationError()
    with session_scope() as db:
        job = db.query(Job.employer_id, Employer.user_id).join(Employer.jobs).filter(Job.id == job_id).first()
        if not job:
            raise JobNotFoundError(job_id)
        if job.user_id != identities.id:
            raise AuthorizationError()
        crud = CRUDJob(db)
        crud.delete(job_id)
    return {
        "status": "deleted",
        "job_id": job_id
    }
