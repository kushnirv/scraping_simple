sh:
	docker-compose run --rm app sh
init_db:
	docker-compose run --rm app python init_db.py


