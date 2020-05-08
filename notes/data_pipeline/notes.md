#### Data Pipelines
- Series of steps to transform data
- Data validation can be done to make sure that quality is ok and data is accurate and correct.
- Data validation should be automated but can be done manually

#### DAGs
- Data pipelines are well expressed as DAGs (https://www.youtube.com/watch?v=YcahqfpcDeA)
- No cycles and edges are in one direction

#### Apache Airflow
"Airflow is a platform to programmatically author, schedule and monitor workflows. Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. The airflow scheduler executes your tasks on an array of workers while following the specified dependencies. Rich command line utilities make performing complex surgeries on DAGs a snap. The rich user interface makes it easy to visualize pipelines running in production, monitor progress, and troubleshoot issues when needed. When workflows are defined as code, they become more maintainable, versionable, testable, and collaborative."
