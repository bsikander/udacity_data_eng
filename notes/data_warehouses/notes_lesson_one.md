# Intro to Data Warehouse

Definitions:
- A data warehouse is a **copy** of transaction data specifically structured for query and analysis.
- A data warehouse is a **subject-oriented**, **integrated**, **nonvolatile**, and **time-variant** collection of data in support of management's decisions.

DWH components and processes:
- ETL: **extract** the data from the source systems used for operation, **transform** the data and **load** it into a dimensional model
- the technologies used for storing dimensional models are different than tranditional technologies
- business-user-facing applications are needed, with clear visuals, aka **Business Intelligence** (BI) apps.

DW goals:
- simple to understand
- quality assured
- performant
- handles new questions well
- secure

## Dimensional Modeling

Goals:
- easy to understand
- fast analytical query performance

#### Fact tables
- record business events, like an order, a phone call, a book review
- fact table columns record events in quantifiable **metrics** like quantity of an item, duration of a call, a book rating
- the simplest rule is that a fact is usually **numeric** and **additive**
  * a comment on an article represent an event but we cannot easily make a statics out of its content per se (not a good fact)
  * invoice number is numeric, but adding it does not make sense (not a good fact)
  * total amount of an invoice could be added to compute total series (a good fact)


#### Dimensional tables
- record the context of the business events, e.g. who, what, where, why...
- dimension table columns contain **attributes** like the store at which an item is purchased, or the customer who made the call, etc.
  * **date & time** are always a dimension
  * **physical location** and their attributes are good candidates for dimensions
  * **human roles** like customers and staff are always good candidates for dimensions
  * **goods sold** always good candidates for dimensions

*Note on REFERENCES constraints*:

