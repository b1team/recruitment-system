from typing import List, Optional
import copy

from sqlalchemy.orm.session import Session

from src.app.exceptions import JobNotFoundError
from src.app.schemas.job import JobPublicInfo, JobModel
from src.app.models import Job, Employer
from src.app.crud.tag import CRUDTag

from src.app.schemas.filters.job import JobFilter


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
        new_job.tags = tags.all()
        self.db.add(new_job)
        return new_job

    def get(self, job_id: int):
        job = self.db.query(Job).get(job_id)
        if not job:
            raise JobNotFoundError(job_id)
        tags = [t.name for t in job.tags]
        job_info = dict(job.__dict__)
        job_info["tags"] = tags
        return JobPublicInfo(**job_info)

    def get_many(self, job_ids: Optional[List[int]] = None,
                 offset: Optional[int] = None,
                 limit: Optional[int] = None,
                 job_filter: JobFilter = None):
        jobs = self.db.query(Job)
        if not offset:
            offset = 0
        if not limit:
            limit = 20
        if job_ids:
            jobs = jobs.filter(Job.id.in_(job_ids))
        results = []
        if job_filter.only_open_job:
            jobs = jobs.filter(Job.is_open == True)
        if job_filter.employer_name:
            jobs = jobs.join(Job.employer).filter(Employer.name == job_filter.employer_name)
        total = jobs.count()
        jobs = jobs.offset(offset).limit(limit)
        for job in jobs:
            tags = [t.name for t in job.tags]
            job_info = dict(job.__dict__)
            job_info["tags"] = tags
            results.append(JobPublicInfo(**job_info))
        return results, total

    def update(self, job_id: int, **info):
        exclude_fields = {"tags"}
        job = self.db.query(Job).get(job_id)
        if not job:
            raise JobNotFoundError()
        if "tags" in info:
            tag_crud = CRUDTag(self.db)
            not_exist_tags = tag_crud.get_not_exist_tags(info["tags"])
            if not_exist_tags:
                tag_crud.create_many(not_exist_tags)
            tags = tag_crud.get_many(info["tags"])
            job.tags = tags.all()
        for key, value in info.items():
            if key in exclude_fields:
                continue
            if hasattr(job, key):
                setattr(job, key, value)
        self.db.add(job)

    def delete(self, job_id: int):
        job = self.db.query(Job).get(job_id)
        if not job:
            raise JobNotFoundError()
        self.db.delete(job)
