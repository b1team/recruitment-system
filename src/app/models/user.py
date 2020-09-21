from src.app.models.base import Base
from sqlalchemy import Column
from sqlalchemy import types
from src.app.db import constants


class User(Base):
    __tablename__ = "users"
    email = Column(types.String(constants.MAXIMUM_EMAIL_LENGTH), nullable=False, unique=True),
    password = Column(types.Text, nullable=False),
    user_type = Column(types.String, nullable=False, default=constants.DEFAULT_USER_TYPE)
    name = Column(types.Text)
    phone_number = Column(types.String(constants.MAXIMUM_PHONE_NUMBER_LENGTH))
