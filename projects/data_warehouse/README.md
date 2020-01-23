## requirement
- python 3.6

## set up
#### install dependencies
```
➜  pipenv install
➜  pipenv shell
```

#### launch an AWS Redshift
and update the `dwh.cfg` with Redshift cluster configuration and IAM role associated with the cluster.


## run the program
```
➜  python create_tables.py
➜  python etl.py
```
