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
from src.app.api.auth import token_status

router = APIRouter()


def check_requests_body(payload, identities):
    if identities.id != payload.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if identities.user_type != UserType.viewer.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if identities.user_type == payload.user_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


def check_token_status(db, payload, identities):
    if not token_status(db, payload.user_id, identities.updated):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Old token")


@router.post("/upgrade/employee")
async def upgrade(payload: PayloadEmployee, identities: Identities = Depends(auth.check_token)):
    check_requests_body(payload, identities)
    if payload.user_type != UserType.employee.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    with session_scope() as db:
        check_token_status(db, payload, identities)
        crud = CRUDemployee(db)
        crud.create(EmployeeBase(**payload.dict()))
        user = db.query(User).filter(User.id == payload.user_id).first()
        user.user_type = payload.user_type

    return payload


@router.post("/upgrade/employer")
async def upgrade(payload: PayloadEmployer, identities: Identities = Depends(auth.check_token)):
    check_requests_body(payload, identities)
    if payload.user_type != UserType.employer.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    with session_scope() as db:
        check_token_status(db, payload, identities)
        crud = CRUDemployer(db)
        crud.create(EmployerBase(**payload.dict()))
        user = db.query(User).filter(User.id == payload.user_id).first()
        user.user_type = payload.user_type

    return payload
