format:
	pipenv run black .

lint:
	pipenv run pre-commit run -a
