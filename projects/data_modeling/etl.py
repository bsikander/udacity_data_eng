import os
import glob
import pandas as pd
import logging
import typing as T
import json


import sqlalchemy as sa

from config import instrument
from db import get_engine
from db.postgres import get_conn_params, copy_to_postgres


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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


def process_song_file(filename: str):
    """Loads a song file and returns a dataframe."""
    data = json.load(open(filename))
    df = pd.DataFrame.from_records([data])
    return df


def process_log_file(filename: str):
    """Loads a log file, sanitizes it, and returns a dataframe."""
    df = pd.read_json(filename, orient="records")
    # artist, auth, firstName, gender, itemInSession, lastName, length,
    # level, location, method, page, registration, sessionId, song, status,
    # ts, userAgent, userId
    pass


def get_files(path, ext: str = "json"):
    """return all files matching extension from a directory."""
    all_files = []
    for root, dirs, files in os.walk(path):
        files = glob.glob(os.path.join(root, f"*.{ext}"))
        for f in files:
            all_files.append(os.path.abspath(f))

    logger.info(f"{len(files)} files found in {path}")
    return all_files


def copy_into_table(
    table: str,
    engine: sa.engine.base.Engine,
    df: pd.DataFrame,
    cols: T.List[str] = None,
    delimiter: str = ",",
    null_string: str = "",
) -> bool:
    """Uses COPY command to load data to an existing Postgres table."""
    logger.info(f"Copying into table {table}...")
    buf = df.to_csv(
        sep=delimiter, na_rep=null_string, columns=cols, header=False, index=False
    )
    logger.info(buf)
    copy_to_postgres(engine, buf, table, validate=True, sep=delimiter, null=null_string)


def process_data(engine, filepath, load_fn):
    all_files = get_files(filepath)

    df = pd.DataFrame()
    logger.info("Reading data from json to df...")
    for idx, f in enumerate(all_files, 1):
        dfa = load_fn(f)
        df = df.append(dfa)

    artists_cols = [
        "artist_id",
        "artist_name",
        "artist_location",
        "artist_latitude",
        "artist_longitude",
    ]
    songs_cols = ["song_id", "title", "artist_id", "year", "duration"]

    copy_into_table("songs", engine=engine, df=df, cols=songs_cols)
    copy_into_table("artists", engine=engine, df=df, cols=artists_cols)


def main():
    db_name = "sparkifydb"
    conn_params = get_conn_params(database=db_name)
    engine = get_engine(conn_params["type"], conn_params)

    process_data(engine, filepath="data/song_data", load_fn=process_song_file)
    process_data(engine, filepath="data/log_data", func=process_log_file)


if not os.getenv("SKIP_INSTRUMENT"):
    instrument()

if __name__ == "__main__":
    main()
