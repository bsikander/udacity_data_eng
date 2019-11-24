### requirement
- python 3.6
- [optional] docker & docker-compose (for postgres setup)

### setup

*libraries*
> pipenv install
or
> pip install -r requirements.txt
> pip install -r requirements-text.txt

*spin up docker contianer for pg*
> make down
> make up

you should get something like this: `setup.output`

### run the program
> python main.py --refresh --run-test

see an example output: `main.output`
