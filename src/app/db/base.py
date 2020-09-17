import databases
from sqlalchemy import MetaData, create_engine
from src.app.config import settings

# sqlalchemy
engine = create_engine(settings.POSTGRES_URL)
metadata = MetaData(engine)


# databases
database = databases.Database(settings.POSTGRES_URL)
