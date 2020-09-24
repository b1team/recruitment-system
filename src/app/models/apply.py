from src.app.models.base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import relationship
from src.app.db.constants import ApplyStatus


class Apply(Base):
    __tablename__ = "applies"
    employee_id = Column(types.Integer, ForeignKey("employees.id"), nullable=False)
    job_id = Column(types.Integer, ForeignKey("jobs.id"), nullable=False)
    description = Column(types.Text, nullable=True)
    cv = Column(types.Text, nullable=False)
    status = Column(types.Enum(ApplyStatus), nullable=False, default=ApplyStatus.pending)
