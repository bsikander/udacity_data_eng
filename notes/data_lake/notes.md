# Big Data

## Hardware

- SEE Screenshots for more numbers

## Vids
- [RAM] https://www.youtube.com/watch?v=Gx0_7CUFInM
- [RAM] https://www.youtube.com/watch?v=Wvz1UeYkjsw
- [CPU] https://www.youtube.com/watch?v=LNv-urROvr0
- [Storage] https://www.youtube.com/watch?v=3nL6JM3QbQQ
- [Big data1] https://www.youtube.com/watch?v=QjPr7qeJTQk
- [Big data2] https://www.youtube.com/watch?v=314zCU4O-f4
- [Medium data] https://www.youtube.com/watch?v=5E0VLIhch6I
- [Functional Programming] https://www.youtube.com/watch?v=jSwfZ8wks_E

#### CPU (Central Processing Unit)
- The CPU is the "brain" of the computer.
- Every process on your computer is eventually handled by your CPU.
  * This includes calculations and also instructions for the other components of the compute.
- The CPU can also store small amounts of data inside itself in what are called **registers**. These registers hold data that the CPU is working with at the moment.
  * The registers make computations more efficient: the registers avoid having to send data unnecessarily back and forth between memory (RAM) and the CPU.


#### Memory (RAM)
- When your program runs, data gets temporarily stored in memory before getting sent to the CPU
- Memory is **ephemeral storage** - when your computer shuts down, the data in the memory is lost.

What are the potential trade offs of creating one computer with a lots of CPUs and memory?
- it is very efficient, but...
- **ephemeral**: we lose our data every time we shut down the machines
- **expensive**

alternative: **distributed systems**
- e.g. rather than relying on lots of memory, Google leveraged **long-term storage** on cheap, pre-used hardware.

#### Storage (SSD or Magnetic Disk)
- Storage is used for keeping data over long periods of time.
- When a program runs, the CPU will direct the memory to temporarily load data from long-term storage.

#### Network (LAN or the Internet)
- Network is the gateway for anything that you need that isn't stored on your computer.
- The network could connect to other computers in the same room (a **Local Area Network**) or to a computer on the other side of the world, connected over the internet.

The *speed of our network* has lagged behind the improvments in CPU memory and storage
- moving data across the network from one machine to another is the most common **bottleneck** when working w/ big data.
- for this reason, distributed systems try to **minimize shuffling** data back and forth across different machines

