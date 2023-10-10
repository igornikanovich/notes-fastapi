cleanup:
	poetry install

start:
	docker-compose -f docker-compose.local.yml up -d --build

down:
	docker-compose -f docker-compose.local.yml down

logs:
	docker-compose -f docker-compose.local.yml logs -f web
