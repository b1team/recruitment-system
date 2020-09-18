from datetime import datetime

from src.app.db.base import metadata
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import types, func

Employee = Table(
    "employees",
    metadata,
    Column("id", types.Integer, primary_key=True, index=True),
    Column("employee_job_id", types.Integer, ForeignKey("employee_jobs.id"), nullable=False, index=True),
    Column("user_id", types.Integer, ForeignKey("users.id"), nullable=False, index=True),
    Column("created_at", types.DateTime, server_default=func.now()),
    Column("updated_at", types.DateTime, server_default=func.now(), onupdate=func.now())
)
