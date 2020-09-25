from fastapi import APIRouter

router = APIRouter()


@router.post("/jobs")
async def create_job():
    ...


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
