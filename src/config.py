import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path

load_dotenv()


class FastAPIPYTestBase(BaseSettings):
    PROJECT_NAME: str = "FastAPI PYTesBase"
    BASE_DIR: str = str(Path().absolute())


class FastAPIPYTestDB(FastAPIPYTestBase):
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: int = os.environ.get("POSTGRES_PORT")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DRIVER: str = "postgresql+asyncpg"
    @property
    def get_db_uri(self) -> str:
        return f"{self.POSTGRES_DRIVER}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:" \
               f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class FastAPIPYTestSettings(FastAPIPYTestDB):
    DEBUG: bool = True
    postgres: FastAPIPYTestDB = FastAPIPYTestDB()


def get_settings(db_only=False):
    if not db_only:
        return FastAPIPYTestSettings()
    else:
        return FastAPIPYTestDB()

