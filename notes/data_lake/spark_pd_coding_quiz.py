from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    isnan,
    count,
    when,
    col,
    desc,
    udf,
    col,
    sort_array,
    asc,
    avg,
)
from pyspark.sql.functions import sum as Fsum
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType

spark = SparkSession.builder.appName("Data Frames practice").getOrCreate()

df = spark.read.json("data/sparkify_log_small.json")

df.printSchema()

# Q: Which pages did users with empty string not visit?

blank_pages = (
    df.filter(df.userId == "").select(col("page").alias("blank_pages")).dropDuplicates()
)

all_pages = df.select("page").dropDuplicates()

for row in set(all_pages.collect()) - set(blank_pages.collect()):
    print(row.page)

# Q: How many female users do we have in the data set?
df.filter(df.gender == "F").select("userId", "gender").dropDuplicates().count()

# Q: How many songs were played from the most played artist?
df.filter(df.page == "NextSong").select("Artist").groupBy("Artist").agg(
    {"Artist": "count"}
).withColumnRenamed("count(Artist)", "artist_count").sort(desc("artist_count")).show(1)

# Q: How many songs do users listen to on average between visiting our home page?
# Please round your answer to the closest integer.
# TODO: filter out 0 sum and max sum to get more exact answer

function = udf(lambda ishome: int(ishome == "Home"), IntegerType())

user_window = (
    Window.partitionBy("userID")
    .orderBy(desc("ts"))
    .rangeBetween(Window.unboundedPreceding, 0)
)

cusum = (
    df.filter((df.page == "NextSong") | (df.page == "Home"))
    .select("userID", "page", "ts")
    .withColumn("homevisit", function(col("page")))
    .withColumn("period", Fsum("homevisit").over(user_window))
)

cusum.filter((cusum.page == "NextSong")).groupBy("userID", "period").agg(
    {"period": "count"}
).agg({"count(period)": "avg"}).show()
