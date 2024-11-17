from typing import AsyncGenerator

from decouple import config
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.domain.exceptions.infrastructure.exception import (
    SqlAlchemyInfrastructureException,
    UnexpectedInfrastructureException,
)


class PostgresInfrastructure:
    async_engine = create_async_engine(
        config("POSTGRES_URL"),
        echo=True,
        poolclass=AsyncAdaptedQueuePool,
        pool_pre_ping=True,
    )
    async_session = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    @classmethod
    async def get_session(cls) -> AsyncGenerator[AsyncSession, None]:
        try:
            async with cls.async_session() as session:
                yield session
        except SQLAlchemyError as ex:
            raise SqlAlchemyInfrastructureException(original_ex=ex)
        except Exception as ex:
            raise UnexpectedInfrastructureException(original_ex=ex)
