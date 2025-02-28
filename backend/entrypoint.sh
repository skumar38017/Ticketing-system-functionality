#!/bin/sh

# Wait for PostgreSQL to be ready
until psql -U postgres -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

# Create role and database if they don't exist
psql -U postgres -c "DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'Neon-Stdioz-Holi-T25') THEN
        CREATE ROLE \"Neon-Stdioz-Holi-T25\" WITH LOGIN PASSWORD 'Neon-Stdioz-Holi-T25';
    END IF;
END \$\$;"

psql -U postgres -c "DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'Neon-Stdioz-Holi-T25') THEN
        CREATE DATABASE \"Neon-Stdioz-Holi-T25\" OWNER \"Neon-Stdioz-Holi-T25\";
    END IF;
END \$\$;"

# Run Alembic migrations
alembic upgrade head

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000