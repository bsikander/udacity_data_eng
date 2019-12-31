# Introduction to Cloud Computing and AWS

**What Is Cloud Computing?**

> **Cloud computing**: the practice of using a network of **remote servers** hosted on the Internet to **store, manage, and process data**, rather than a local server or a personal computer.

**Cloud computing advantages**:
- Eliminate need to invest in costly hardware upfront.
- Rapidly provision resources
- Provide efficient global access

# DWH on AWS

Choices for implementing a data warehouse:
- Taking the **on-premise** road, think about:
  * Heterogeneity, scalability, elasticity of the tools, technologies, and processes
  * Need for diverse IT staff skills & multiple locations
  * Cost of ownership
- Taking the **cloud** road:
  * Lower barrier to entry
  * May add as you need - it's ok to change your opinion 
  * scalability & elasticity out of box
  * operational cost might be high and heterogeneity/complexity won't disappear, but...

## Cloud 

**Cloud-managed**: e.g. Amazon RDS, Amazon DynamoDB, Amazon S3
- Re-use of expertise
- Way less IT staff for security, upgrades, etc; and way less OpEx
- Deal with complexity with techniques like "infrastructure as code"
- We lose a little bit of control as things are pre-configured for us and there might not be room for customized settings

Cloud-managed Options:
- SQL
  * AWS RDS
  * Amazon Redshift: SQL Columnar, massively parallel 
- NoSQL
- Files

**Self-managed**: e.g. EC2 + Postgresql, EC2 + Cassandra, EC2 + Unix FS
- Always "catch-all" option if needed

### Amazon Redshift

**Massively Parallel Processing** (MPP) databases **parallelize the execution of one query on multiple CPUs / machines**. 
- How? A table is partitioned and partitions are processed in parallel.

Amazon Redshift is a **cloud-managed**, **column-orientated**, **MPP** database. 
- Other examples include: Teradata, Aster, Oracle ExaData, and Azure SQL
- **Column-orientated storage**
  * best suited for storing OLAP workloads, summing over a long history
  * internally, it's modified postgresql
- **MPP**:
  * Most relational databases execute multiple queries in parallel if they have access to many cores/servers
    - However, **every query is always executed on a single CPU of a single machine**.
    - Acceptable for OLTP: mostly updates and few rows retrival. e.g. many concurrent users running some query that doesn't take too long, and each user can be assigned to a different CPU. 
  * One table is partitioned into multiple tables, distributed across the CPUs; each CPU will be crunching one partition of the data. 
  
#### Redshift Architecture

Redshift **Cluster**: 
- 1 **leader node**
  * coordinates compute nodes
  * handles external communication
  * optimizes query execution
- 1+ **compute nodes**
  * each with its own CPU, memory, and disk (determined by node type)
  * *scale up*: get more powerful nodes
  * *scale out*: get more nodes
  * **node slices**:
    - each compute node is logically divided into a number of slices
    - for simplicity, think of each slice as a CPU, and each CPU has a bunch of disks **dedicated to its work**
    - a cluster with *n* slices, can process *n* partitions of a table simultaneously
 
### SQL to SQL ETL

To copy the results of a query to another table *in the same database*, we can easily use `SELECT INTO`

To copy the results of a query to another table *on a totally different database server*? 
- If both servers are running the same RDBMS, it might be possible to do `SELECT INTO` but harder between two completely different RDBMSs.
- And even if we can, we probably need to do some cleaning, tranformation, governace, etc...

A more general solution? 
- an **ETL server** can talk to the source server and runs a `SELECT` query on the source db server
- stores the results in CSV files - needs large storage space.
- `INSERT` or `COPY` the results in the destination db server. 
