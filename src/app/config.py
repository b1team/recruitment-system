from pydantic import BaseSettings


class Settings(BaseSettings):
    POSTGRES_URL: str

    class Config:
        env_file = "../../.env"


settings = Settings()
