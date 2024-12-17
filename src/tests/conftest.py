import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.data_base.db_connect import get_db
from src.main import app
from src.data_base.session_manager import Base
from src.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from src.tests import defaults
from sqlalchemy.sql import text


settings = get_settings(db_only=True)


async_engine_main = create_async_engine(
    settings.get_db_uri,
    poolclass=NullPool,
)

async_engine_test = create_async_engine(defaults.TEST_DB_URI)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def engine():
    async with async_engine_main.connect() as connection:
        await connection.execute(text("COMMIT;"))
        await connection.execute(text(f"CREATE DATABASE {defaults.TEST_DB_NAME};"))
    async with async_engine_test.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield async_engine_test
    await async_engine_test.dispose()
    async with async_engine_main.connect() as connection:
        await connection.execute(text("COMMIT;"))
        await connection.execute(text(f"DROP DATABASE {defaults.TEST_DB_NAME};"))


@pytest.fixture(scope="session")
def async_session_class(engine: AsyncEngine) -> sessionmaker[AsyncSession]:
    return sessionmaker(  # type: ignore[call-arg]
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest.fixture(scope="session")
def test_app(async_session_class: sessionmaker[AsyncSession]):
    async def get_test_session():
        async with async_session_class() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_session
    return app


@pytest.fixture(scope="function", autouse=True)
async def session(
    async_session_class: sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with async_session_class() as session:
        yield session
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f"TRUNCATE {table.name} CASCADE;"))
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_client(test_app) -> AsyncClient:
    async with AsyncClient(base_url=defaults.HOST_URL) as client:
        yield client