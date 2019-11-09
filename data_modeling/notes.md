## Relational Databases

### ACID transactions

#### Atomicity:
- The whole transaction is processed or nothing is processed.
- A commonly cited example of an atomic transaction is money transactions between two bank accounts. The transaction of transferring money from one account to the other is made up of two operations. First, you have to withdraw money in one account, and second you have to save the withdrawn money to the second account. An atomic transaction, i.e., when either all operations occur or nothing occurs, keeps the database in a consistent state. This ensures that if either of those two operations (withdrawing money from the 1st account or saving the money to the 2nd account) fail, the money is neither lost nor created. Source Wikipedia for a detailed description of this example.

#### Consistency:
- Only transactions that abide by constraints and rules are written into the database, otherwise the database keeps the previous state. The data should be correct across all rows and tables. 

#### Isolation: 
- Transactions are processed independently and securely, order does not matter.
- A low level of isolation enables many users to access the data simultaneously, however this also increases the possibilities of concurrency effects (e.g., dirty reads or lost updates). On the other hand, a high level of isolation reduces these chances of concurrency effects, but also uses more system resources and transactions blocking each other. 

#### Durability:
- Completed transactions are saved to database even in cases of system failure.
- A commonly cited example includes tracking flight seat bookings. So once the flight booking records a confirmed seat booking, the seat remains booked even if a system failure occurs. Source: Wikipedia.

## NoSQL Databases

Common types of NoSQL databases:
- Apache Cassandra (Partition Row store)
- MongoDB (Document store)
- DynamoDB (Key-Value store)
- Apache HBase (Wide Column store)
- Neo4j (Graph Database)

### Cassandra
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
 * However, there are exceptions to it. Some non-relational databases like MongoDB can support ACID transactions.
- When you need the ability to **do JOINS across tables**: NoSQL does not allow the ability to do JOINS. This is not allowed as this will result in *full table scans*.
- If you want to be able to do **aggregations and analytics**
- If you have **changing business requirements**: Ad-hoc queries are possible but difficult as the data model was done to fix particular queries
- If your queries are not available and you need the flexibility: You need your queries in advance. If those are not available or you will need to be able to have flexibility on how you query your data you might need to stick with a relational database