**Other Numbers to Know?**
- check out [Peter Norvig's original blog post](http://norvig.com/21-days.html) from a few years ago;
- and [an interactive version](https://colin-scott.github.io/personal_website/research/interactive_latency.html) for today's current hardware.

**Key Ratios**
- Fastest: CPU - 200x faster than memory
- Memory - 15x faster than SSD
- SSD - 20x faster than network
- Slowest: Network

## History of Distributed and Parallel Computing
- At a high level, distributed computing implies multiple CPUs each with its own memory.
- Parallel computing uses multiple CPUs sharing the same memory. (https://www.youtube.com/watch?v=9CRZURNg2zs)

### Hadoop
- **Hadoop**: an ecosystem of tools for big data storage and data analysis.
- Hadoop is an older system than Spark but is still used by many companies.
- The major difference between Spark and Hadoop is **how they use memory**.
  * **Hadoop writes intermediate results to disk whereas Spark tries to keep data in memory whenever possible**. This makes Spark faster for many use cases.

- **Hadoop MapReduce**: a system for processing and analyzing large data sets in parallel.

- **Hadoop YARN** - a resource manager that schedules jobs across a cluster.
  * The manager keeps track of what computer resources are available and then assigns those resources to specific tasks.

- **Hadoop Distributed File System (HDFS)** - a big data storage system that splits data into chunks and stores the chunks across a cluster of computers.

As Hadoop matured, other tools were developed to make Hadoop easier to work with. These tools included:
- **Apache Pig** - a SQL-like language that runs on top of Hadoop MapReduce
- **Apache Hive** - another SQL-like interface that runs on top of Hadoop MapReduce
Oftentimes when someone is talking about Hadoop in general terms, they are actually talking about Hadoop MapReduce. However, Hadoop is more than just MapReduce.

**How is Spark related to Hadoop?**
- Spark contains libraries for data analysis, machine learning, graph analysis, and streaming live data.
- Spark is generally faster than Hadoop.
  * This is because Hadoop writes intermediate results to disk whereas Spark tries to keep intermediate results in memory whenever possible.
- The Hadoop ecosystem includes a distributed file storage system called **HDFS (Hadoop Distributed File System)**. Spark, on the other hand, does not include a file storage system. You can use Spark on top of HDFS but you do not have to. Spark can read in data from other sources as well such as Amazon S3.

**Streaming Data**

**Data streaming** is a specialized topic in big data. The use case is when you want to store and analyze data in real-time such as Facebook posts or Twitter tweets.
- Spark has a streaming library called [**Spark Streaming**](https://spark.apache.org/docs/latest/streaming-programming-guide.html) although it is not as popular and fast as some other streaming libraries.
- Other popular streaming libraries include [**Storm**](http://storm.apache.org/) and [**Flink**](https://flink.apache.org/).

**Map Reduce**

MapReduce is a programming technique for manipulating large data sets. "Hadoop MapReduce" is a specific implementation of this programming technique.

The technique works by first dividing up a large dataset and distributing the data across a cluster. In the map step, each data is analyzed and converted into a (key, value) pair. Then these key-value pairs are shuffled across the cluster so that all keys are on the same machine. In the reduce step, the values with the same keys are combined together.

While Spark doesn't implement MapReduce, you can write Spark programs that behave in a similar way to the map-reduce paradigm.

**The Spark Cluster**
- Local mode
- Cluster modes
  * Standalone
  * YARN
  * Mesos

### Spark Use Cases and Resources
Here are a few resources about different Spark use cases:
- Data Analytics http://spark.apache.org/sql/
- Machine Learning http://spark.apache.org/mllib/
- Streaming http://spark.apache.org/streaming/
- Graph Analytics http://spark.apache.org/graphx/

**You Don't Always Need Spark**

Spark is meant for big data sets that cannot fit on one computer. But you don't need Spark if you are working on smaller data sets. In the cases of data sets that can fit on your local computer, there are many other options out there you can use to manipulate data such as:
- **AWK** - a command line tool for manipulating text files
- **R** - a programming language and software environment for statistical computing
- [**Python PyData Stack**](https://pydata.org/downloads/), which includes pandas, Matplotlib, NumPy, and scikit-learn among other libraries
Sometimes, you can still use pandas on a single, local machine even if your data set is only a little bit larger than memory. Pandas can read data in chunks. Depending on your use case, you can filter the data and write out the relevant parts to disk.

If the data is already stored in a relational database such as MySQL or Postgres, you can leverage SQL to extract, filter and aggregate the data. If you would like to leverage pandas and SQL simultaneously, you can use libraries such as SQLAlchemy, which provides an abstraction layer to manipulate SQL tables with generative Python expressions.

The most commonly used Python Machine Learning library is [scikit-learn](https://scikit-learn.org/stable/). It has a wide range of algorithms for classification, regression, and clustering, as well as utilities for preprocessing data, fine tuning model parameters and testing their results.
However, if you want to use more complex algorithms - like deep learning - you'll need to look further. [TensorFlow](https://www.tensorflow.org/) and [PyTorch](https://pytorch.org/) are currently popular packages.

**Spark's Limitations**
- Spark Streaming’s latency is at least 500 milliseconds since it operates on micro-batches of records, instead of processing one record at a time.
  * Native streaming tools such as Storm, Apex, or Flink can push down this latency value and might be more suitable for low-latency applications.
  * Flink and Apex can be used for batch computation as well, so if you're already using them for stream processing, there's no need to add Spark to your stack of technologies.
- Another limitation of Spark is its selection of machine learning algorithms.
  * Currently, Spark only supports algorithms that scale linearly with the input data size.
  * In general, deep learning is not available either, though there are many projects integrate Spark with Tensorflow and other deep learning tools.

**Hadoop versus Spark**
- The Hadoop ecosystem is a slightly older technology than the Spark ecosystem.
- In general, Hadoop MapReduce is slower than Spark because Hadoop writes data out to disk during intermediate steps.
  * However, many big companies, such as Facebook and LinkedIn, started using Big Data early and built their infrastructure around the Hadoop ecosystem.
  * While Spark is great for iterative algorithms, there is not much of a performance boost over Hadoop MapReduce when doing simple counting.
  * Migrating legacy code to Spark, especially on hundreds of nodes that are already in production, might not be worth the cost for the small performance boost.

**Beyond Spark for Storing and Processing Big Data**

Keep in mind that Spark is not a data storage system, and there are a number of tools besides Spark that can be used to process and analyze large datasets.

Sometimes it makes sense to use the power and simplicity of SQL on big data. For these cases, a new class of databases, know as NoSQL and NewSQL, have been developed.
- For example, you might hear about newer database storage systems like HBase or Cassandra.
- There are also distributed SQL engines like Impala and Presto. Many of these technologies use query syntax that you are likely already familiar with based on your experiences with Python and SQL.


### Data Wrangling with Spark
- Spark uses functional programming to take advantage of pure functions

read more on [lambda functions](http://palmstroem.blogspot.com/2012/05/lambda-calculus-for-absolute-dummies.html)

e.g.
```
def convert_song_to_lowercase(song):
    return song.lower()

distributed_song_log.map(convert_song_to_lowercase)

PythonRDD[1] at RDD at PythonRDD.scala:53
```

- You'll notice that this code cell ran quite quickly. This is because of **lazy evaluation**.
  * Spark does not actually execute the map step unless it needs to.
- "**RDD**" in the output refers to **resilient distributed dataset**.
  * RDDs are exactly what they say they are: fault-tolerant datasets distributed across a cluster. This is how Spark stores data.
- To get Spark to actually run the map step, you need to use an "action". One available action is the collect method. The `collect()` method takes the results from all of the clusters and "collects" them into a single list on the master node.

**Distributed Date Store**
- [**HDFS**](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html) - Hadoop Distributed File System
  * splits files into 64 or 128 megabyte blocks and replicates these blocks across the cluster
  * so data is stored in a **fault tolerant** way and can be accessed in digestible chunks
- [Amazon S3](https://aws.amazon.com/s3/)

#### Imperative vs Declarative programming

- Imperative Programming
  * e.g. Spark Dataframes & Python
  * "How"
- Declarative Programming
  * e.g. SQL
  * "What"


### Data Wrangling with DataFrames

**General functions**
- `select()`
- `filter()`
- `where()`
- `sort()`
- `dropDuplicates()`
- `withColumn()`

**Aggregate functions**
- Spark SQL provides built-in methods for the most common aggregations such as `count()`, `countDistinct()`, `avg()`, `max()`, `min()`, etc. in the `pyspark.sql.functions` module.
  * These methods are not the same as the built-in methods in the Python Standard Library, where we can find `min()` for example as well, hence you need to be careful not to use them interchangeably.
- In many cases, there are multiple ways to express the same aggregations.
  * For example, if we would like to compute one type of aggregate for one or more columns of the DataFrame we can just simply chain the aggregate method after a `groupBy()`.
  * If we would like to use different functions on different columns, `agg()` comes in handy. For example `agg({"salary": "avg", "age": "max"})` computes the average salary and maximum age.

**User defined functions (UDF)**
- In Spark SQL we can define our own functions with the udf method from the `pyspark.sql.function`s module.
- The default type of the returned variable for UDFs is string. If we would like to return an other type we need to explicitly do so by using the different types from the `pyspark.sql.types` module.

**Window functions**
- Window functions are a way of **combining the values of ranges of rows in a DataFrame**.
- When defining the window we can choose:
  * how to **sort** and **group** (with the `partitionBy` method) the rows, and
  * how wide of a window we'd like to use (described by `rangeBetween` or `rowsBetween`).

For further information see the [Spark SQL, DataFrames and Datasets Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html) and the [Spark Python API Docs](https://spark.apache.org/docs/latest/api/python/index.html).

#### Spark SQL
- [Spark SQL built-in functions](https://spark.apache.org/docs/latest/api/sql/index.html)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/api/sql/index.html)

#### RDDs
- Spark's query optimizer is called **Catalyst**
- **RDD**s, or **Resilient Distributed Data Set** are a low-level abstraction of the data. 
  * In the first version of Spark, you worked directly with RDDs.
  * You can think of RDDs as long lists distributed across various machines. 
  * You can still use RDDs as part of your Spark code although data frames and SQL are easier. 
- You can find some further explanation of the difference between RDDs and DataFrames in Databricks' [A Tale of Three Apache Spark APIs: RDDs, DataFrames, and Datasets](https://databricks.com/blog/2016/07/14/a-tale-of-three-apache-spark-apis-rdds-dataframes-and-datasets.html) blog post.
- Here is a link to the Spark documentation's [RDD programming guide](https://spark.apache.org/docs/latest/rdd-programming-guide.html).

### Debugging & Optimization

- Work with distributed data
- Spark Web UI
- Optimize code for efficiency
- Common Spark issues

**From Local Mode to Cluster Mode**

Spark Cluster Managers:
- Standalone Mode
- MESOS
- YARN

### Data Lake
Data warehouse is already enough for most of the orgs and is the prefered way but there are reason for datalake
- Unstructured data
- Data volume
- New type of analysis emerging e.g. predictive analytics
- New tools like Hadoop/Spark opened more powerful ways to analyze

##### Unstructured data in class warehouse
- Possible but difficult
- ETL process can convert JSON to tabular format. Deep nested json can be an issue.
- Text/pdf can be stored as blob in the DW but mostly useless

##### Schema On Read vs Schema On Write
- Load a csv and already start querying

```
Data lake is the new data warehouse
```
Data lake shares the goals of data warehouse for supporting business in their day to day activities beyond transactional.

##### Big Data effect on DW
- Low cost of storage
- Moving ETL to big data became clear
- Big data clusters can do ETL + data storage and can relief DW from the storage burden. Generally the data which was too heavy for DW can now be stored in big data cluster.

![alt text](https://github.com/bsikander/udacity_data_eng/blob/master/notes/data_lake/Screen%20Shot%202020-05-06%20at%2015.01.57.png)
