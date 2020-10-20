from fastapi import APIRouter, Depends, Body, Query
from typing import Optional, List
from src.app.api.dependencies import apply_filter, employee_filter, job_filter, employer_jobs_filter

from src.app.db.session import session_scope
from src.app.schemas.token import Identities
from src.app.api import auth

from src.app.models import Apply, Job, Employer, User
from src.app.db.constants import ApplyStatus
from src.app.constants import UserType
from src.app.exceptions import BadRequestsError, AuthenticationError, AuthorizationError, AuthenError, EmployeeNotFoundError
from src.app.crud.employer import CRUDemployer
from src.app.crud.job import CRUDJob

from src.app.schemas.filters.apply import ApplyFilter
from src.app.schemas.filters.employee import EmployeeFilter
from src.app.schemas.filters.job import JobFilter

from src.app.schemas.apply import PayloadUpdateApply
from src.app.schemas.employer import EmployerUpdate, GetEmployerResponse
from src.app.schemas.job import GetEmployerJobsResponse
from src.app.schemas.employer import EmployerCreate, EmployerInDB

router = APIRouter()



@router.get('/employers/{employer_id}/applies')
async def applied_jobs(employer_id: Optional[int],
                       offset: Optional[int] = Query(None, gte=0),
                       limit: Optional[int] = Query(None, gte=0),
                       applied: ApplyFilter = Depends(apply_filter),
                       employee: EmployeeFilter = Depends(employee_filter),
                       job: JobFilter = Depends(job_filter),
                       identities: Identities = Depends(auth.check_token)):

    if identities.user_type != UserType.employer.value:
        raise AuthenticationError

    with session_scope() as db:
        crud = CRUDemployer(db)
        user = db.query(Employer.user_id).filter(Employer.id == employer_id).first()
        if not user:
            raise BadRequestsError("employer_id is not legal")
        if user.user_id != identities.id:
            raise AuthenticationError
        applied_jobs_info, total = crud.get_applied_job(employer_id, offset, 
                                                        limit, applied, employee, job)

    return {
        "applied": applied_jobs_info,
        "total": total
    }


@router.put('/employers/{employer_id}/applies')
async def update_applied_job(employer_id: Optional[int],
                             payload: PayloadUpdateApply,
                             identities: Identities = Depends(auth.check_token)):

    if identities.user_type != UserType.employer.value:
        raise AuthenticationError
    if payload.status not in [ApplyStatus.pending.value,
                              ApplyStatus.approved.value,
                              ApplyStatus.rejected.value]:
        raise BadRequestsError("'status' is not legal")

    with session_scope() as db:
        crud = CRUDemployer(db)
        user = db.query(Employer.user_id).filter(Employer.id == employer_id).first()
        if not user:
            raise BadRequestsError("employer_id is not legal")
        if user.user_id != identities.id:
            raise AuthenticationError
        crud.update_apply_status(payload.apply_id, payload.status)
    return {
        "status": "updated",
        "apply_id": payload.apply_id,
        "employer_id": employer_id,
        "updated": f"apply status to {payload.status}"
    }


@router.put('/employers/{employer_id}')
async def update_employer(employer_id: Optional[int],
                          employer_info: EmployerUpdate = Body(...),
                          identities: Identities = Depends(auth.check_token)):

    if identities.user_type != UserType.employer.value:
        raise AuthenticationError
    
    with session_scope() as db:
        user = db.query(Employer.user_id).filter(Employer.id == employer_id).first()
        if not user:
            raise BadRequestsError("employer_id is not legal")
        if user.user_id != identities.id:
            raise AuthenticationError
        crud = CRUDemployer(db)
        crud.update(employer_id, **employer_info.dict())
    return {
        "status": "updated",
        "employer_id": employer_id,
        "updated": employer_info.dict()
    }


def check_requests_body(payload, identities):
    if identities.user_type != UserType.viewer.value:
        raise BadRequestsError()
    if identities.user_type == UserType.employer.value:
        raise BadRequestsError()


@router.post("/employers")
async def upgrade(payload: EmployerCreate, identities: Identities = Depends(auth.check_token)):
    check_requests_body(payload, identities)
    with session_scope() as db:
        crud = CRUDemployer(db)
        crud.create(EmployerInDB(user_id=identities.id, **payload.dict()))
        user = db.query(User).get(identities.id)
        user.user_type = UserType.employer.value
    return {
        "status": "upgraded",
        "user_type": "employer",
        "info": payload.dict()
    }


@router.get("/employers/{employer_id}/jobs", response_model=GetEmployerJobsResponse)
async def get_employer_jobs(employer_id: int, identities: Identities = Depends(auth.check_token),
                  offset: Optional[int] = Query(None, gte=0),
                  limit: Optional[int] = Query(None, gte=0),
                  job_filters: JobFilter = Depends(employer_jobs_filter)):
    if identities.user_type != UserType.employer.value:
        raise AuthorizationError("Bạn không phải nhà tuyển dụng")
    if identities.employer_id != employer_id:
        raise AuthorizationError("Bạn không thể quản lý công việc của nhà tuyển dụng khác")
    with session_scope() as db:
        crud_job = CRUDJob(db)
        job_filters.employer_id = employer_id
        jobs, total = crud_job.get_many(offset=offset, limit=limit, job_filter=job_filters)
    return GetEmployerJobsResponse(jobs=jobs, total=total)


@router.get("/employers/{employer_id}", response_model=GetEmployerResponse)
async def get_one_employer(employer_id: str):
    with session_scope() as db:
        employer = db.query(Employer).get(employer_id)
        if not employer:
            raise EmployeeNotFoundError(employer_id)
        
        return GetEmployerResponse(**employer.__dict__)
