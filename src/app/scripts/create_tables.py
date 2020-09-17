from src.app.db.base import metadata
from src.app.models import *

if __name__ == '__main__':
    metadata.create_all()
