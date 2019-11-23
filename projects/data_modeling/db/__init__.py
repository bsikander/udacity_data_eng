"""Utilities for establishing SQLAlchemy connections to different databases."""
import typing as T
import logging
from importlib import import_module


import sqlalchemy as sa

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SUPPORTED_FACTORY_SCHEMES = {"postgres"}


def get_engine_factory(scheme: str) -> T.Callable:
    """Lookup the factory to use for a specific database.

    :param scheme: Type of database to get SQLAlchemy engine factory for
    """
    if scheme not in SUPPORTED_FACTORY_SCHEMES:
        raise ValueError(f"Unsupported database scheme: {scheme}")

    mod = import_module(f"db.{scheme}")
    factory_method = getattr(mod, f"{scheme}_engine_factory")
    return factory_method


def get_engine(scheme: str, connection: dict) -> sa.engine.base.Engine:
    """Get a SQLAlchemy engine connected to a specific database."""
    factory = get_engine_factory(scheme)
    return factory(**connection)


def query_executor(engine: sa.engine.base.Engine, query: str, **kwargs):
    """Execute DB queries safely."""
    conn = engine.connect()
    if len(kwargs) > 0:
        conn = conn.execution_options(**kwargs)

    try:
        logger.info(query)
        lazy_result = conn.execute(query)
        try:
            results = lazy_result.fetchall()
        except sa.exc.ResourceClosedError:
            results = None
    finally:
        conn.close()
        engine.dispose()
    return results
