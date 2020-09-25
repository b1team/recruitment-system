from src.app.models.tag import Tag
from sqlalchemy.orm.session import Session

from typing import List

class CRUDTag:
    def __init__(self, session):
        self.db = session
    
    def get_many(self, tags: List[str]):
        return self.db.query(Tag).filter(Tag.name.in_(tags))

    def create_many(self, tags: List[str]):
        for tag in tags:
            new_tag = Tag(name=tag)
            self.db.add(new_tag)
    
    def get_not_exist_tags(self, tags: List[str]):
        existing_tags = [result.name for result in self.db.query(Tag.name)
                         .filter(Tag.name.in_(tags))]
        return list(set(tags) - set(existing_tags))
        
