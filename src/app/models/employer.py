from src.app.db.base import metadata
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import types, func
from src.app.db import constants

Employer = Table(
    "employers",
    metadata,
    Column("id", types.Integer, primary_key=True, index=True),
    Column("user_id", types.Integer, ForeignKey("users.id"), nullable=False, index=True),
    Column("code", types.String, nullable=False, unique=True, index=True),
    Column("name", types.Text, nullable=False),
    Column("description", types.Text),
    Column("address", types.Text, nullable=False),
    Column("type", types.Text, default=constants.DEFAULT_EMPLOYER_TYPE),
    Column("size", types.Integer, nullable=False),
    Column("active", types.Boolean, nullable=False, default=True),
    Column("created_at", types.DateTime, server_default=func.now()),
    Column("updated_at", types.DateTime, server_default=func.now(), onupdate=func.now())
)
