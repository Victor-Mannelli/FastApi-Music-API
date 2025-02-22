start: 
	uvicorn main:app --reload
dbsetup:
	alembic upgrade head