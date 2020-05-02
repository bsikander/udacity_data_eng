# Relational Databases

## ACID transactions

- **Atomicity**:
  - The whole transaction is processed or nothing is processed.
  - A commonly cited example of an atomic transaction is money transactions between two bank accounts. The transaction of transferring money from one account to the other is made up of two operations. First, you have to withdraw money in one account, and second you have to save the withdrawn money to the second account. An atomic transaction, i.e., when either all operations occur or nothing occurs, keeps the database in a consistent state. This ensures that if either of those two operations (withdrawing money from the 1st account or saving the money to the 2nd account) fail, the money is neither lost nor created. Source Wikipedia for a detailed description of this example.

- **Consistency**:
  - Only transactions that abide by constraints and rules are written into the database, otherwise the database keeps the previous state. The data should be correct across all rows and tables.

- **Isolation**:
- Transactions are processed independently and securely, order does not matter.
- A low level of isolation enables many users to access the data simultaneously, however this also increases the possibilities of concurrency effects (e.g., dirty reads or lost updates). On the other hand, a high level of isolation reduces these chances of concurrency effects, but also uses more system resources and transactions blocking each other.

- **Durability**:
- Completed transactions are saved to database even in cases of system failure.
- A commonly cited example includes tracking flight seat bookings. So once the flight booking records a confirmed seat booking, the seat remains booked even if a system failure occurs. Source: Wikipedia.


## OLAP vs. OLTP

- **Online Analytical Processing (OLAP)**:
  * Databases optimized for these workloads allow for complex analytical and ad hoc queries, including **aggregations**. These type of databases are optimized for reads.

- **Online Transactional Processing (OLTP)**:
  * Databases optimized for these workloads allow for less complex queries in large volume. The types of queries for these databases are read, insert, update, and delete.

The key to remember the difference between OLAP and OLTP is **analytics (A)** vs **transactions (T)**. If you want to get the price of a shoe then you are using OLTP (this has very little or no aggregations). If you want to know the total stock of shoes a particular store sold, then this requires using OLAP (since this will require aggregations).

