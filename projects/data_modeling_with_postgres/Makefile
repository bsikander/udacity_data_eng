clean:
	docker system prune --volumes

up:
	docker-compose up

down:
	docker-compose down --remove-orphans --volumes

connect:
	docker exec -it data_modeling_with_postgres_postgres_1 psql -U student studentdb
