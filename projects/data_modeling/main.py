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


def main():
    """Runs through the main process."""
    conn_params = get_conn_params()
    engine = get_engine(conn_params["type"], conn_params)

    db_name = "sparkifydb"
    create_database(engine=engine, db_name=db_name)
    conn_params = get_conn_params(database=db_name)
    engine = get_engine(conn_params["type"], conn_params)

    drop_tables(engine)
    create_tables(engine)

    process_song_data(engine, filepath="data/song_data")
    process_log_data(engine, filepath="data/log_data")


if __name__ == "__main__":
    main()