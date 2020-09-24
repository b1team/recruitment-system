from src.app.models.employer import Employer
from sqlalchemy.orm.session import Session
from src.app.schemas.employer import EmployerBase


class CRUDemployer:
    def __init__(self, session):
        self.db = session
    
    def create(self, employer: EmployerBase):
        new_employer = Employer(**employer.dict())
        self.db.add(new_employer)
