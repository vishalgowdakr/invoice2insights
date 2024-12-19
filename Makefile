SHELL := /bin/bash

run:
	@echo "Loading environment variables from .env..."
	SUPERSET_SECRET_KEY=d+zT49TdTrEIcFn4e0ZsbQPClmKiXwpGJKOg/So8bfhMKeWJgc3z8r+F FLASK_APP=superset SUPERSET_CONFIG_PATH=/home/vishal/personal/invoice2insights/backend/superset_config.py superset run -p 8088 --with-threads --reload --debugger & \
	npm --prefix frontend run start & \



stop:
	@echo "Stopping all services..."
	pkill node
	pkill superset
	pkill python
	pkill python
