from fastapi import APIRouter, Body, Depends
from src.app.db.session import session_scope
from src.app.crud.job import CRUDJob
from src.app.schemas.job import JobBase, JobPublicInfo
from src.app.api import auth

router = APIRouter()


@router.post("/jobs", response_model=JobPublicInfo)
async def create_job(job: JobBase = Body(...), identities=Depends(auth.check_token)):
    with session_scope() as db:
        crud = CRUDJob(db)
        crud.create()


@router.get("/jobs")
async def get_all_jobs():
    ...


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    ...


@router.put("/jobs/{job_id}")
async def update(job_id: str):
    ...


@router.delete("/jobs/{job_id}")
async def delete(job_id: str):
    ...
