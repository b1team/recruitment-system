from src.app.models.base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import relationship


class JobTag(Base):
    __tablename__ = "job_tags"
    job_id = Column(types.Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    tag_id = Column(types.Integer, ForeignKey("tags.id"), nullable=False, index=True)
