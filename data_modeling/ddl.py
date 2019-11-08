import psycopg2
from string import Template
from functional import seq


class Postgres:
    def __init__(
        self,
        host: str = "127.0.0.1",
        dbname: str = "default",
        user: str = "student",
        password: str = "student",
    ):
        self.conn_params = (
            f"host={host} dbname={dbname} user={user} password={password}"
        )

    def connect(self):
        try:
            self.conn = psycopg2.connect(self.conn_params)
            self.conn.set_session(autocommit=True)
        except psycopg2.Error as e:
            print("Error: Could not make connection to the Postgres database")
            print(e)

    def run(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
        except psycopg2.Error as e:
            print(e)


pg_conn = Postgres().connect()

create_table_sql = """
    CREATE TABLE IF NOT EXISTS songs (
        song_title text,
        artist_name text,
        year integer,
        albumn_name text,
        single boolean
    );
"""
pg_conn.run(create_table_sql)

insert_table_sql = """
    INSERT INTO songs (song_title, artist_name, year, albumn_name, single)
    VALUES ('$song_title', '$artist_name', '$year', '$albumn_name', '$single')
"""


def get_insert_dml(row):
    tmpl = Template(insert_table_sql)
    return tmpl.substitue(
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

(
    seq(data)
    .map(lambda row: get_insert_dml(row))
    .map(lambda insert_sql: pg_conn.run(insert_sql))
)
