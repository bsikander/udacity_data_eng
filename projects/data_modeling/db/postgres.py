"""Utilities for interacting purely with Postgres."""
import typing as T
import logging

import sqlalchemy as sa
from io import StringIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_conn_params(database: str, user: str = "", password: str = "",) -> dict:
    """Build params dict for a database connection."""
    if database is None:
        raise ValueError("database is not provided.")

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
    columns: T.List[str] = None,
    sep: str = "\t",
    null_string: str = "",
    size: int = 8192,
    validate: bool = False,
    verbose: bool = False,
):
    """Execute COPY FROM query in Postgres safely."""
    conn = engine.raw_connection()
    cur = conn.cursor()

    logger.info(f"Copying into table {table}...")
    if verbose:
        logger.info(data)

    try:
        results = cur.copy_from(
            StringIO(data), table, sep=sep, null=null_string, size=size, columns=columns
        )
        if validate:
            query = f"SELECT count(*) from {table}"
            logger.info(query)
            cur.execute(query)
            select_results = cur.fetchall()
            logger.info(f"{select_results[0][0]} rows uploaded to {table}")
        conn.commit()
    finally:
        conn.close()
        engine.dispose()

    return results
