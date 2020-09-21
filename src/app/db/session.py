from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.app.config import settings


engine = create_engine(settings.POSTGRES_URL)
Session = sessionmaker(bind=engine)
