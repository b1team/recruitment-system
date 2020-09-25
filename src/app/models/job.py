from src.app.models.base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import relationship
from src.app.models.job_tag import JobTag


class Job(Base):
    __tablename__ = "jobs"
    title = Column(types.Text, nullable=False)
    salary = Column(types.Float, nullable=False)
    address = Column(types.Text, nullable=False)
    description = Column(types.Text, nullable=False)
    is_open = Column(types.Boolean, nullable=False, default=True)
    tags = relationship("Tag", secondary=JobTag)
    applies = relationship("Apply", backref="job")
    employer_id = Column(types.Integer, ForeignKey("employers.id"), nullable=False)
