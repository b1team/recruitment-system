from fastapi import APIRouter, Depends
from typing import Optional

from src.app.db.session import session_scope
from src.app.schemas.token import Identities
from src.app.api import auth

from src.app.models import Apply, Job, Employer

from src.app.constants import UserType
from src.app.exceptions import BadRequestsError
from src.app.crud.employer import CRUDemployer

router = APIRouter()

@router.get('/employers/{employer_id}/applies')
async def applied_jobs(employer_id: Optional[int],
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

        applied_jobs_info = crud.get_applied_job(employer_id)
    return applied_jobs_info


@router.put('/employers/{employer_id}/applies')
async def update_applied_job(employer_id: Optional[int],
                             identities: Identities = Depends(auth.check_token)):
    pass


