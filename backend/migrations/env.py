from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool, text
from alembic import context
from app.config import config
from app.database.base import Base  
from app.database import models  # Import models for Alembic detection
from app.utils.common_icons import event_icons  
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Alembic config object
alembic_config = context.config

# Apply logging configuration
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Set the target metadata for 'autogenerate' support
target_metadata = Base.metadata

# Set database URL dynamically from the config
alembic_config.set_main_option("sqlalchemy.url", config.async_database_url)

async def list_existing_roles_and_databases(connection):
    """Log existing roles, databases, and schemas."""
    try:
        # List all roles
        result = await connection.execute(text("SELECT rolname FROM pg_roles"))
        roles = result.fetchall()
        logger.info(f"event_icons['role'] Existing Roles: {[row[0] for row in roles]}")

        # List all databases
        result = await connection.execute(text("SELECT datname FROM pg_database"))
        databases = result.fetchall()
        logger.info(f"event_icons['Existing'] Existing Databases: {[row[0] for row in databases]}")

        # List all schemas
        result = await connection.execute(text("SELECT schema_name FROM information_schema.schemata"))
        schemas = result.fetchall()
        logger.info(f"event_icons['Existing'] Existing Schemas: {[row[0] for row in schemas]}")

    except Exception as e:
        logger.error(f"event_icons['error'] Error listing roles/databases/schemas: {e}")
        raise

async def ensure_role_and_database_exist(connection):
    """
    Ensure the role and database exist before running migrations.
    """
    role_name = config.database["role"]
    db_name = config.database["db_name"]
    db_password = config.database["password"]

    try:
        # Log existing roles, databases, and schemas
        await list_existing_roles_and_databases(connection)

        # Check if the role exists
        result = await connection.execute(text(f"SELECT 1 FROM pg_roles WHERE rolname = '{role_name}'"))
        role_exists = result.scalar() is not None

        if not role_exists:
            logger.info(f"{event_icons['update']} Creating role '{role_name}'...")
            await connection.execute(text(f"CREATE ROLE \"{role_name}\" WITH LOGIN PASSWORD '{db_password}'"))
            logger.info(f"{event_icons['check_mark']} Role '{role_name}' created successfully.")
        else:
            logger.info(f"{event_icons['check_mark']} Role '{role_name}' already exists.")

        # Check if the database exists
        result = await connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
        db_exists = result.scalar() is not None

        if not db_exists:
            logger.info(f"{event_icons['update']} Creating database '{db_name}'...")
            await connection.execute(text(f"CREATE DATABASE \"{db_name}\" OWNER \"{role_name}\""))
            logger.info(f"{event_icons['check_mark']} Database '{db_name}' created successfully.")
        else:
            logger.info(f"{event_icons['check_mark']} Database '{db_name}' already exists.")

    except Exception as e:
        logger.error(f"{event_icons['error']} Error ensuring role/database: {e}")
        raise  # Re-raise to prevent further execution

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    try:
        url = alembic_config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

        with context.connect() as connection:
            logger.info(f"{event_icons['refresh']} Running migrations in offline mode...")
            context.run_migrations()
            logger.info(f"{event_icons['check_mark']} Offline migrations completed successfully.")
    
    except Exception as e:
        logger.error(f"{event_icons['error']} Error running offline migrations: {e}")
        raise  # Exit the process

async def ensure_public_schema_exists(connection):
    """Check if the 'public' schema exists and create it if not."""
    try:
        result = await connection.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'public'"))
        schema_exists = result.scalar() is not None

        if not schema_exists:
            logger.info(f"{event_icons['update']} Creating 'public' schema...")
            await connection.execute(text("CREATE SCHEMA public"))
            await connection.execute(text("GRANT ALL ON SCHEMA public TO postgres"))
            await connection.execute(text("GRANT ALL ON SCHEMA public TO public"))
            logger.info(f"{event_icons['check_mark']} 'public' schema created successfully.")
        else:
            logger.info(f"{event_icons['check_mark']} 'public' schema already exists.")

    except Exception as e:
        logger.error(f"{event_icons['error']} Error ensuring public schema: {e}")
        raise

async def do_run_migrations(connection):
    """Ensure schema exists and run migrations."""
    try:
        # Ensure role and database exist
        await ensure_role_and_database_exist(connection)

        # Ensure the 'public' schema exists
        await ensure_public_schema_exists(connection)

        # Configure the context for Alembic migrations
        await connection.run_sync(lambda conn: context.configure(
            connection=conn,  # Pass the synchronous connection here
            target_metadata=target_metadata,
            version_table="alembic_version",
            version_table_schema="public",
        ))

        # Run migrations
        logger.info(f"{event_icons['update']} Running migrations...")
        await connection.run_sync(lambda conn: context.run_migrations())

        logger.info(f"{event_icons['check_mark']} Migration completed successfully.")

    except Exception as e:
        logger.error(f"{event_icons['error']} Migration error: {e}")
        raise

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    try:
        connectable = create_async_engine(
            alembic_config.get_main_option("sqlalchemy.url"),
            future=True,
            poolclass=pool.NullPool,
        )

        async with connectable.connect() as connection:
            # Directly await the migration function instead of using asyncio.run()
            await do_run_migrations(connection)

        logger.info(f"{event_icons['check_mark']} Online migrations completed successfully.")

    except Exception as e:
        logger.error(f"{event_icons['error']} Error running migrations online: {e}")
        raise

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())