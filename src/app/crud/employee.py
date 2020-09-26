from sqlalchemy.orm.session import Session

from src.app.models import Employee, Apply, Job
from src.app.schemas.employee import EmployeeBase
from src.app.exceptions import NotFoundError
from src.app.schemas.filters.apply import ApplyFilter


class CRUDemployee:
    def __init__(self, session: Session):
        self.db = session
    
    def create(self, user_id: int):
        new_employee = Employee(user_id=user_id)
        self.db.add(new_employee)

    def get_applied_job(self, employee_id: int, applied: ApplyFilter):
        result = self.db.query(Job, Apply).join(Job.applies).filter_by(employee_id=employee_id)
        if applied.apply_status:
            result = result.filter(Apply.status.in_(applied.apply_status))
        if not result.first():
            raise NotFoundError("Applied")
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
            for job, apply in result.all()]
        return applied_jobs_info
