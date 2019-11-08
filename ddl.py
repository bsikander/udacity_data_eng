import psycopg2
from string import Template

try:
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
except psycopg2.Error as e:
    print("Error: Could not make connection to the Postgres database")
    print(e)

try:
    cur = conn.cursor()
except psycopg2.Error as e:
    print("Error: Could not get curser to the Database")
    print(e)

conn.set_session(autocommit=True)

try:
    cur.execute("create database crossfit")
except psycopg2.Error as e:
    print(e)

try:
    conn.close()
except psycopg2.Error as e:
    print(e)

try:
    conn = psycopg2.connect("host=127.0.0.1 dbname=crossfit user=student password=student")
except psycopg2.Error as e:
    print("Error: Could not make connection to the Postgres database")
    print(e)

try:
    cur = conn.cursor()
except psycopg2.Error as e:
    print("Error: Could not get curser to the Database")
    print(e)

conn.set_session(autocommit=True)

create_table_sql = """
    CREATE TABLE IF NOT EXISTS songs (
        song_title text,
        artist_name text,
        year integer,
        albumn_name text,
        single boolean
    );
"""
try:
    cur.execute(create_table_sql)
except psycopg2.Error as e:
    print (e)

insert_table_sql = """
    INSERT INTO songs ()
    VALUES ($song_title, $artist_name, $year, $albumn_name, $single)
"""

def insert_into(data):
    tmpl = Template(insert_table_sql)
    tmpl.substitue(song_title=data[0], artist_name=data[1], year=data[2], album_name=data[3], single=data[4])
    try:
        cur.execute(tmpl)
    except psycopg2.Error as e:
        print (e)

data = [
    ["Across The Universe", "The Beatles", "1970", "False", "Let It Be"],
    ["The Beatles", "Think For Yourself", "False", "1965", "Rubber Soul"],
]
