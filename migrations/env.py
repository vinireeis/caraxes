from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool
from decouple import config

from src import Base


DATABASE_URL = config("POSTGRES_STRING_CONNECTION")

if not DATABASE_URL:
    raise ValueError("POSTGRES_STRING_CONNECTION is not set in environment variables.")

config = context.config
url = config.get_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_engine() -> AsyncEngine:
    return create_async_engine(DATABASE_URL, poolclass=pool.NullPool)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode."""

    async with get_engine().connect() as connection:

        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                transaction_per_migration=True,
            )
        )

        await connection.run_sync(lambda sync_conn: context.run_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
