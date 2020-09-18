from src.app.db.base import metadata
from sqlalchemy import Table, Column
from sqlalchemy import types, func
from src.app.db import constants

User = Table(
    "users",
    metadata,
    Column("id", types.Integer, primary_key=True),
    Column("email", types.String(constants.MAXIMUM_EMAIL_LENGTH), nullable=False, unique=True),
    Column("password", types.Text, nullable=False),
    Column("token", types.Text, nullable=False),
    Column("name", types.Text),
    Column("phone_number", types.String(constants.MAXIMUM_PHONE_NUMBER_LENGTH)),
    Column("created_at", types.DateTime, server_default=func.now()),
    Column("updated_at", types.DateTime, server_default=func.now(), onupdate=func.now())
)
