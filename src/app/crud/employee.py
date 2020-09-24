from src.app.models.employee import Employee
from sqlalchemy.orm.session import Session
from src.app.schemas.employee import EmployeeBase


class CRUDemployee:
    def __init__(self, session):
        self.db = session
    
    def create(self, employee: EmployeeBase):
        new_employee = Employee(**employee.dict())
        self.db.add(new_employee)
