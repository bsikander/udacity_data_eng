import os
import logging

import sqlalchemy as sa

from config import instrument
from db import get_engine, query_executor
from db.postgres import get_conn_params

from sql_queries import create_table_queries, drop_table_queries

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_database(engine: sa.engine.base.Engine, db_name: str = None):
    if db_name is None:
        raise ValueError("database name is not provided.")

    drop_db_query = f"DROP DATABASE IF EXISTS {db_name}"
    query_executor(engine, drop_db_query, isolation_level="AUTOCOMMIT")
    create_db_query = f"CREATE DATABASE {db_name} WITH ENCODING 'utf8'"
    query_executor(engine, create_db_query, isolation_level="AUTOCOMMIT")

    return db_name


def drop_tables(engine: sa.engine.base.Engine):
    for query in drop_table_queries:
        query_executor(engine, query)


def create_tables(engine: sa.engine.base.Engine):
    for query in create_table_queries:
        query_executor(engine, query)


def main():
    conn_params = get_conn_params()
    engine = get_engine(conn_params["type"], conn_params)

    db_name = "sparkifydb"
    create_database(engine=engine, db_name=db_name)
    conn_params = get_conn_params(database=db_name)
    engine = get_engine(conn_params["type"], conn_params)

    drop_tables(engine)
    create_tables(engine)


if not os.getenv("SKIP_INSTRUMENT"):
    instrument()

if __name__ == "__main__":
    main()
