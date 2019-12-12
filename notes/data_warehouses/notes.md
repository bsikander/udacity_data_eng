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
- Record business events, like an order, a phone call, a book review
- Fact table columns record events in quantifiable **metrics** like quantity of an item, duration of a call, a book rating

#### Dimensional tables
- Record the context of the business events, e.g. who, what, where, why...
- Dimension table columns contain **attributes** like the store at which an item is purchased, or the customer who made the call, etc. 
