from src.app.db.base import metadata
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import types, func

JobSkill = Table(
    "job_skills",
    metadata,
    Column("id", types.Integer, primary_key=True, index=True),
    Column("skill_id", types.Integer, ForeignKey("skills.id"), nullable=False, index=True),
    Column("job_id", types.Integer, ForeignKey("jobs.id"), nullable=False, index=True),
    Column("created_at", types.DateTime, server_default=func.now()),
    Column("updated_at", types.DateTime, server_default=func.now(), onupdate=func.now())
)
