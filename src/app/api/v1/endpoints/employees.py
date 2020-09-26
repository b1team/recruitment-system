from fastapi import APIRouter, Depends
from typing import Optional

from src.app.db.session import session_scope
from src.app.schemas.token import Identities
from src.app.api import auth

from src.app.models import Apply, Job, Employee

from src.app.constants import UserType
from src.app.exceptions import BadRequestsError

from src.app.crud.employee import CRUDemployee

router = APIRouter()

@router.get('/employees/{employee_id}/applies')
async def applied_jobs(employee_id: Optional[int],
                       identities: Identities = Depends(auth.check_token)):

    if identities.user_type != UserType.employee.value:
        raise AuthenticationError

    with session_scope() as db:
        crud = CRUDemployee(db)
        user = db.query(Employee.user_id).filter(Employee.id == employee_id).first()
        if not user:
            raise BadRequestsError("employee_id is not legal")
        
        if user.user_id != identities.id:
            raise AuthenticationError

        applied_jobs_info = crud.get_applied_job(employee_id)
    return applied_jobs_info


@router.delete('/employees/{employee_id}/applies')
async def delete_applied_job(employee_id: Optional[int], job_id: Optional[int] = None,
                             identities: Identities = Depends(auth.check_token)):
    pass


@router.put('/employees/{employee_id}/applies')
async def update_applied_job(employee_id: Optional[int], job_id: Optional[int],
                             identities: Identities = Depends(auth.check_token)):
    pass



