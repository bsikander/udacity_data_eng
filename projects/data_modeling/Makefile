clean:
	docker system prune --volumes

up:
	docker-compose up

down:
	docker-compose down --remove-orphans --volumes

connect:
	docker exec -it data_modeling_postgres_1 psql -U student sparkifydb

regen-reqs:
	rm -f requirements*.txt
	pipenv lock -r --dev > requirements-dev.txt
	pipenv lock -r > requirements.txt
