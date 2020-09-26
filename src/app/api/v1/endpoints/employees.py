from fastapi import APIRouter, Depends
from typing import Optional

from src.app.db.session import session_scope
from src.app.schemas.token import Identities
from src.app.schemas.filters.apply import ApplyFilter
from src.app.api.dependencies import apply_filter

from src.app.api import auth
from src.app.models import Apply, Job, User, Employee

from src.app.constants import UserType
from src.app.exceptions import BadRequestsError, AuthenticationError

from src.app.crud.employee import CRUDemployee

router = APIRouter()


def check_requests_body(identities):
    if identities.user_type != UserType.viewer.value:
        raise BadRequestsError()
    if identities.user_type == UserType.employee.value:
        raise BadRequestsError()


@router.get('/employees/{employee_id}/applies')
async def applied_jobs(employee_id: Optional[int], applied: ApplyFilter = Depends(apply_filter),
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

        applied_jobs_info = crud.get_applied_job(employee_id, applied=applied)
    return applied_jobs_info


@router.post("/employees")
async def upgrade(identities: Identities = Depends(auth.check_token)):
    check_requests_body(identities)
    with session_scope() as db:
        crud = CRUDemployee(db)
        crud.create(user_id=identities.id)
        user = db.query(User).get(identities.id)
        user.user_type = UserType.employee.value
    return {
        "status": "upgraded",
        "user_type": "employee"
    }


