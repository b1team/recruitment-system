from fastapi import APIRouter, HTTPException, Depends, status
from src.app.db.session import session_scope
from src.app.api import auth

from src.app.models import User

from src.app.schemas.token import Identities
from src.app.schemas.upgrade import PayloadEmployee, PayloadEmployer

from src.app.schemas.employee import EmployeeBase
from src.app.schemas.employer import EmployerBase

from src.app.crud.employer import CRUDemployer
from src.app.crud.employee import CRUDemployee

from src.app.constants import UserType

from src.app.exceptions import *

router = APIRouter()


def check_requests_body(payload, identities):
    if identities.id != payload.user_id:
        raise AuthorizationError()
    if identities.user_type != UserType.viewer.value:
        raise BadRequestsError()
    if identities.user_type == payload.user_type:
        raise BadRequestsError()


@router.post("/upgrade/employee")
async def upgrade(payload: PayloadEmployee, identities: Identities = Depends(auth.check_token)):
    check_requests_body(payload, identities)
    if payload.user_type != UserType.employee.value:
        raise BadRequestsError()
    with session_scope() as db:
        crud = CRUDemployee(db)
        crud.create(EmployeeBase(**payload.dict()))
        user = db.query(User).filter(User.id == payload.user_id).first()
        user.user_type = payload.user_type

    return payload


@router.post("/upgrade/employer")
async def upgrade(payload: PayloadEmployer, identities: Identities = Depends(auth.check_token)):
    check_requests_body(payload, identities)
    if payload.user_type != UserType.employer.value:
        raise BadRequestsError()
    with session_scope() as db:
        crud = CRUDemployer(db)
        crud.create(EmployerBase(**payload.dict()))
        user = db.query(User).filter(User.id == payload.user_id).first()
        user.user_type = payload.user_type

    return payload
