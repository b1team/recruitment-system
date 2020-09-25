from fastapi import APIRouter, Depends
from src.app.db.session import session_scope
from src.app.schemas.token import Identities
from src.app.api import auth
from src.app.models import Employee, Job

from src.app.schemas.apply import ApplyBase
from src.app.constants import UserType

from src.app.exceptions import *

router = APIRouter()


@router.post('/apply')
async def apply_job(payload: ApplyBase, identities: Identities = Depends(auth.check_token)):
    if identities.user_type != UserType.employee.value:
        raise AuthenticationError

    with session_scope() as db:
        job = db.query(Job.is_open).get(payload.job_id)
        if not job:
            raise JobNotFoundError({'job_id': payload.job_id})
        if not job.is_open:
            raise BadRequests("Jobs are closed")
        employee = db.query(Employee.id).get(identities.id)
        if not employee:
            raise BadRequests("")
        employee_id = employee.id

        

        
        