When building a fact table, you use the `REFERENCES` constraint to identify which table and column a foreign key is connected to. This ensures that the fact table does not refer to items that do not appear in the respective dimension tables. You can read more [here](https://www.postgresql.org/docs/9.2/ddl-constraints.html). Here's an example of the syntax on a different schema:
```
CREATE TABLE orders (
    order_id integer PRIMARY KEY,
    product_no integer REFERENCES products (product_no),
    quantity integer
);
```

## DWH Architecture

### Kimball's Bus Architecture

**ETL System** (kitchen)
- transform from source to target
- conform dimensions
- no user query support

**Presentation Area** (dining room)
- **dimensional**
- **atomic** & summary data
  * as opposed to keeping the data at the aggregated level
- organized by business processes
- uses **conformed dimensions**
  * e.g. if i use date dimensions, i try to use it across all departments; try to generalize and build all of my dimensions in a way that is usable by the whole organization.

**Applications** (dining room)
- ad hoc queries
- standard reports
- analytic apps

**ETL: A closer look**
- Extracting:
  * Get the data from its source
  * Possibly delete old state
- Transforming:
  * **Integrates** many sources together
  * Possibly **cleaning**: inconsistencies, duplication, missing values, etc.
  * Possibly producing **diagnostic metadata**
- Loading:
  * Structuring and loading the data into dimensional data model

### Independent Data Marts
- Each department has independent ETL processes & dimensional models.
- These **separate & smaller** dimensional models are called "**Data Marts**".
- Different fact tables for the same events; **no conformed dimensions**.
- **Uncoordinated efforts** can lead to **inconsistent views**.
- Despite awareness of the emergence of this architecture from departmental autonomy, it is generally discouraged.

### Inmon's Corporate Information Factory (CIF)
Think of an *open kitchen*.
- 2 ETL Processes
  * from source system to 3NF database
  * from 3NF database to departmental data marts
- The 3NF DB acts as an **enterprise wide data store**.
  * single integrated source of truth for data-marts
  * could be accessed by end-users if needed
- Data marts dimensionally modelled & unlike Kimball's dimensional models, they're mostly aggregated.

### Hybrid Kimball Bus & CIF
The Hybrid Kimball Bus and Inmon CIF model stays true to the Enterprise Data Warehouse with data maintained in 3NF even though normalized data tables may not be optimal for BI reports.

## OLAP Cubes
An OLAP cube is an aggregation of a fact metric on a number of dimensions, e.g. Movie, Branch, Month
- easy to communicate to business users

Common OLAP **operations** include: **Rollup, drill-down, slice & dice**.
- **Roll-up**: Sum up the sales of each city by country, e.g. US, France (less columns in branch dimension)
- **Drill-down**: Decompose the sales of each city into smaller districts (more columns in branch dimension)
  * The **OLAP cubes should store the finest grain of data (atomic data)**, in case we need to drill-down to the lowest level, e.g. country -> city -> district -> street, etc.
- **Slice**: Reduce N dimensions to N-1 dimensions by restricting one dimension to a single value.
  * e.g. `month = 'March'`
- **Dice**: Same dimensions but computing a sub-cube by restricting some of the values of the dimensions.
  * e.g. `month in ('March, 'Feb'] and movie in ['Avatar', 'Batman'] and branch = 'NY'`

OLAP cube **query optimatization**:
- Business users will typically want to slice, dice, roll up , and drill down all the time
- Each sub combination will potentially go through all the facts table (suboptimal)
- The **`GROUP BY CUBE (movie, branch, month)`** will make **one pass through** the facts table and will aggregate all possible combinations of groupings, of length 0, 1, 2, 3; e.g.
  * total revenue
  * revenue by movie; revenue by month; revenue by branch
  * revenue by movie, branch; revenue by branch, month; revenue by movie, month
  * revenue by movie, branch, revenue.
- Saving/materializing the output of the CUBE operation and using it is usually enough to answer all forthcoming aggregations from business uesrs w/o having to process the whole facts table again.

#### GROUPING SETS

The [`GROUPING SETS`](http://www.sqlservertutorial.net/sql-server-basics/sql-server-grouping-sets/) defines multiple grouping sets in the same query.
```
SELECT
    column1,
    column2,
    aggregate_function (column3)
FROM
    table_name
GROUP BY
    GROUPING SETS (
        (column1, column2),
        (column1),
        (column2),
        ()
);
```
As you can see, the query produces the same result as the one that uses the `UNION ALL` operator. However, this query is much more readable and of course more efficient.

e.g.
```
SELECT d.month AS month, s.country AS country, sum(fs.sales_amount) AS revenue
FROM factsales AS fs
JOIN dimstore AS s on s.store_key = fs.store_key
JOIN dimdate AS d on d.date_key = fs.date_key
GROUP BY grouping sets ((), month, country, (month, country))
ORDER BY month, country, revenue desc
```

#### CUBE
The `CUBE` is a subclause of the `GROUP BY` clause that allows you to [generate multiple grouping sets](http://www.sqlservertutorial.net/sql-server-basics/sql-server-cube/).
```
SELECT
    d1,
    d2,
    d3,
    aggregate_function (c4)
FROM
    table_name
GROUP BY
    CUBE (d1, d2, d3);
```
In this syntax, the `CUBE` generates all possible grouping sets based on the dimension columns d1, d2, and d3 that you specify in the `CUBE` clause.
The above query returns the same result set as the following query, which uses the `GROUPING SETS`:
```
SELECT
    d1,
    d2,
    d3,
    aggregate_function (c4)
FROM
    table_name
GROUP BY
    GROUPING SETS (
        (d1,d2,d3),
        (d1,d2),
        (d1,d3),
        (d2,d3),
        (d1),
        (d2),
        (d3),
        ()
     );
```

If you have **N** dimension columns specified in the `CUBE`, you will have **2N** grouping sets.

Also, `None` here is expressive; so one usually cleans and drops any `None`s before doing a cube.

## Delivering the analytics to users
Data is available:
- in an understandable & performant dimensional model
- with *conformed dimensions* or separate *data marts*
- for users to report and visualize
  * by interacting directly with the model
  * or in most cases, through a BI application

#### OLAP Cube technology

Approach 1: **Pre-aggregate** the OLAP cubes and saves them on a special purpose non-relational database (**MOLAP**)
- go buy an OLAP server: has an internal structure optimized for serving OLAP cubes; this is more traditional.

Approach 2: Compute the OLAP cubes **on the fly** from the existing relational database where the dimensional model resides (**ROLAP**)

**Column format in ROLAP**:
- Use a postgresql with a **columnar table** extension
- Load a dataset in a normal table
- Load the same dataset in a columnar table
- Compare the performance of the fact-aggregating query performance in both tables.

e.g. Columnar store for analytics with Postgres, developed by Citus Data - [cstore_fdw](https://github.com/citusdata/cstore_fdw)
```
-- load extension first time after install
CREATE EXTENSION cstore_fdw;

-- create server object
CREATE SERVER cstore_server FOREIGN DATA WRAPPER cstore_fdw;

-- create foreign table
DROP FOREIGN TABLE IF EXISTS customer_reviews_col;

-- CREATE FOREIGN TABLE

-- leave code below as is
SERVER cstore_server
OPTIONS(compression 'pglz');
```

**References**:
- [The Data Warehouse Toolkit: The Complete Guide to Dimensional Modeling (Kimball)](https://www.amazon.com/Data-Warehouse-Toolkit-Complete-Dimensional/dp/0471200247)
- [Building the Data Warehouse (Inmon)](https://www.amazon.com/Building-Data-Warehouse-W-Inmon/dp/0764599445)
- [Building a Data Warehouse: With Examples in SQL Server (Rainardi)](https://www.amazon.com/Building-Data-Warehouse-Examples-Experts/dp/1590599314)
