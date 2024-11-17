from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool

from src.domain.models.orm_base.model import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
url = config.get_main_option("sqlalchemy.url")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# create async engine


def get_engine() -> AsyncEngine:
    return create_async_engine(url, poolclass=pool.NullPool)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    context.configure(
        url=url,
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
                connection=sync_conn, target_metadata=target_metadata, transaction_per_migration=True
            )
        )
        async with connection.begin():
            await connection.run_sync(context.run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
