"""Utilities for interacting purely with Postgres."""
import sqlalchemy as sa
import logging

from io import StringIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_conn_params(
    database: str = "studentdb", user: str = "student", password: str = "student",
) -> dict:
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
) -> sa.engine.base.Engine:
    """Get a SQLAlchemy engine for a Postgres connection."""
    engine = sa.create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )

    return engine


def copy_to_postgres(
    engine: sa.engine.base.Engine,
    data: str,
    table: str,
    validate: bool = False,
    **kwargs,
):
    """Execute COPY FROM query in Postgres safely."""
    conn = engine.raw_connection()
    cur = conn.cursor()

    try:
        results = cur.copy_from(StringIO(data), table, **kwargs)
        if validate:
            cur.execute(f"SELECT count(*) from {table}")
            select_results = cur.fetchall()
            logger.info(select_results)
    finally:
        conn.close()
        engine.dispose()

    return results
