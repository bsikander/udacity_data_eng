from cassandra.cluster import Cluster
from string import Template


class Cassandra:
    def __init__(self, host: str = "127.0.0.1"):
        self.host = host

    def connect(self):
        try:
            cluster = Cluster([self.host])
            self.session = cluster.connect()
        except Exception as e:
            print(e)

    def create_keyspace(
        self,
        keyspace: str = "default_db",
        rep_class: str = "SimpleStrategy",
        rep_factor: int = 1,
    ):
        create_query = """
            CREATE KEYSPACE IF NOT EXISTS {keyspace}
            WITH REPLICATION =
            { 'class' : {rep_class}, 'replication_factor' : {rep_factor} }
        """
        try:
            self.session.execute(create_query)
            self.session.set_keyspace(keyspace)
        except Exception as e:
            print(e)

    def run(self, query: str = None):
        try:
            self.session.execute(query)
        except Exception as e:
            print(e)


session = Cassandra().connect()

create_table_query = """
    CREATE TABLE IF NOT EXISTS songs (
        song_title text,
        artist_name text,
        year int,
        albumn_name text,
        single boolean,
        PRIMARY KEY (year, artist_name)
    );
"""
session.run(create_table_query)

insert_into_sql = """
    INSERT INTO songs (song_title, artist_name, year, albumn_name, single)
    VALUES ('$song_title', '$artist_name', $year, '$albumn_name', $single)
"""


def get_insert_dml(row):
    tmpl = Template(insert_into_sql)
    return tmpl.substitute(
        song_title=row[0],
        artist_name=row[1],
        year=row[2],
        albumn_name=row[3],
        single=row[4],
    )


data = (
    ["Across The Universe", "The Beatles", "1970", "Let It Be", "False"],
    ["Think For Yourself", "The Beatles", "1965", "Rubber Soul", "False"],
)


for insert_query in map(get_insert_dml, data):
    session.run(insert_query)
