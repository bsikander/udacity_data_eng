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
    song VARCHAR,
    status INTEGER,
    ts BIGINT,
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
    COPY stg_events FROM {}
    IAM_ROLE {}
    FORMAT AS JSON {};
    """
).format(
    config.get("S3", "LOG_DATA"),
    config.get("IAM_ROLE", "ARN"),
    config.get("S3", "LOG_JSONPATH"),
)


staging_songs_copy = (
    """
    COPY stg_songs (artist_id, artist_latitude, artist_location, artist_longitude, artist_name, duration, num_songs, song_id, title, year)
    FROM {}
    IAM_ROLE {}
    JSON 'auto';
    """
).format(config.get("S3", "SONG_DATA"), config.get("IAM_ROLE", "ARN"))

# insert tables
songplay_table_insert = """
INSERT INTO fct_songplays (artist_id, level, location, session_id, song_id, start_time, user_agent, user_id)
SELECT a.artist_id AS artist_id,
       u.level AS level,
       a.location AS location,
       e.session_id AS session_id,
       s.song_id AS song_id,
       (TIMESTAMP 'epoch' + e.ts * INTERVAL '0.001 Second ') AS start_time,
       e.user_agent AS user_agent,
       e.user_id AS user_id
FROM stg_events AS e
LEFT JOIN dim_artists AS a ON (a.name = e.artist)
LEFT JOIN dim_users AS u ON (u.user_id = e.user_id)
LEFT JOIN dim_songs AS s ON (s.title = e.song)
WHERE e.page = 'NextSong';
"""

user_table_insert = """
INSERT INTO dim_users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT(user_id) AS user_id,
	   first_name AS first_name,
       last_name AS last_name,
       gender AS gender,
       level AS level
FROM stg_events WHERE user_id IS NOT NULL;
"""

song_table_insert = """
INSERT INTO dim_songs (artist_id, duration, song_id, title, year)
SELECT artist_id AS artist_id,
       cast(duration as double precision) AS duration,
       coalesce(song_id, '') AS song_id,
       coalesce(title, '') AS title,
       year AS year
FROM stg_songs;
"""

artist_table_insert = """
INSERT INTO dim_artists (artist_id, latitude, location, longitude, name)
SELECT DISTINCT(artist_id) AS artist_id,
       cast(artist_latitude as double precision) AS latitude,
       coalesce(artist_location, '') AS location,
       cast(artist_longitude as double precision) AS longitude,
       artist_name AS name
FROM stg_songs;
"""

time_table_insert = """
INSERT INTO dim_time (start_time, day, hour, month, week, weekday, year)
SELECT (TIMESTAMP 'epoch' + ts * INTERVAL '0.001 Second') as start_time,
       extract(day from start_time) as day,
       extract(hour from start_time) as hour,
       extract(month from start_time) as month,
       extract(week from start_time) as week,
       extract(weekday from start_time) as weekday,
       extract(year from start_time) as year
FROM stg_events;
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

copy_table_queries = [
    staging_songs_copy,
    staging_event_copy,
]

insert_table_queries = [
    songplay_table_insert,
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
]
