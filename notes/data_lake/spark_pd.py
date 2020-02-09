from pyspark.sql import SparkSession
from pyspark.sql.functions import asc, desc, udf
from pyspark.sql.functions import sum as Fsum
from pyspark.sql.types import IntegerType, StringType

import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = "hdfs://ec2-34-218-86-174.us-west-2.compute.amazonaws.com:9000/sparkify/sparkify_log_small.json"
spark = SparkSession.builder.appName("wrangling v1").getOrCreate()
user_log = spark.read.json(path)

user_log.select("page").dropDuplicates().sort("page").show()

user_log.select(["userId", "firstname", "page", "song"]).where(
    user_log.userId == "1046"
).collect()

# convert time from epoch to datetime
get_hour = udf(lambda x: datetime.datetime.fromtimestamp(x / 1000.0).hour)
user_log = user_log.withColumn("hour", get_hour(user_log.ts))

songs_in_hour = (
    user_log.filter(user_log.page == "NextSong")
    .groupby(user_log.hour)
    .count()
    .orderBy(user_log.hour.cast("float"))
)

df = songs_in_hour.toPandas()
plt.scatter(df["hour"], df["count"])
plt.xlim(-1, 25)
plt.ylim(0, 1.2 * max(df["count"]))
plt.xlabel("hour")
plt.ylabel("songs played")

user_log_valid = user_log.dropna(how="any", subset=["userId", "sessionId"])
user_log.count()
user_log_valid.count()

user_log_valid.filter("page = 'Submit Downgrade'").show()
flag_downgrade_event = udf(lambda x: 1 if x == "Submit Downgrade" else 0, IntegerType())
user_log_valid.withColumn("downgraded", flag_downgrade_event(user_log_valid.page))
