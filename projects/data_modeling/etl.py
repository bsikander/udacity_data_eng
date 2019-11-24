import os
import glob
import pandas as pd
import logging
import typing as T
import json

import sqlalchemy as sa
import stringcase

from db.postgres import copy_to_postgres
from db import query_executor
from sql_queries import song_select

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_files(path, ext: str = "json"):
    """return all files matching extension from a directory."""
    all_files = []
    for root, dirs, files in os.walk(path):
        files = glob.glob(os.path.join(root, f"*.{ext}"))
        for f in files:
            all_files.append(os.path.abspath(f))
    logger.info(f"{len(all_files)} files found in {path}")
    return all_files


def clean_cols(df, drop_cols: T.List[str] = None):
    """Normalize column names of a dataframe."""

    df.columns = df.columns.str.strip().str.replace("(", "").str.replace(")", "")
    df.columns = map(stringcase.snakecase, df.columns)

    if drop_cols is not None:
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
        df = pd.read_json(filename, lines=True)
        drop_cols = ["method", "status", "item_in_session", "auth"]
        df = clean_cols(df, drop_cols)
        return df

    logger.info(f"Processing files in {filepath}...")
    all_files = get_files(filepath)

    logger.info("Loading data from each file in {filepath} to one dataframe...")
    df = pd.DataFrame()
    for idx, f in enumerate(all_files, 1):
        dfa = process_log_file(f)
        df = df.append(dfa)

    # copy into users table
    user_cols = ["user_id", "first_name", "last_name", "gender", "level"]
    dfu = df[user_cols].drop_duplicates(subset="user_id")
    copy_into_table("users", engine, dfu, cols=user_cols)

    # convert timestamp column to datetime
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", infer_datetime_format=True)

    # copy into time table
    df = df.loc[df["page"] == "NextSong"]
    # extract timeinfo from ts and split to new cols
    df_time = df
    time_cols = ["hour", "day", "week", "month", "year", "weekday"]
    for col in time_cols:
        ts = df["ts"]
        df_time[col] = getattr(ts.dt, col)

    time_cols.append("start_time")
    df_time = df.rename(columns={"ts": "start_time"})[time_cols]
    copy_into_table("time", engine, df_time, cols=time_cols)

    # copy in to songplays table
    df_song_play = df.rename(columns={"ts": "start_time"})

    songplays_cols = [
        "artist_id",
        "song_id",
        "start_time",
        "user_id",
        "session_id",
        "level",
        "location",
        "user_agent",
    ]

    query = "SELECT artist_id, name FROM artists;"
    results = query_executor(engine, query)
    artist_dict = dict((y, x) for x, y in results)
    df_song_play["artist_id"] = df_song_play["artist"].map(artist_dict)

    query = "SELECT song_id, title FROM songs;"
    results = query_executor(engine, query)
    song_dict = dict((y, x) for x, y in results)
    df_song_play["song_id"] = df_song_play["song"].map(song_dict)
    df_song_play = df_song_play[songplays_cols]

    copy_into_table("songplays", engine, df_song_play, cols=songplays_cols)


def process_song_data(engine, filepath):
    """Extracts, transforms, and loads song data."""

    def file_to_df(filename: str):
        """Loads a song file and returns a dataframe."""
        data = json.load(open(filename))
        df = pd.DataFrame.from_records([data])
        df = clean_cols(df)
        return df

    logger.info(f"Processing files in {filepath}...")
    all_files = get_files(filepath)

    logger.info("Loading data from each file in {filepath} to one dataframe...")
    df = pd.DataFrame()
    for idx, f in enumerate(all_files, 1):
        dfa = file_to_df(f)
        df = df.append(dfa)

    # songs table
    songs_cols = ["song_id", "title", "artist_id", "year", "duration"]
    dfs = df[songs_cols]
    dfs.drop_duplicates(subset="song_id", inplace=True)
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
    dfa.drop_duplicates(subset="artist_id", inplace=True)
    copy_into_table("artists", engine, dfa, cols=artists_cols)
