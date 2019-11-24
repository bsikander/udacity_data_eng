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


def get_files(path, ext: str = "json"):
    """return all files matching extension from a directory."""
    all_files = []
    for root, dirs, files in os.walk(path):
        files = glob.glob(os.path.join(root, f"*.{ext}"))
        for f in files:
            all_files.append(os.path.abspath(f))

    logger.info(f"{len(files)} files found in {path}")
    return all_files


def clean_cols(df):
    """Normalize column names of a dataframe."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    return df


def process_song_file(filename: str):
    """Loads a song file and returns a dataframe."""
    data = json.load(open(filename))
    df = pd.DataFrame.from_records([data])
    df = clean_cols(df)
    return df


def process_log_file(filename: str):
    """Loads a log file, sanitizes it, and returns a dataframe."""
    df = pd.read_json(filename, orient="records")
    # artist, auth, firstName, gender, itemInSession, lastName, length,
    # level, location, method, page, registration, sessionId, song, status,
    # ts, userAgent, userId

    df = clean_cols(df)

    # df.rename(columns={"A": "a", "B": "c"})

    # filter by NextSong action

    # convert timestamp column to datetime

    # insert time data

    # insert user records

    # insert songplay records
    return df


def copy_into_table(
    table: str,
    engine: sa.engine.base.Engine,
    df: pd.DataFrame,
    cols: T.List[str] = None,
    delimiter: str = "\t",
    null_string: str = "",
) -> bool:
    """Uses COPY command to load data to an existing Postgres table."""
    buf = df.to_csv(
        sep=delimiter, na_rep=null_string, columns=cols, header=False, index=False
    )
    copy_to_postgres(
        engine,
        buf,
        table,
        sep=delimiter,
        null_string=null_string,
        columns=cols,
        validate=True,
    )


def process_data(engine, filepath, load_fn):
    all_files = get_files(filepath)

    df = pd.DataFrame()
    logger.info("Reading data from json to df...")
    for idx, f in enumerate(all_files, 1):
        dfa = load_fn(f)
        df = df.append(dfa)

    artists_cols = [
        "artist_id",
        "name",
        "location",
        "latitude",
        "longitute",
    ]
    dfa = df.rename(
        columns={
            "artist_name": "name",
            "artist_location": "location",
            "artist_latitude": "latitude",
            "artist_longitude": "longitute",
        }
    )[artists_cols]
    copy_into_table("artists", engine, dfa, cols=artists_cols)

    songs_cols = ["song_id", "title", "artist_id", "year", "duration"]
    dfs = df[songs_cols]
    copy_into_table("songs", engine, dfs, cols=songs_cols)


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
