from fastapi import APIRouter, Depends
from src.app.db.session import session_scope
from src.app.schemas.token import Identities
from src.app.api import auth
from src.app.models import Employee, Job

from src.app.schemas.apply import ApplyInDB, ApplyBase
from src.app.constants import UserType
from src.app.crud.apply import CRUDapply
from src.app.models import Apply
from src.app.exceptions import *

router = APIRouter()


@router.post('/apply')
async def apply_job(payload: ApplyBase, identities: Identities = Depends(auth.check_token)):
    if identities.user_type != UserType.employee.value:
        raise AuthenticationError

    with session_scope() as db:
        job = db.query(Job.is_open).filter(Job.id == payload.job_id).first()
        if not job:
            raise JobNotFoundError({'job_id': payload.job_id})
        if not job.is_open:
            raise BadRequests("Job is closed")

        employee = db.query(Employee.id).filter(Employee.user_id == identities.id).first()
        if not employee:
            raise BadRequestsError("User is not employee!!")

        applied = db.query(Apply).filter(Apply.employee_id == employee.id, Apply.job_id == payload.job_id).first()
        if applied:
            raise BadRequestsError('You are applied this job!')

        crud = CRUDapply(db)
        apply_info = {
            'employee_id': employee.id,
            'job_id': payload.job_id,
            'description': payload.description,
            'cv': payload.cv
        }
        crud.create(ApplyInDB(**apply_info))
    return payload


        

        
        