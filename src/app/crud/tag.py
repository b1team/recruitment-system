from src.app.models.tag import Tag
from sqlalchemy.orm.session import Session
from src.app.schemas.tag import TagBase, PayloadTag

from typing import List

class CRUDTag:
    def __init__(self, session):
        self.db = session
    
    def get(self, payload: PayloadTag):
        tag = self.db.query(Tag).filter(Tag.name.in_(payload.tags))
        return tag

    def create(self, tags: List[str]):
        for tag in tags:
            new_tag = Tag(name=tag)
            self.db.add(new_tag)
    
    def filter(self, payload: PayloadTag):
        existing_tags = [result.name for result in self.db.query(Tag.name)
                         .filter(Tag.name.in_(payload.tags))]
        usable_tag = list(set(payload.tags) - set(existing_tags))
        return usable_tag
