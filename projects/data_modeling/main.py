import sys
import os
from config import instrument

import logging

from db import get_engine, query_executor
from db.postgres import get_conn_params

from etl import process_song_data, process_log_data
from database_setup import create_database, create_tables, drop_tables

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not os.getenv("SKIP_INSTRUMENT"):
    instrument()


def _get_engine(
    database: str = "studentdb", user: str = "student", password: str = "student"
):
    conn_params = get_conn_params(database=database, user=user, password=password)
    return get_engine(conn_params["type"], conn_params)


def test(engine):
    logger.info("Running basic set of tests...")

    default_limit = 5

    def select_query(table: str, limit: int = default_limit):
        return f"SELECT * from {table} LIMIT {limit}"

    tables = ["songs", "artists", "users", "time"]

    for q in map(select_query, tables):
        results = query_executor(engine, q)
        assert len(results) == default_limit

        for res in results:
            logger.info(res)


def main(run_test: bool = False, refresh_database: bool = False):
    """Runs through the main process."""
    if refresh_database:
        engine = _get_engine()
        create_database(engine=engine, db_name="sparkifydb")

    engine = _get_engine(database="sparkifydb")
    drop_tables(engine)
    create_tables(engine)

    engine = _get_engine(database="sparkifydb")

    process_song_data(engine, filepath="data/song_data")
    process_log_data(engine, filepath="data/log_data")

    if run_test:
        test(engine)


if __name__ == "__main__":
    args = sys.argv[1:]
    run_test = "--run-test" in args
    refresh_database = "--refresh" in args
    if run_test:
        logger.info(f"running with test...")
    if refresh_database:
        logger.info(f"running with a fresh database")

    main(run_test=run_test, refresh_database=refresh_database)
