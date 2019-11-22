"""Utilities for establishing SQLAlchemy connections to different databases."""
import typing as T
import warnings
from importlib import import_module

import sqlalchemy as sa

from sqlalchemy import text

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
    """Get a SQLAlchemy engine connected to a specific database.

    :param scheme: Type of database to get SQLAlchemy engine for
    :param connection: dict of parameters to pass to SQLAlchemy engine
        constructor to establish database connection
    """
    factory = get_engine_factory(scheme)
    return factory(**connection)


def query_executor(engine: sa.engine.base.Engine, query: str, **execution_options):
    """Execute DB queries safely."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="cffi")

        connection = engine.connect()

    query = text(query)
    if len(execution_options) > 0:
        query = query.execution_options(**execution_options)

    try:
        lazy_result = connection.execute(query)
        try:
            results = lazy_result.fetchall()
        except sa.exc.ResourceClosedError:
            # some statements don't return rows
            results = None
    finally:
        connection.close()
        engine.dispose()
    return results