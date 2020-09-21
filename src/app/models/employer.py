from src.app.models.base import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import types
from sqlalchemy.orm import relationship
from src.app.db import constants


class Employer(Base):
    __tablename__ = "employers"
    user_id = Column(types.Integer, ForeignKey("users.id"), nullable=False, index=True)
    user = relationship("User", backref="employer")
    name = Column(types.Text, nullable=False, index=True, unique=True)
    code = Column(types.Text, nullable=False, unique=True, index=True)
    description = Column(types.Text)
    address = Column(types.Text, nullable=False)
    type = Column(types.Text, default=constants.DEFAULT_EMPLOYER_TYPE),
    active = Column(types.Boolean, nullable=False, default=True)

