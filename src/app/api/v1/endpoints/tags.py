from fastapi import APIRouter, Query
from typing import Optional

from src.app.models import *
from src.app.db.session import session_scope

from src.app.schemas.tag import TagBase, PayloadTag

from src.app.crud.tag import CRUDTag
from src.app.exceptions import JobNotFoundError

router = APIRouter()


@router.post('/tags/{job_id}')
async def create_tags(job_id: int, payload: PayloadTag):
    with session_scope() as db:
        crud = CRUDTag(db)
        not_exist_tags = crud.get_not_exist_tags(payload.tags)
        if not_exist_tags:
            crud.create_many(not_exist_tags)
        tags = crud.get_many(payload.tags)
        if tags:
            job = db.query(Job).get(job_id)
            if not job:
                raise JobNotFoundError(info={'job_id': job_id})
            job.tags.extend(tags)

    return payload
