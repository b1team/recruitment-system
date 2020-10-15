from fastapi import APIRouter, Depends, Body
from src.app.db.session import session_scope
from src.app.exceptions import BadRequestsError, AuthenticationError, JobNotFoundError, AuthorizationError, ApplyNotFoundError
from src.app.schemas.token import Identities
from src.app.api import auth
from src.app.models import Employee, Job

from src.app.schemas.apply import ApplyInDB, ApplyBase, EmployeeUpdateApplyModel
from src.app.constants import UserType
from src.app.crud.apply import CRUDApply
from src.app.models import Apply

router = APIRouter()


@router.post('/applies')
async def apply_job(payload: ApplyBase, identities: Identities = Depends(auth.check_token)):
    if identities.user_type != UserType.employee.value:
        raise AuthenticationError

    with session_scope() as db:
        job = db.query(Job.is_open).filter(Job.id == payload.job_id).first()
        if not job:
            raise JobNotFoundError({'job_id': payload.job_id})
        if not job.is_open:
            raise BadRequestsError("Job is closed")

        employee = db.query(Employee.id).filter(Employee.user_id == identities.id).first()
        if not employee:
            raise BadRequestsError("User is not employee!!")

        applied = db.query(Apply).filter(Apply.employee_id == employee.id, Apply.job_id == payload.job_id).first()
        if applied:
            raise BadRequestsError('You are applied this job!')

        crud = CRUDApply(db)
        apply_info = {
            'employee_id': employee.id,
            'job_id': payload.job_id,
            'description': payload.description,
            'cv': payload.cv
        }
        crud.create(ApplyInDB(**apply_info))
    return payload


@router.put("/applies/{apply_id}")
async def update_apply(apply_id: str, update_info: EmployeeUpdateApplyModel = Body(...),
                       identities: Identities = Depends(auth.check_token)):
    if identities.user_type != UserType.employee.value:
        raise AuthorizationError()
    with session_scope() as db:
        apply = db.query(Employee.user_id).join(Employee.applies).filter(Apply.id == apply_id).first()
        if not apply:
            raise ApplyNotFoundError(apply_id)
        if apply.user_id != identities.id:
            raise AuthorizationError()
        crud = CRUDApply(db)
        crud.update(apply_id, **update_info.dict(exclude_unset=True))
    return {
        "status": "updated",
        "apply_id": apply_id,
        "updated": update_info.dict(exclude_unset=True)
    }


@router.delete("/applies/{apply_id}")
async def delete_apply(apply_id: str, identities: Identities = Depends(auth.check_token)):
    if identities.user_type != UserType.employee.value:
        raise AuthorizationError()
    with session_scope() as db:
        apply = db.query(Employee.user_id).join(Employee.applies).filter(Apply.id == apply_id).first()
        if not apply:
            raise ApplyNotFoundError(apply_id)
        if apply.user_id != identities.id:
            raise AuthorizationError()
        crud = CRUDApply(db)
        crud.delete(apply_id)
    return {
        "status": "deleted",
        "apply_id": apply_id
    }

@router.get("/applies/{apply_id}")
async def get_apply(apply_id: str, identities: Identities = Depends(auth.check_token)):
    if identities.user_type not in {UserType.employee.value, UserType.employer.value}:
        raise AuthorizationError()
    apply = None
    with session_scope() as db:
        apply = db.query(Apply).filter(Apply.id == apply_id).first()
        if not apply:
            raise ApplyNotFoundError(apply_id)
        return ApplyBase(id=apply.id, job_id=apply.job_id, description=apply.description, cv=apply.cv, status=apply.status.value)