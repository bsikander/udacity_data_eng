import os
import glob
import pandas as pd
import logging
import typing as T
import json

import sqlalchemy as sa

from db.postgres import copy_to_postgres

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


def clean_cols(df, drop_cols: T.List[str] = []):
    """Normalize column names of a dataframe."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
    )
    df = df.drop(columns=drop_cols)
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


def process_log_data(engine, filepath):
    """Extracts, transforms, and loads log data."""

    def process_log_file(filename: str):
        """Loads a log file, sanitizes it, and returns a dataframe."""
        df = pd.read_json(filename, orient="records")
        drop_cols = ["user_agent", "method", "session_id", "status"]
        df = clean_cols(df, drop_cols)

        # artist, auth, firstName, gender, itemInSession, lastName, length,
        # level, location, method, page, registration, sessionId, song, status,
        # ts, userAgent, userId

        # convert timestamp column to datetime
        df["ts"] = pd.to_datetime(df["ts"], unit="s")

        return df

    all_files = get_files(filepath)

    logger.info("Reading log data from json to df...")
    df = pd.DataFrame()
    for idx, f in enumerate(all_files, 1):
        dfa = process_log_file(f)
        df = df.append(dfa)

    # copy into users table
    user_cols = ["user_id", "first_name", "last_name", "gender", "level"]
    dfu = df[user_cols].drop_duplicates(subset="user_id", keep=False)
    copy_into_table("users", engine, dfu, cols=user_cols)

    # copy into time table
    time_cols = ["start_time", "hour", "day", "week", "month", "year", "weekday"]

    # song plays table
    dfsp = df.loc[df["page"] == "NextSong"]
    song_plays_cols = [
        "songplay_id",
        "start_time",
        "user_id",
        "song_id",
        "artist_id",
        "session_id",
        "level",
        "location",
        "user_agent",
    ]


def process_song_data(engine, filepath):
    """Extracts, transforms, and loads song data."""

    def file_to_df(filename: str):
        """Loads a song file and returns a dataframe."""
        data = json.load(open(filename))
        df = pd.DataFrame.from_records([data])
        # TODO: drop some cols
        df = clean_cols(df)
        return df

    all_files = get_files(filepath)

    logger.info("Reading song data from json to df...")
    df = pd.DataFrame()
    for idx, f in enumerate(all_files, 1):
        dfa = file_to_df(f)
        df = df.append(dfa)

    # songs table
    songs_cols = ["song_id", "title", "artist_id", "year", "duration"]
    dfs = df[songs_cols]
    copy_into_table("songs", engine, dfs, cols=songs_cols)

    # artists table
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
    dfa.drop_duplicates(subset="artist_id", keep=False, inplace=True)
    copy_into_table("artists", engine, dfa, cols=artists_cols)
