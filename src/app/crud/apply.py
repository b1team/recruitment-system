from src.app.models.apply import Apply
from src.app.schemas.apply import ApplyInDB

from sqlalchemy.orm.session import Session
from src.app.exceptions import *


class CRUDApply:
    def __init__(self, session: Session):
        self.db = session

    def create(self, apply: ApplyInDB):
        new_apply = Apply(**apply.dict())
        self.db.add(new_apply)

    def update(self, apply_id: str, **info):
        exclude_fields = {"jobs"}
        apply = self.db.query(Apply).get(apply_id)
        if not apply:
            raise ApplyNotFoundError(apply_id)
        for key, value in info.items():
            if key in exclude_fields:
                continue
            if hasattr(apply, key):
                setattr(apply, key, value)
        self.db.add(apply)

    def delete(self, apply_id: str):
        apply = self.db.query(Apply).get(apply_id)
        if not apply:
            raise ApplyNotFoundError(apply_id)

        self.db.delete(apply)
