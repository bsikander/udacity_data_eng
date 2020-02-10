from pyspark.sql import SparkSession

import datetime

spark = SparkSession.builder.appName("Data wrangling with Spark SQL").getOrCreate()

path = "data/sparkify_log_small.json"
user_log = spark.read.json(path)

user_log.take(1)

# The code below creates a temporary view against which you can run SQL queries.
user_log.createOrReplaceTempView("user_log_table")

spark.sql("SELECT * FROM user_log_table LIMIT 2").show()

spark.sql(
    """
          SELECT *
          FROM user_log_table
          LIMIT 2
          """
).show()

spark.sql(
    """
          SELECT COUNT(*)
          FROM user_log_table
          """
).show()

spark.sql(
    """
          SELECT userID, firstname, page, song
          FROM user_log_table
          WHERE userID == '1046'
          """
).collect()

spark.sql(
    """
          SELECT DISTINCT page
          FROM user_log_table
          ORDER BY page ASC
          """
).show()

# User defined functions
spark.udf.register(
    "get_hour", lambda x: int(datetime.datetime.fromtimestamp(x / 1000.0).hour)
)

spark.sql(
    """
          SELECT *, get_hour(ts) AS hour
          FROM user_log_table
          LIMIT 1
          """
).collect()

songs_in_hour = spark.sql(
    """
          SELECT get_hour(ts) AS hour, COUNT(*) as plays_per_hour
          FROM user_log_table
          WHERE page = "NextSong"
          GROUP BY hour
          ORDER BY cast(hour as int) ASC
          """
)

# Converting results to pandas
songs_in_hour_pd = songs_in_hour.toPandas()
print(songs_in_hour_pd)

# Question: Which page did user id ""(empty string) NOT visit?

# SELECT distinct pages for the blank user and distinc pages for all users
# Right join the results to find pages that blank visitor did not visit
spark.sql(
    """
          SELECT *
            FROM (
                SELECT DISTINCT page
                FROM user_log_table
                WHERE userID='') AS user_pages
            RIGHT JOIN (
                SELECT DISTINCT page
                FROM user_log_table) AS all_pages
            ON user_pages.page = all_pages.page
            WHERE user_pages.page IS NULL
          """
).show()

# Question: How many female users do we have in the data set?
spark.sql(
    """
          SELECT COUNT(DISTINCT userID)
            FROM user_log_table
            WHERE gender = 'F'
          """
).show()

# Question: How many songs were played from the most played artist?

# Here is one solution
spark.sql(
    """
          SELECT Artist, COUNT(Artist) AS plays
            FROM user_log_table
            GROUP BY Artist
            ORDER BY plays DESC
            LIMIT 1
          """
).show()

# Here is an alternative solution
# Get the artist play counts
play_counts = spark.sql(
    """
                        SELECT Artist, COUNT(Artist) AS plays
                        FROM user_log_table
                        GROUP BY Artist
                        """
)

# save the results in a new view
play_counts.createOrReplaceTempView("artist_counts")

# use a self join to find where the max play equals the count value
spark.sql(
    """
          SELECT a2.Artist, a2.plays FROM
            (SELECT max(plays) AS max_plays FROM artist_counts) AS a1
            JOIN artist_counts AS a2
            ON a1.max_plays = a2.plays
          """
).show()

# Question: How many songs do users listen to on average between visiting our home page?
# Please round your answer to the closest integer.

# SELECT CASE WHEN 1 > 0 THEN 1 WHEN 2 > 0 THEN 2.0 ELSE 1.2 END;
is_home = spark.sql(
    """
                    SELECT
                        userID,
                        page,
                        ts,
                        CASE WHEN page = 'Home' THEN 1 ELSE 0 END AS is_home
                    FROM user_log_table
                    WHERE (page = 'NextSong') or (page = 'Home')
                    """
)

# keep the results in a new view
is_home.createOrReplaceTempView("is_home_table")

# find the cumulative sum over the is_home column
cumulative_sum = spark.sql(
    """
                           SELECT
                                *,
                                SUM(is_home) OVER
                                    (PARTITION BY userID
                                    ORDER BY ts DESC
                                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                                AS period
                           FROM is_home_table
                           """
)

# keep the results in a view
cumulative_sum.createOrReplaceTempView("period_table")

# find the average count for NextSong
spark.sql(
    """
          SELECT
            AVG(count_results)
          FROM
            (SELECT COUNT(*) AS count_results FROM period_table
          GROUP BY userID, period, page HAVING page = 'NextSong') AS counts
          """
).show()
