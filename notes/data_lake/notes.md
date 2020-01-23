# Big Data

## Hardware

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
- Parallel computing uses multiple CPUs sharing the same memory.

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
