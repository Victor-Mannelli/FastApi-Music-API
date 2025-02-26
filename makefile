start: 
	uvicorn api.main:app --reload
# app.main tells Uvicorn to look inside the app folder for the main.py file.
# :app specifies that within main.py, you are looking for the app FastAPI instance.

dbsetup:
	alembic upgrade head

gp:
	pip freeze > requirements.txt & git push