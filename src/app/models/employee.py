from src.app.models.base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import relationship, backref


class Employee(Base):
    __tablename__ = "employees"
    applies = relationship("Apply", backref="employee")
    user_id = Column(types.Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="employee")
