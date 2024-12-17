from src.config import get_settings
from sqlalchemy import URL


def get_test_db_uri():
    settings = get_settings(db_only=True)
    sql_test_uri = URL.create(
        drivername=settings.POSTGRES_DRIVER,
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=TEST_DB_NAME
    )
    return sql_test_uri


TEST_DB_NAME: str = "fastapi_pytest_async_tests"
TEST_DB_URI = get_test_db_uri()
HOST_URL: str = "http://127.0.0.1:8000/"
