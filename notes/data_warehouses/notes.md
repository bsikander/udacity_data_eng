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
