def get_drop_table_query(table: str):
    """returns drop table query."""
    return f"DROP TABLE IF EXISTS {table}"


# decided against using this query because running SELECT for each row can be
# very expensive especially for event-driven files e.g. log files.
song_select = """
SELECT
    songs.artist_id as artist_id,
    songs.song_id as song_id
FROM songs
LEFT JOIN artists on artists.artist_id = songs.artist_id
WHERE songs.title = %s
AND artists.name = %s
AND songs.duration = %s
"""


# create tables
songplay_table_create = """
CREATE TABLE songplays (
    songplay_id int,
    start_time timestamp,
    user_id int,
    song_id text,
    artist_id text,
    session_id int,
    level text,
    location text,
    user_agent text
);
"""

user_table_create = """
CREATE TABLE users (
    user_id int,
    first_name text,
    last_name text,
    gender text,
    level text
);
"""

song_table_create = """
CREATE TABLE songs (
    song_id text,
    title text,
    artist_id text,
    year int,
    duration float
);
"""

artist_table_create = """
CREATE TABLE artists (
    artist_id text,
    name text,
    location text,
    latitude float,
    longitute float
);
"""

time_table_create = """
CREATE TABLE time (
    start_time timestamp,
    hour int,
    day int,
    week int,
    month int,
    year int,
    weekday int
);
"""

create_table_queries = [
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create,
]

drop_table_queries = [
    get_drop_table_query("songplays"),
    get_drop_table_query("users"),
    get_drop_table_query("songs"),
    get_drop_table_query("artists"),
    get_drop_table_query("time"),
]
