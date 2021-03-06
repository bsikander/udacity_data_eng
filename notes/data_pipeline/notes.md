#### Data Pipelines
- Series of steps to transform data
- Data validation can be done to make sure that quality is ok and data is accurate and correct.
- Data validation should be automated but can be done manually

#### DAGs
- Data pipelines are well expressed as DAGs (https://www.youtube.com/watch?v=YcahqfpcDeA)
- No cycles and edges are in one direction

#### Apache Airflow
"Airflow is a platform to programmatically author, schedule and monitor workflows. Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative."


![alt text](https://github.com/bsikander/udacity_data_eng/blob/master/notes/data_pipeline/Screen%20Shot%202020-05-08%20at%2017.18.18.png)

#### Operators
Operators define the atomic steps of work that make up a DAG. Airflow comes with many Operators that can perform common operations. Here are a handful of common ones:

PythonOperator
PostgresOperator
RedshiftToS3Operator
S3ToRedshiftOperator
BashOperator
SimpleHttpOperator
Sensor

#### Task Dependencies
In Airflow DAGs:

Nodes = Tasks
Edges = Ordering and dependencies between tasks
Task dependencies can be described programmatically in Airflow using >> and <<
```
a >> b means a comes before b
a << b means a comes after b
```
Tasks dependencies can also be set with “set_downstream” and “set_upstream”
```
a.set_downstream(b) means a comes before b
a.set_upstream(b) means a comes after b
```

#### Data Lineage
Definition
The data lineage of a dataset describes the discrete steps involved in the creation, movement, and calculation of that dataset.

Why is Data Lineage important?
- Instilling Confidence: Being able to describe the data lineage of a particular dataset or analysis will build confidence in data consumers (engineers, analysts, data scientists, etc.) that our data pipeline is creating meaningful results using the correct datasets. If the data lineage is unclear, its less likely that the data consumers will trust or use the data.
- Defining Metrics: Another major benefit of surfacing data lineage is that it allows everyone in the organization to agree on the definition of how a particular metric is calculated.
- Debugging: Data lineage helps data engineers track down the root of errors when they occur. If each step of the data movement and transformation process is well described, it's easy to find problems when they occur.

#### Data Quality
https://www.youtube.com/watch?v=-ravmjI7RYk

- Examples of Data Quality Requirements
- Data must be a certain size
- Data must be accurate to some margin of error
- Data must arrive within a given timeframe from the start of execution
- Pipelines must run on a particular schedule
- Data must not contain any sensitive information

#### Airflow Plugins
Airflow was built with the intention of allowing its users to extend and customize its functionality through plugins. The most common types of user-created plugins for Airflow are Operators and Hooks. These plugins make DAGs reusable and simpler to maintain.

To create custom operator, follow the steps:

Identify Operators that perform similar functions and can be consolidated
Define a new Operator in the plugins folder
Replace the original Operators with your new custom one, re-parameterize, and instantiate them.

#### Other Pipeline Orchestrators
Here are some resources to explore other data pipeline orchestrators.

This [Github link](https://github.com/pditommaso/awesome-pipeline) contains perhaps way too many examples, but it shows a nice list of other pipeline orchestrators.

You can also check out these pages to see how Airflow's components can be generalized to the elements of other pipeline orchestrators.

- [Quora page](https://www.quora.com/Which-is-a-better-data-pipeline-scheduling-platform-Airflow-or-Luigi)

- [Github link](https://xunnanxu.github.io/2018/04/13/Workflow-Processing-Engine-Overview-2018-Airflow-vs-Azkaban-vs-Conductor-vs-Oozie-vs-Amazon-Step-Functions/)

- [Medium post](https://medium.com/@cyrusv/luigi-vs-airflow-vs-zope-wfmc-comparison-of-open-source-workflow-engines-de5209e6dac1)
