start: 
	uvicorn app.main:app --reload
# app.main tells Uvicorn to look inside the app folder for the main.py file.
# :app specifies that within main.py, you are looking for the app FastAPI instance.

# only runs prod command after dbsetup finishes
prod: dbsetup
	uvicorn app.main:app --host 0.0.0.0 --port 8000

dbsetup: 
	alembic upgrade head

deps:
	pip freeze > requirements.txt

compose:
	docker compose down -v && docker compose up --build

clear-cache:
	find . -name "__pycache__" -type d -exec rm -rf {} +