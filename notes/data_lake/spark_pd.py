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
