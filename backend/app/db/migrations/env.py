import alembic
import logging
import os

from logging.config import fileConfig
from psycopg2 import DatabaseError
from sqlalchemy import engine_from_config, pool

# Load the database schemas so that Alembic knows what it needs to create/update
from db import schemas
from db.database import Base

# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in "online" mode
    """

    # Handle database configuration for running tests
    database_url = os.environ["DATABASE_URL"]
    if "TESTING" in os.environ and os.environ["TESTING"]:
        database_url = f"{database_url}_test"

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", database_url)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(connection=connection, target_metadata=Base.metadata)

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in "offline" mode.
    """

    if "TESTING" in os.environ and os.environ["TESTING"]:
        raise DatabaseError("Running testing migrations offline is not permitted.")

    alembic.context.configure(url=os.environ["DATABASE_URL"])

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
