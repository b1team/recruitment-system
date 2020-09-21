from src.app.models.base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"
    title = Column(types.Text, nullable=False)
    salary = Column(types.Float, nullable=False)
    address = Column(types.Text, nullable=False)
    description = Column(types.Text, nullable=False)
    job_tags = relationship("JobTag", backref="job")
    applies = relationship("Apply", backref="job")
