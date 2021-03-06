## instructions

### requirement
- python 3.6
- [optional] docker & docker-compose (for postgres setup)

### setup

#### install dependencies
```
➜  data_modeling git:(master) pipenv install
```

or
```
➜  data_modeling git:(master) make install
```

see output [here](https://gist.github.com/pwen/dba568665552fdde63b50b7e3860a5ef).

#### spin up postgres inside docker
```
➜  data_modeling git:(master) make down
➜  data_modeling git:(master) make up
```

see output [here](https://gist.github.com/pwen/ca8cb2255ab3ff5d8a32127f8a0e1cab).

### run the program

```
➜  data_modeling git:(master) python main.py --refresh --run-test
```

see output [here](https://gist.github.com/pwen/847233b4237d2a4c11c93c6482b6bb15).

## code design notes

**`main.py`** contains the entry point to run the program.
- it instruments logging for a more informative stdout output than `print`; can be skipped by `ENV=SKIP_INSTRUMENT` prefix.
- it then sets up the database, drop/create tables, and runs through the etl process.
 * with `--refresh` flag, it will recreates the "sparkifydb" database.
- it can run a basic set of tests with `--run-test` flag.
 * ensures each table has at least 5 records, and logs the first 5 records;
 * ensures the `songplays` fact table is correctly generated by selecting the row with `song_id` and `artist_id` properly inserted.

**`etl.py`** contains the extract-transform-load process.
- it processes json files in `data/song_data` and `data/log_data` sequentially.
  * for each file path, it grabs all files with `.json` extension, unloads all of them into one dataframe.
  * it transformas the raw dataframe to another by sanitizing, manipulating, and slicing the data so the output dataframe is suitable for a specific table.
  * post-processing it writes the dataframe to a csv string (via [`pd.to_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html)) and then loads the string into an existing postgres table (via [psycopg's `copy_from`](http://initd.org/psycopg/docs/cursor.html#cursor.copy_from) all at once.
    * 👌🏼this greatly utilizes the postgres `COPY` command to bulk insert files, isntead of using `INSERT` on one row at a time.
    * 🤔currently `pd` outputs the csv as string - and in memory; when the data gets big, we could 1) writes the csv file on disk, or 2) writes the csv file and loads to an external storage e.g. s3 bucket.
- notes on generating `songplays` fact table:
  * i had `song_select` query written down in `sql_queries.py` and decided not to use it mostly because doing a `SELECT` with `JOIN` on each row can be very expensive; especially for event-streaming files e.g. log files.
  * instead, i did `SELECT` once from `songs` and `artists` and created a dict for mapping:
    * for *artists*: `{"<artist_name>": "artist_id"}`, e.g. `{'Adam Ant': 'AR7G5I41187FB4CE6C', 'Planet P Project': 'AR8ZCNI1187B9A069B'...}`
    * for *songs*, i used a tuple of title and duration as a composite key: `{"(<song_title>, <song_duration>)": "<song_id>"}`, e.g. `{('Something Girls', 233.40363): 'SONHOTT12A8C13493C', ('Pink World', 269.81832): 'SOIAZJW12AB01853F1'...}`
  * and then used the dict to map `song` to `song_id`, and `artist` to `artist_id` (fill na with none values).
  * 👌🏼in this way i was able to minimize the numeber of calls to the database, and did most of the work **on the dataframe itself**.

`db/*` contains functions primarily concerned w/ operations on a data store.
- i intend to extend this to include other data stores, e.g. cassandra; hence the factory pattern.

#### additional thoughts
it's probably an overkill for the scope of this project but i really wanted to use this as an opportunity to learn python and specifically working with certain libraries e.g. database-related (`sqlalchemy` & `psycopg`) and `pandas`. and i had tons of fun doing just that!
