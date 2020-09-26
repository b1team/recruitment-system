from sqlalchemy.orm.session import Session

from src.app.models import Employee, Apply, Job
from src.app.schemas.employee import EmployeeBase
from src.app.exceptions import NotFoundError


class CRUDemployee:
    def __init__(self, session):
        self.db = session
    
    def create(self, employee: EmployeeBase):
        new_employee = Employee(**employee.dict())
        self.db.add(new_employee)

    def get_applied_job(self, employee_id: int):
        result = self.db.query(Job, Apply).join(Job.applies).filter_by(employee_id=employee_id).all()
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
                    "employee_id":apply.employee_id
                    }
            }
            for job, apply in result]
        return applied_jobs_info