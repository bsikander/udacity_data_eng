import cassandra
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
