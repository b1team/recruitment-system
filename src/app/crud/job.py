from typing import List

from sqlalchemy.orm.session import Session

from src.app.exceptions import JobNotFoundError
from src.app.schemas.job import JobModel, JobPublicInfo, JobBase
from src.app.models import Job
from src.app.crud.tag import CRUDTag


class CRUDJob:
    def __init__(self, session: Session):
        self.db = session

    def create(self, job: JobModel):
        tag_crud = CRUDTag(self.db)
        not_exist_tags = tag_crud.get_not_exist_tags(job.tags)
        if not_exist_tags:
            tag_crud.create_many(not_exist_tags)
        tags = tag_crud.get_many(job.tags)
        new_job = Job(**job.dict())
        new_job.tags.extend(tags)
        self.db.add(new_job)

    def get(self, job_id: int):
        job = self.db.query(Job).get(job_id)
        if not job:
            raise JobNotFoundError()
        return JobPublicInfo(job.__dict__)

    def get_many(self, job_ids: List[int]):
        jobs = self.db.query(Job).filter(Job.id.in_(job_ids))
        results = []
        for job in jobs:
            results.append(JobPublicInfo(*job.__dict__))
        return results

    def update(self, job_id: int, **info):
        job = self.db.query(Job).get(job_id)
        if not job:
            raise JobNotFoundError()
        for key, value in info.items():
            if hasattr(job, key):
                setattr(job, key, value)
        self.db.add(job)

    def delete(self, job_id: int):
        job = self.db.query(Job).get(job_id)
        if not job:
            raise JobNotFoundError()
        self.db.delete(job)
