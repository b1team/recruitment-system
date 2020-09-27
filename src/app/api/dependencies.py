from typing import Optional, List
from src.app.schemas.filters.apply import ApplyFilter
from src.app.schemas.filters.employee import EmployeeFilter
from src.app.schemas.filters.job import JobFilter


def apply_filter(apply_status: Optional[List[str]] = None):
    return ApplyFilter(apply_status=apply_status)


def employee_filter(employee_id: Optional[int] = None):
    return EmployeeFilter(employee_id=employee_id)


def job_filter(only_open_job: Optional[bool] = None):
    return JobFilter(only_open_job=only_open_job)