Read [stackoverflow reference](https://stackoverflow.com/questions/21900185/what-are-oltp-and-olap-what-is-the-difference-between-them)

## Structuring your data

### Normalization
- To *reduce data redunancy* and *increase data integrity*
- Objective of **normal form**:
    * To free the db from unwanted insertions, updates, and deletion dependencies
    * To reduce the need for refactoring the db as new types of data are introduced
    * To make the relational model more informative to users
    * To make the database neutral to the query statistics

**How to reach First Normal Form (1NF)**:
- **Atomic values**: each cell contains unique and single values
- Be able to add data without altering tables
- Separate different relations into different tables
- Keep relationships between tables together with **foreign keys**

**Second Normal Form (2NF)**:
- Have reached 1NF
- All columns in the table must rely on the **Primary Key**

**Third Normal Form (3NF)**:
- Must be in 2nd Normal Form
- No **transitive dependencies**
  * transitive dependencies you are trying to maintain is that to get from A-> C, you want to avoid going through B.
- When to use 3NF: when you want to update data, we want to be able to do in just 1 place.


### Denormalization
- Must be done in read heavy workloads to increase performance.
  * reads will be faster (select)
  * writes will be slower (insert, update, delete)

#### Fact and Dimension Tables

**Fact table** consists of the measurements, metrics, or facts of a business process.
**Dimensions** are **people**, **products**, **place**, and **time**.

#### Star Schema
- the simplest style of *data mart* schema.
- consists of one or more fact tables referencing any number of dimension tables.
  * fact table is at the center
  * dimension table surrounds the fact table representing the star's points
- **benefits**:
  * denormalized
  * simplifies queries
  * fast aggregations
- **drawbacks**:
  * issues that come with denormalization, e.g.
    - data integrity (duplicate data across multiple tables)
    - decreased query flexibility
    - many to many relationship (simplified)

#### Snowflake Schema
- "a complex snowflake shape emerges when the dimensions of a snowflake schema are elaborated, having multiple levels of relationships, child tables having multiple parents."

**Snowflake vs. Star**
- Star schema is a special, simplified case of the snowflake schema.
- Star schema does not allow for one to many relationships while the snowflake schema does.
- Snowflake schema is more normalized than start schema but only in 1NF or 2NF.

Ref [Deep Diving in the World of Data Warehousing](https://medium.com/@BluePi_In/deep-diving-in-the-world-of-data-warehousing-78c0d52f49a)

More refs:
- upsert: http://www.postgresqltutorial.com/postgresql-upsert/
- insert: https://www.postgresql.org/docs/9.5/sql-insert.html


# NoSQL Databases

Common types of NoSQL databases:
- Apache Cassandra (Partition Row store)
- MongoDB (Document store)
- DynamoDB (Key-Value store)
- Apache HBase (Wide Column store)
- Neo4j (Graph Database)

## Cassandra
- **keyspace**: collection of tables
- **table**: a group of partitions
- **rows**: a single item
- **partition**:
  - fundamental unit of access
  - collection of row(s)
  - how data is distributed
- **primary key**: made up of a partition key and clustering columns
- **column**:
  - *clustering* columns and *data* columns
  - labeled element

**Q: What type of companies use Apache Cassandra?**

All kinds of companies. For example, Uber uses Apache Cassandra for their entire backend. Netflix uses Apache Cassandra to serve all their videos to customers. Good use cases for NoSQL (and more specifically Apache Cassandra) are:
- Transaction logging (retail, health care)
- Internet of Things (IoT)
- Time series data
- Any workload that is heavy on writes to the database (since Apache Cassandra is optimized for writes).

**Q: When to use a NoSQL database?**
- **Needs to be able to store different data type formats**
  * NoSQL was also to handle different data configurations: structured, semi-structured, and unstructured data.
  * JSON, XML documents can all be handled easily with NoSQL
- **Large amounts of data**
  * Relational databases are not distributed databases and b/c of this they can only scale vertically by addming more storage in the machine itself.
  * NoSQL databases were created to be able to be **horizontally scalable** - the more servers/systems you add to the database the more data that can be ahosted with **high availability** and **low latency** (fast reads and writes).
- **Need horizontal scalability**
- **Need high throughput**
  * While ACID transactions bring benefits they also slow down the process of reading and writing data.
- **Need a flexible schema**: flexible schema can allow for columns to be added that do not have to be used by every row, saving disk space.
- **Need high availability**: Relational databases have a single point of failure. When that database goes down, a failover to a backup system must happen and takes time.

**Q: When NOT to use a NoSQL Database?**
- When you have **a small dataset**: NoSQL databases were made for big datasets not small datasets and while it works it wasn’t created for that.
- When you need **ACID Transactions**:
  * If you need a consistent database with ACID transactions, then most NoSQL databases will not be able to serve this need.
  * NoSQL database are **eventually consistent** and do not provide ACID transactions.
  * There are some NoSQL databases that offer some form of ACID transaction.
    - As of v4.0, **MongoDB** added multi-document ACID transactions within a single replica set. With their later version, v4.2, they have added multi-document ACID transactions in a sharded/partitioned deployment.
      * [MongoDB on multi-document ACID transactions](https://www.mongodb.com/collateral/mongodb-multi-document-acid-transactions)
      * Another post on [MongoDB's ability to handle ACID transactions](https://www.mongodb.com/blog/post/mongodb-multi-document-acid-transactions-general-availability)
    - Another example of a NoSQL database supporting ACID transactions is **MarkLogic**.
- When you need the ability to **do JOINS across tables**: NoSQL does not allow the ability to do JOINS. This is not allowed as this will result in *full table scans*.
- If you want to be able to do **aggregations and analytics**
- If you have **changing business requirements**: Ad-hoc queries are possible but difficult as the data model was done to fix particular queries
- If your **queries are not available and you need the flexibility**: You need your queries in advance. If those are not available or you will need to be able to have flexibility on how you query your data you might need to stick with a relational database

## Distributed databases

In a **distributed database**, in order to have **high availability**, you need copies of your data.

### Eventual Consistency:

Over time (if no new changes are made) each copy of the data will be the same, but if there are new changes, the data may be different in different locations. The data may be inconsistent for only milliseconds. There are workarounds in place to prevent getting stale data.

[Reference](https://en.wikipedia.org/wiki/Eventual_consistency).

**Q: What does the network look like?**

In Apache Cassandra every node is connected to every node -- it's peer to peer database architecture.

**Cassandra Architecture**
- [Understanding the architecture](https://docs.datastax.com/en/cassandra/3.0/cassandra/architecture/archTOC.html)
- [Cassandra Architecture](https://www.tutorialspoint.com/cassandra/cassandra_architecture.htm)

- *Data Replication* in Cassandra
  * One or more of the nodes in a cluster act as replicas for a given piece of data. If it is detected that some of the nodes responded with an out-of-date value, Cassandra will return the most recent value to the client. After returning the most recent value, Cassandra performs a **read repair** in the background to update the stale values.
  * Cassandra uses the **Gossip Protocol** in the background to allow the nodes to communicate with each other and detect any faulty nodes in the cluster.

- Components of Cassandra
  * **Node** − It is the place where data is stored.
  * **Data center** − It is a collection of related nodes.
  * **Cluster** − A cluster is a component that contains one or more data centers.
  * **Commit log** − The commit log is a crash-recovery mechanism in Cassandra. Every write operation is written to the commit log.
  * **Mem-table** − A mem-table is a memory-resident data structure. After commit log, the data will be written to the mem-table. Sometimes, for a single-column family, there will be multiple mem-tables.
  * **SSTable** (sorted string table) − It is a disk file to which the data is flushed from the mem-table when its contents reach a threshold value.
  * **Bloom filter** − These are nothing but quick, nondeterministic, algorithms for testing whether an element is a member of a set. It is a special kind of *cache*. Bloom filters are accessed after every query.
    * [What are bloom filters?](https://blog.medium.com/what-are-bloom-filters-1ec2a50c68ff)
- **Write** Operations
  * Every write activity of nodes is captured by the **commit logs** written in the nodes. Later the data will be captured and stored in the **mem-table**. Whenever the mem-table is full, data will be written into the **SStable data file**.
  * All writes are automatically partitioned and replicated throughout the cluster.
  * Cassandra periodically consolidates the SSTables, discarding unnecessary data.
- **Read** Operations
  * During read operations, Cassandra gets values from the **mem-table** and checks the **bloom filter** to find the appropriate **SSTable** that holds the required data.

- [How Cassandra reads and writes data](https://docs.datastax.com/en/cassandra/3.0/cassandra/dml/dmlIntro.html)
  * more in-depth about the Apache Cassandra Data Model, how Cassandra reads, writes, updates, and deletes data.

## CAP Theorem

- **Consistency**: Every read from the database gets the latest (and correct) piece of data or an error
- **Availability**: Every request is received and a response is given -- without a guarantee that the data is the latest update
- **Partition Tolerance**: The system continues to work regardless of losing network connectivity between nodes

**Q: Is Eventual Consistency the opposite of what is promised by SQL database per the ACID principle?**
Much has been written about how Consistency is interpreted in the ACID principle and the CAP theorem. Consistency in the ACID principle refers to the requirement that only transactions that abide by constraints and database rules are written into the database, otherwise the database keeps previous state. In other words, the data should be correct across all rows and tables. However, consistency in the CAP theorem refers to every read from the database getting the latest piece of data or an error.
- [Disambiguating ACID and CAP](https://www.voltdb.com/blog/2015/10/22/disambiguating-acid-cap/)

**Q: Which of these combinations is desirable for a production system - Consistency and Availability, Consistency and Partition Tolerance, or Availability and Partition Tolerance?**
As the CAP Theorem Wikipedia entry says, "The CAP theorem implies that in the presence of a network partition, one has to choose between consistency and availability." So there is no such thing as Consistency and Availability in a distributed database since it must always tolerate network issues. You can only have Consistency and Partition Tolerance (CP) or Availability and Partition Tolerance (AP). Remember, relational and non-relational databases do different things, and that's why most companies have both types of database systems.

**Q: Does Cassandra meet just Availability and Partition Tolerance in the CAP theorem?**
According to the CAP theorem, a database can actually only guarantee two out of the three in CAP. So supporting Availability and Partition Tolerance makes sense, since Availability and Partition Tolerance are the biggest requirements.

**Q: If Apache Cassandra is not built for consistency, won't the analytics pipeline break?**
If I am trying to do analysis, such as determining a trend over time, e.g., how many friends does John have on Twitter, and if you have one less person counted because of "eventual consistency" (the data may not be up-to-date in all locations), that's OK. In theory, that can be an issue but only if you are not constantly updating. If the pipeline pulls data from one node and it has not been updated, then you won't get it. Remember, in Apache Cassandra it is about Eventual Consistency.

### Data Modeling in Apache Cassandra:
- **Denormalization** is not just okay -- it's a must
- Denormalization must be done for fast reads
- Apache Cassandra has been optimized for **fast writes**
- ALWAYS think **queries** first
- *One table per query* is a great strategy
- Apache Cassandra **does not allow for JOINs between tables**
- No Group By, JOINS or sub queries possible with CQL

#### Primary Key
- Must be *unique*
  * Hasing of this value results in placement on a particular node in the system
  * data distributed by this partition key
  * you want to pick a key that will **evenly distribute** the data as best you can
- The `PRIMARY KEY` is made up of either just the `PARTITION KEY` or may also include additional `CLUSTERING COLUMNS`
- A Simple `PRIMARY KEY` is just one column that is also the `PARTITION KEY`. A **Composite** `PRIMARY KEY` is made up of more than one column and will assist in creating a unique value and in your retrieval queries
  * [datatax's Simple Primary Key](https://docs.datastax.com/en/cql/3.3/cql/cql_using/useSimplePrimaryKeyConcept.html#useSimplePrimaryKeyConcept)
- The `PARTITION KEY` will determine the *distribution of data across the system*
  * The partition key's row value will be *hashed* and stored on the node in the system that holds that range of values.

#### Clustering Columns:
- The *Primary Key* is made up of either just the *Partition Key* or with the addition of *Clustering Columns*.
  * The Clustering Column will determine the **sort order within a partition**.
  * The clustering column will sort the data in **ascending order**, e.g., alphabetical order.
- More than one clustering column can be added (or none!)
- From there the clustering columns will sort in order of how they were added to the primary key.

**Q: How many clustering columns can we add?**
You can use as many clustering columns as you would like. You cannot use the clustering columns out of order in the SELECT statement. You may choose to omit using a clustering column in your SELECT statement. That's OK. Just remember to use them in order when you are using the SELECT statement.

References
- [datastax's Compound Primary Key](https://docs.datastax.com/en/cql/3.3/cql/cql_using/useCompoundPrimaryKeyConcept.html)
- [StackOverflow: description of the difference between Partition Keys and Clustering Keys](https://stackoverflow.com/questions/24949676/difference-between-partition-key-composite-key-and-clustering-key-in-cassandra)

In a situation of **COMPOSITE primary key**, the "first part" of the key is called **PARTITION KEY**, and the second part of the key is the **CLUSTERING KEY**.
  - Please note that the both partition and clustering key can be made by more columns.

Behind these names ...
  - The **Partition Key** is responsible for data distribution across your nodes.
  - The **Clustering Key** is responsible for data sorting within the partition.
  - The **Primary Ke**y is equivalent to the Partition Key in a single-field-key table (i.e. Simple).
  - The **Composite/Compound Key** is just any multiple-column key.

#### WHERE clause
- Data modeling in Apache Cassandra is query focused, and that focus needs to be on the WHERE clause.
  * The *Partition Key* must be included in your query and any *Clustering Columns* can be used in the order they appear in your *Primary Key*.
- Failure to include a WHERE clause will result in an error
- AVOID using `ALLOW FILTERING`: Here is a [reference in DataStax](https://www.datastax.com/blog/2014/12/allow-filtering-explained) that explains ALLOW FILTERING and why you should not use it.
  * When your query is rejected by Cassandra because it needs filtering, you should resist the urge to just add ALLOW FILTERING to it. You should think about your data, your model and what you are trying to do. You always have multiple options.
    * You can change your data model, add an index, use another table or use ALLOW FILTERING.
    * You have to make the right choice for your specific use case.

**Q: Why do we need to use a WHERE statement since we are not concerned about analytics? Is it only for debugging purposes?**
The WHERE statement is allowing us to do the **fast reads**.
- With Apache Cassandra, we are talking about big data -- think terabytes of data -- so we are making it fast for read purposes.
- Data is spread across all the nodes. By using the WHERE statement, we know which node to go to, from which node to get that data and serve it back.
  * For example, imagine we have 10 years of data on 10 nodes or servers. So 1 year's data is on a separate node. By using the WHERE year = 1 statement we know which node to visit fast to pull the data from.
