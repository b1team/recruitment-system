from fastapi import APIRouter, Query
from typing import Optional

from src.app.models import *
from src.app.db.session import session_scope

from src.app.schemas.tag import TagBase, PayloadTag

from src.app.crud.tag import CRUDTag

router = APIRouter()


def add_job_tag(db, job_id, tags):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    db_job.tags.extend(tags)


@router.post('/tags/{job_id}')
async def tags(job_id: int, payload: PayloadTag):
    with session_scope() as db:
        crud = CRUDTag(db)
        usable_tag = crud.filter(PayloadTag(**payload.dict()))
        crud.create(usable_tag)
        tag = crud.get(PayloadTag(**payload.dict()))
        if tag:
            add_job_tag(db, job_id, tag)
    return payload
