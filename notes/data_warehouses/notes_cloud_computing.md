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

Ingesting at scale: 
- to transfer data from an S3 staging area to redshift use the `COPY` command
  * inserting data row using `INSERT` will be very slow
- if the file is large, it's better to break it into **multiple files**
  - each redshift slice will act as a separate worker and will use ingest the split of a file in parallel, so the process will complete much faster
  - ingest **in parallel**:
    * either using a **common prefix**
    * or a **manifest file**
- better to ingest from **the same AWS region**
- better to **compress** the csv files
- one can also speficy the delimiter to be used, if not '`,`'.


using a **common prefix** e.g. `part`
```sql
COPY sporting_event_ticket FROM 's3://udacity-labs/tickets/split/part'
CREDENTIALS 'aws_iam_role=arn:aws:iam:464956546:role/dwhRole'
gzip DELIMITER ';' REGION 'us-west-2'
```

using **manifest file** - if the files have a common suffix and not a common prefix, we actually need to create a manifest specifying the list of files, e.g.
```sql
COPY customer FROM 's3://mybucket/cust.manifest'
IAM_ROLE 'arn:aws:iam:0123456789012:role/myRedshiftRole'
manifest;
```

**Redshift ELT Automatic Compression Optimization**
- The optimal compression strategy for each column type is different
- Redshift gives the user control over the compression of each column
- The `COPY` command makes automatic best-effort compression decisions of each column

**ETL out of Redshift**
- Redshift is accessible, like any relational database, as a JDBC/ODBC source
  * naturally used by BI app
- However, we may need to extract data out of Redshift to **pre-aggregated OLAP cubes**

```sql
UNLOAD ('select * from venue limit 10')
TO 's3://mybucket/venue_pipe_'
IAM_ROLE 'arn:aws:iam:0123456789012:role/myRedshiftRole'
```

**ETL from other sources**
It's also possible to **ingest directly** using *ssh* from EC2 machines
- S3 needs to be used as a **staging area**
- Usually, an EC2 ETL worker needs to run the ingestion job **orchestrated by a dataflow product** like Airflow, Luigi, Nifi, StreamSet or AWS Data Pipeline. 

### Building A Redshift Cluster
[Launching a Redshift Cluster in the AWS console](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/445568fc-578d-4d3e-ab9c-2d186728ab22/lessons/21d59f40-6033-40b5-81a2-4a3211d9f46e/concepts/fad03fb3-ce48-4a69-9887-4baf8751cae3)

Note: The steps below were introduced in lesson 2. 
- [Create an IAM role](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/445568fc-578d-4d3e-ab9c-2d186728ab22/lessons/53e6c5d3-c9bb-4938-9133-bf8c6bfad3da/concepts/ef0f5bdf-d5e2-461c-b375-fc0dd89ccb79)
- [Create a Security Group](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/445568fc-578d-4d3e-ab9c-2d186728ab22/lessons/53e6c5d3-c9bb-4938-9133-bf8c6bfad3da/concepts/2609fcec-122e-4780-bfff-510713320800)
- [Create an IAM user](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/445568fc-578d-4d3e-ab9c-2d186728ab22/lessons/53e6c5d3-c9bb-4938-9133-bf8c6bfad3da/concepts/0436985e-ead1-42ce-b8c4-982ab5ca2178)
- [Delete a Redshift Cluster](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/445568fc-578d-4d3e-ab9c-2d186728ab22/lessons/53e6c5d3-c9bb-4938-9133-bf8c6bfad3da/concepts/97c74cce-8f6f-41f1-828b-9220f640d739)
- [Create a S3 bucket](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/445568fc-578d-4d3e-ab9c-2d186728ab22/lessons/53e6c5d3-c9bb-4938-9133-bf8c6bfad3da/concepts/29f83c05-0897-48e4-b6f3-c778dd95cb65)
- [Upload to S3 bucket](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/445568fc-578d-4d3e-ab9c-2d186728ab22/lessons/53e6c5d3-c9bb-4938-9133-bf8c6bfad3da/concepts/25f1b022-bda6-49b0-9f20-ca9ac3de633c)
- [Create PostgresSQL RDS](https://classroom.udacity.com/nanodegrees/nd027/parts/69a25b76-3ebd-4b72-b7cb-03d82da12844/modules/445568fc-578d-4d3e-ab9c-2d186728ab22/lessons/53e6c5d3-c9bb-4938-9133-bf8c6bfad3da/concepts/6e828ca4-2950-4794-b804-b5bf25af3562)

**Key recommendations for using your AWS credits wisely**:
- Delete your Amazon Redshift cluster each time you're finished working.
- Use a smaller subset of your data while you code and debug on AWS, and only execute with the full dataset on AWS as a final test of your code.

**security settings**:
- Redshift has to act as a user who has Read access to S3 
- Jupyter has to be able to connect
  * Redshift is launched within a VPC
  * this means we need to change TCP ports open in the security group, so we can access this DWH from the outside

### Infrastructure as Code on AWS
An advantage of being in the cloud is the ability to **create infrastructure, i.e. machines, users, roles, folders and processes using code**. 
- IaC lets you automate, maintain, deploy, replicate and share complex infrastructures as easily as you maintain code (undreamt-of in an on-premise deployment) e.g. "creating a machine is as easy as opening a file."
  * **sharing**: one can share all the steps with others easily
  * **reproducibility**: one can be sure that no steps are forgotten. 
  * **multiple deployments**: one can create a test environment identical to the production environment
  * **maintainability**: if a change is needed, one can keep track of the changes by comparing the code 
- IaC is border-line dataEng/devOps.

We have a number of options to achieve IaC on AWS:
- `aws-cli` scripts
  * similar to bash scripts
  * simple & convenient
- AWS sdk
  * available in a lot of languages, e.g. Java, Ruby, Python, Go, Node, etc.
  * more powerful, could be integrated with apps
- **Amazon Cloud Formation**
  * json description of all resources, permissions, constraints
  * atomic - "stack" either all succeed or all fail

Our IaC choice:
- will use the python AWS SDK aka `boto3`
- will create one IAM user called `dwhadmin`
  * will give admin privileges 
  * will use its access token and secret to build our cluster and configure it, that should be our last "click-and-fill" process
