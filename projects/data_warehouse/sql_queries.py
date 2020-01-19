import configparser

config = configparser.ConfigParser()
config.read("dwh.cfg")

# CREATE TABLES
staging_events_table_create = """
CREATE TABLE IF NOT EXISTS "stg_events" (
    artist VARCHAR,
    auth VARCHAR,
    first_name VARCHAR,
    gender CHAR,
    item_in_session SMALLINT,
    last_name VARCHAR,
    length DOUBLE PRECISION,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration DOUBLE PRECISION,
    session_id INTEGER,
    status INTEGER,
    ts TIMESTAMP,
    user_agent VARCHAR,
    user_id INTEGER
);
"""

staging_songs_table_create = """
CREATE TABLE IF NOT EXISTS "stg_songs" (
    num_songs SMALLINT,
    artist_id VARCHAR,
    artist_latitude DOUBLE PRECISION,
    artist_longitude DOUBLE PRECISION,
    artist_location VARCHAR,
    artist_name VARCHAR,
    song_id VARCHAR,
    title VARCHAR,
    duration DOUBLE PRECISION,
    year INTEGER
);
"""

songplay_table_create = """
CREATE TABLE IF NOT EXISTS "fct_songplays" (
    songplay_id BIGINT IDENTITY(0, 1) NOT NULL,
    start_time TIMESTAMP,
    user_id INTEGER NOT NULL,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INTEGER,
    location VARCHAR,
    user_agent VARCHAR
);
"""

user_table_create = """
CREATE TABLE IF NOT EXISTS "dim_users" (
    user_id integer NOT NULL,
    first_name VARCHAR,
    last_name VARCHAR,
    gender CHAR,
    level VARCHAR
);
"""

song_table_create = """
CREATE TABLE IF NOT EXISTS "dim_songs" (
    song_id VARCHAR,
    title VARCHAR,
    artist_id VARCHAR,
    year INTEGER,
    duration DOUBLE PRECISION
);
"""

artist_table_create = """
CREATE TABLE IF NOT EXISTS "dim_artists" (
    artist_id VARCHAR,
    name VARCHAR,
    location VARCHAR,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);
"""

time_table_create = """
CREATE TABLE IF NOT EXISTS "dim_time" (
    start_time TIMESTAMP,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER
);
"""

# Staging tables

staging_events_copy = (
    """
    """
).format()

staging_songs_copy = (
    """
    """
).format()

# insert tables
songplay_table_insert = """
"""

user_table_insert = """
"""

song_table_insert = """
"""

artist_table_insert = """
"""

time_table_insert = """
"""

# List of queries
create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]


def get_drop_table_query(table: str):
    """returns drop table query."""
    return f"DROP TABLE IF EXISTS {table}"


drop_table_queries = [
    get_drop_table_query("stg_events"),
    get_drop_table_query("stg_songs"),
    get_drop_table_query("fct_songplays"),
    get_drop_table_query("dim_users"),
    get_drop_table_query("dim_songs"),
    get_drop_table_query("dim_artists"),
    get_drop_table_query("dim_time"),
]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [
    songplay_table_insert,
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
]
