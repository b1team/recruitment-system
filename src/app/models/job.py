from src.app.db.base import metadata
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import types, func

Job = Table(
    "jobs",
    metadata,
    Column("job_id", types.Integer, primary_key=True, index=True),
    Column("employee_job_id", types.Integer, ForeignKey("employee_jobs.employee_job_id"), nullable=False, index=True),
    Column("job_skill_id", types.Integer, ForeignKey("job_skills.job_skill_id"), nullable=False, index=True),
    Column("title", types.Text, nullable=False),
    Column("salary", types.Float, nullable=False),
    Column("address", types.Text, nullable=False),
    Column("descriptions", types.Text, nullable=False),
    Column("created_at", types.DateTime, server_default=func.now()),
    Column("updated_at", types.DateTime, server_default=func.now(), onupdate=func.now())
)
