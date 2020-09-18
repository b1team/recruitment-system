from src.app.db.base import metadata
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import types, func

EmployeeJob = Table(
    "employee_jobs",
    metadata,
    Column("id", types.Integer, primary_key=True, index=True),
    Column("employee_id", types.Integer, ForeignKey("employees.id"), nullable=False, index=True),
    Column("job_id", types.Integer, ForeignKey("jobs.id"), nullable=False, index=True),
    Column("created_at", types.DateTime, server_default=func.now()),
    Column("updated_at", types.DateTime, server_default=func.now(), onupdate=func.now())
)
