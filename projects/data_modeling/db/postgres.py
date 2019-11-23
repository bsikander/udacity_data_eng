"""Utilities for interacting purely with Postgres."""
import sqlalchemy as sa


def get_conn_params(
    database: str = "studentdb", user: str = "student", password: str = "student",
):
    """Build params dict for a database connection."""
    return {
        "type": "postgres",
        "host": "127.0.0.1",
        "port": 5432,
        "user": user,
        "password": password,
        "database": database,
    }


def postgres_engine_factory(
    user: str,
    password: str,
    database: str,
    host: str = "localhost",
    port: int = 5432,
    **kwargs,
):
    """Get a SQLAlchemy engine for a Postgres connection."""
    engine = sa.create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    return engine
