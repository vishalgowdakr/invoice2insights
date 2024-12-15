run:
	source backend/venv/bin/activate &
	superset run -p 8088 --with-threads --reload --debugger &
	python backend/api/manage.py runserver &
	cd frontend && npm run start &
