from contextlib import asynccontextmanager
from typing import AsyncGenerator


from decouple import config
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class PostgresInfrastructure:
    async_engine = create_async_engine(
        config("POSTGRES_STRING_CONNECTION"),
        echo=True,
        poolclass=AsyncAdaptedQueuePool,
        pool_pre_ping=True,
    )
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    @classmethod
    @asynccontextmanager
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        async with cls.async_session() as session:
            yield session
