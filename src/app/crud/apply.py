from src.app.models.apply import Apply
from src.app.schemas.apply import ApplyBase

from sqlalchemy.orm.session import Session


class CRUDemployee:
    def __init__(self, session):
        self.db = session
