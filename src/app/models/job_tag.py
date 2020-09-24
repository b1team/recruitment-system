from src.app.models.base import Base
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy import types

JobTag = Table('job_tags', Base.metadata,
               Column('job_id', types.Integer, ForeignKey('jobs.id')),
               Column('tag_id', types.Integer, ForeignKey('tags.id'))
               )
