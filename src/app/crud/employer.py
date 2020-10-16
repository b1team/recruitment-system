from src.app.models import apply
from typing import List, Optional
from sqlalchemy.orm.session import Session

from src.app.models import Employer, Apply, Job
from src.app.schemas.employer import EmployerInDB

from src.app.schemas.filters.apply import ApplyFilter
from src.app.schemas.filters.employee import EmployeeFilter
from src.app.schemas.filters.job import JobFilter

from src.app.exceptions import NotFoundError, EmployerNotFoundError


class CRUDemployer:
    def __init__(self, session: Session):
        self.db = session
    
    def create(self, employer: EmployerInDB):
        new_employer = Employer(**employer.dict())
        self.db.add(new_employer)
    
    def get_applied_job(self, employer_id: int,
                        offset: Optional[int],
                        limit: Optional[int],
                        applied: ApplyFilter,
                        employee: EmployeeFilter,
                        job: JobFilter):
        result = self.db.query(Apply, Job).join(Apply.job).filter(Job.employer_id==employer_id)
        total = result.count()
        if offset:
            result = result.offset(offset)
        if limit:
            result = result.limit(limit)
        if job.only_open_job:
            result = result.filter(Job.is_open == True)
        if applied.apply_status:
            result = result.filter(Apply.status.in_(applied.apply_status))
        if employee.employee_id:
            result = result.filter(Apply.employee_id == employee.employee_id)

        job_applied_mapping = dict()
        for apply, job in result:
            if job.id not in job_applied_mapping:
                job_applied_mapping[job.id]={
                    "job": {
                        "id":job.id,
                        "title":job.title,
                        "salary":job.salary,
                        "description":job.description,
                        "address":job.address,
                        "employer_id":job.employer_id,
                        "tags": [t.name for t in job.tags],
                        "is_open":job.is_open
                    },
                    "applies": [{
                        "id": apply.id,
                        "status":apply.status.value,
                        "employee_id":apply.employee_id,
                        "description": apply.description,
                        "cv": apply.cv
                    }]
                }
            else:
                job_applied_mapping[job.id]['applies'].append({
                    "id": apply.id,
                    "status":apply.status.value,
                    "employee_id":apply.employee_id,
                    "description": apply.description,
                    "cv": apply.cv
                })
       
        return list(job_applied_mapping.values()), total

    def update(self, employer_id: int, **employer_info):
        employer = self.db.query(Employer).get(employer_id)
        if not employer:
            raise EmployerNotFoundError(employer_id)
        for key, value in employer_info.items():
            if hasattr(employer, key):
                setattr(employer, key, value)
        self.db.add(employer)

    def update_apply_status(self, apply_id: int, status: str):

        result = self.db.query(Apply).get(apply_id)
        if not result:
            raise NotFoundError('Applied job')
        result.status = status
        self.db.add(result)

        



