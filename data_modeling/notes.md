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

The key to remember the difference between OLAP and OLTP is **analytics (A)** vs **transactions (T)**. If you want to get the price of a shoe then you are using OLTP (this has very little or no aggregations). If you want to know the total stock of shoes a particular store sold, then this requires using OLAP (since this will require aggregations). Ref https://stackoverflow.com/questions/21900185/what-are-oltp-and-olap-what-is-the-difference-between-them

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

#### Star Schemas

#### Snowflake Schemas


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
