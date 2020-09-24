import datetime

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column
from sqlalchemy import func, types

# sqlalchemy
BaseRoot = declarative_base()


class Base(BaseRoot):
    __abstract__ = True
    # @declared_attr
    # def __tablename__(cls):
    #     return cls.__name__.lower()

    id = Column(types.Integer, primary_key=True, index=True)
    created_at = Column(types.DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(types.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
