clean:
	docker system prune --volumes

up:
	docker-compose up --remove-orphans --force-recreate --build postgres

down:
	docker-compose down -v
