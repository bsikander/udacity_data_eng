## instructions

### requirement
- python 3.6
- [optional] docker & docker-compose (for postgres setup)

### setup

#### install dependencies
```
➜  data_modeling git:(master) pipenv install
```

or
```
➜  data_modeling git:(master) pip install -r requirements.txt
➜  data_modeling git:(master) pip install -r requirements-dev.txt
```

#### spin up postgres inside docker
```
➜  data_modeling git:(master) make down
➜  data_modeling git:(master) make up
```

you should get something like this: `setup.output`

### run the program

```
➜  data_modeling git:(master) python main.py --refresh --run-test
```

see an example output: `main.output`

## design notes

TODO: Add more cmments & make sure they are used effectively; each function has a docstring.
