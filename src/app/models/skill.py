from src.app.db.base import metadata
from sqlalchemy import Table, Column
from sqlalchemy import types, func

Skill = Table(
    "skills",
    metadata,
    Column("id", types.Integer, primary_key=True, index=True),
    Column("name", types.Text, nullable=False, unique=True, index=True),
    Column("description", types.Text),
    Column("created_at", types.DateTime, server_default=func.now()),
    Column("updated_at", types.DateTime, server_default=func.now(), onupdate=func.now())
)
