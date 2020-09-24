from src.app.models.base import Base
from sqlalchemy import Column
from sqlalchemy import types
from sqlalchemy.orm import relationship
from src.app.models.job_tag import job_tags


class Tag(Base):
    __tablename__ = "tags"
    name = Column(types.Text, nullable=False, index=True, unique=True)
    description = Column(types.Text)
    job_tags = relationship("JobTag", secondary=job_tags)
