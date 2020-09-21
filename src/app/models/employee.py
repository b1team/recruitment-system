from src.app.models.base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import relationship, backref


class Employee(Base):
    __tablename__ = "employees"
    user_id = Column(types.Integer, ForeignKey("users.id"), nullable=False)
    applies = relationship("Apply", backref="employee")
    user = relationship("User", backref=backref("employee", uselist=False))
