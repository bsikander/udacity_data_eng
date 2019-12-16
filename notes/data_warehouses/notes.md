# Data Warehouse

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

### Hybrid Bus & CIF
