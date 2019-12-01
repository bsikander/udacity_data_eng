from cassandra.cluster import Cluster

# boilerplate code for db connection
try:
    cluster = Cluster(["127.0.0.1"])
    session = cluster.connect()
    # create a keyspace to work on
    session.execute(
        """
        CREATE KEYSPACE IF NOT EXISTS udacity
        WITH REPLICATION =
        { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""
    )
    # connect to our Keyspace.
    # compare this to how we had to create a new session in PostgreSQL.
    session.set_keyspace("udacity")
except Exception as e:
    print(e)


# we want to ask 3 questions of the data
# 1. Give every album in the music library that was released in a given year
#   select * from music_library WHERE YEAR=1970
#
# 2. Give every album in the music library that was created by a given artist
#   select * from artist_library WHERE artist_name="The Beatles"
#
# 3. Give all the information from the music library about a given album
#   select * from album_library WHERE album_name="Close To You"

# create tables
create_table_one_query = """
    CREATE TABLE IF NOT EXISTS music_library (
        year int,
        artist_name text,
        album_name text,
        PRIMARY KEY (year, artist_name)
    );
"""

create_table_two_query = """
    CREATE TABLE IF NOT EXISTS artist_library (
        artist_name text,
        album_name text,
        year int,
        PRIMARY KEY (artist_name, year)
    );
"""

create_table_three_query = """
    CREATE TABLE IF NOT EXISTS album_library (
        album_name text,
        artist_name text,
        year int,
        PRIMARY KEY (album_name, artist_name)
    );
"""

for query in [create_table_one_query, create_table_two_query, create_table_three_query]:
    try:
        session.execute(query)
    except Exception as e:
        print(e)

# insert into tables
insert_query_one = """
    INSERT INTO music_library (year, artist_name, album_name)
    VALUES (%s, %s, %s)
"""

insert_query_two = """
    INSERT INTO artist_library (artist_name, year, album_name)
    VALUES (%s, %s, %s)
"""

insert_query_three = """
    INSERT INTO album_library (album_name, artist_name, year)
    VALUES (%s, %s, %s)
"""

for data in [
    (1970, "The Beatles", "Let it Be"),
    (1965, "The Beatles", "Rubber Soul"),
    (1965, "The Who", "My Generation"),
    (1966, "The Monkees", "The Monkees"),
    (1970, "The Carpenters", "Close To You"),
]:
    try:
        session.execute(insert_query_one, data)
    except Exception as e:
        print(e)

for data in [
    ("The Beatles", 1970, "Let it Be"),
    ("The Beatles", 1965, "Rubber Soul"),
    ("The Who", 1965, "My Generation"),
    ("The Monkees", 1966, "The Monkees"),
    ("The Carpenters", 1970, "Close To You"),
]:
    try:
        session.execute(insert_query_two, data)
    except Exception as e:
        print(e)

for data in [
    ("Let it Be", "The Beatles", 1970),
    ("Rubber Soul", "The Beatles", 1965),
    ("My Generation", "The Who", 1965),
    ("The Monkees", "The Monkees", 1966),
    ("Close To You", "The Carpenters", 1970),
]:
    try:
        session.execute(insert_query_three, data)
    except Exception as e:
        print(e)
