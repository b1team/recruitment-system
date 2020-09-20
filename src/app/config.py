from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: str
    TOKEN_SECRET_KEY: str

    class Config:
        env_file = "../../.env"


settings = Settings()
