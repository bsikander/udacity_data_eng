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
