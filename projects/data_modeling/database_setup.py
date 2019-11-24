import sqlalchemy as sa

from db import query_executor
from sql_queries import create_table_queries, drop_table_queries


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
