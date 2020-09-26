from src.app.models import Employer, Apply, Job
from sqlalchemy.orm.session import Session
from src.app.schemas.employer import EmployerBase
from src.app.exceptions import NotFoundError


class CRUDemployer:
    def __init__(self, session):
        self.db = session
    
    def create(self, employer: EmployerBase):
        new_employer = Employer(**employer.dict())
        self.db.add(new_employer)
    
    def get_applied_job(self, employer_id: int):
        result = self.db.query(Apply, Job).join(Apply.job).filter_by(employer_id=employer_id).all()
        if not result:
            raise NotFoundError("Applied job is")
        applied_jobs_info = [
             {
                "job": {
                    "id":job.id,
                    "title":job.title,
                    "salary":job.salary,
                    "description":job.description,
                    "address":job.address,
                    "employer_id":job.employer_id,
                    "is_open":job.is_open
                },
                "apply": {
                    "status":apply.status.value,
                    "employee_id":apply.employee_id,
                    "description": apply.description,
                    "cv": apply.cv
                    }
            }
            for apply, job in result]
        return applied_jobs_info
