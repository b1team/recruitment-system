from src.app.models.base import Base
from src.app.db.session import engine

Base.metadata.create_all(engine)
