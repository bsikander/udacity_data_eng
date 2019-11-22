"""Utilities for interacting purely with Postgres."""
import sqlalchemy as sa


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
