from sql_queries import create_table_queries, drop_table_queries

from db import get_engine, query_executor
import sqlalchemy as sa


def get_conn_params(database: str = "studentdb", user: str = "student", password: str = "student"):
    """Build params dict for a database connection."""
    return {
        "type": "postgres",
        "host": "data_modeling_postgres_1",
        "port": 5432,
        "user": user,
        "password": password,
        "database": database,
    }


def create_database(engine: sa.engine.base.Engine, db_name: str = None):
    if db_name is None:
        raise ValueError("database name is not provided.")

    # create sparkify database with UTF8 encoding
    query_executor(engine, "DROP DATABASE IF EXISTS sparkifydb")
    query_executor(
        engine, "CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0"
    )

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


if __name__ == "__main__":
    main()
