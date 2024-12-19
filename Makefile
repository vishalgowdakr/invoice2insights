SHELL := /bin/bash

run:
	@echo "Loading environment variables from .env..."
	SUPERSET_SECRET_KEY=d+zT49TdTrEIcFn4e0ZsbQPClmKiXwpGJKOg/So8bfhMKeWJgc3z8r+F FLASK_APP=superset SUPERSET_CONFIG_PATH=/home/vishalgowdakr/college/invoice2insights/backend/superset_config.py superset run -p 8088 --with-threads --reload --debugger & \
	npm --prefix frontend run start & \
	GOOGLE_API_KEY=AIzaSyCBIl7sHo6F2gS8IXnPpsw2Pq97s1gqptk python backend/api/manage.py runserver


stop:
	@echo "Stopping all services..."
	pkill node
	pkill superset
	pkill python
	pkill python
