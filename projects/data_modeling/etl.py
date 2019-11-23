import os
import glob
import psycopg2
import pandas as pd
import logging

import sqlalchemy as sa

from config import instrument
from db import get_engine, query_executor
from db.postgres import get_conn_params

from sql_queries import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def process_song_file(engine, filepath):
    # open song file
    df = pd.read_json(filepath)
    import ipdb

    ipdb.set_trace()

    # insert song record
    # song_data =
    # cur.execute(song_table_insert, song_data)
    #
    # # insert artist record
    # artist_data =
    # cur.execute(artist_table_insert, artist_data)


# def process_log_file(engine, filepath):
#     # open log file
#     df =
#
#     # filter by NextSong action
#     df =
#
#     # convert timestamp column to datetime
#     t =
#
#     # insert time data records
#     time_data =
#     column_labels =
#     time_df =
#
#     for i, row in time_df.iterrows():
#         cur.execute(time_table_insert, list(row))
#
#     # load user table
#     user_df =
#
#     # insert user records
#     for i, row in user_df.iterrows():
#         cur.execute(user_table_insert, row)
#
#     # insert songplay records
#     for index, row in df.iterrows():
#
#         # get songid and artistid from song and artist tables
#         results = cur.execute(song_select, (row.song, row.artist, row.length))
#         songid, artistid = results if results else None, None
#
#         # insert songplay record
#         songplay_data =
#         cur.execute(songplay_table_insert, songplay_data)


def process_data(engine, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    logger.info(f"{num_files} files found in {filepath}")

    for idx, datafile in enumerate(all_files, 1):
        func(engine, datafile)
        logger.info(f"{idx}/{num_files} files processed.")


def main():
    db_name = "sparkifydb"
    conn_params = get_conn_params(database=db_name)
    engine = get_engine(conn_params["type"], conn_params)

    process_data(engine, filepath="data/song_data", func=process_song_file)
    # process_data(engine, filepath='data/log_data', func=process_log_file)


if not os.getenv("SKIP_INSTRUMENT"):
    instrument()

if __name__ == "__main__":
    main()
