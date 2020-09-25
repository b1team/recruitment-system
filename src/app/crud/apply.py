from src.app.models.apply import Apply
from src.app.schemas.apply import ApplyInDB

from sqlalchemy.orm.session import Session


class CRUDapply:
    def __init__(self, session):
        self.db = session

    def create(self, apply: ApplyInDB):
        new_apply = Apply(**apply.dict())
        self.db.add(new_apply)
