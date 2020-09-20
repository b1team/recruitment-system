from databases import Database
from src.app import models
from src.app.schemas import login as login_schemas


class LoginHandler:
    def __init__(self, database: Database):
        self.database = database

    def check_user(self, user: login_schemas.LoginRequestBody):
        # TODO check user
        return True
