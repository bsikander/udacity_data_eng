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
➜  data_modeling git:(master) make install
```

see output here: https://gist.github.com/pwen/dba568665552fdde63b50b7e3860a5ef

#### spin up postgres inside docker
```
➜  data_modeling git:(master) make down
➜  data_modeling git:(master) make up
```

see output here: https://gist.github.com/pwen/ca8cb2255ab3ff5d8a32127f8a0e1cab

### run the program

```
➜  data_modeling git:(master) python main.py --refresh --run-test
```

see output here: https://gist.github.com/pwen/847233b4237d2a4c11c93c6482b6bb15

## design notes

TODO: Add more cmments & make sure they are used effectively; each function has a docstring.
