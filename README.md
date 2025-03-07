# 🎵 FastAPI Music Playlist API

This project is a structured backend built with FastAPI, following a well-organized architecture inspired by NestJS, but adapted to Python best practices. The goal was to apply the same concepts used in JavaScript development while learning how to properly build a backend using modern Python technologies.

## 🚀 Technologies Used

- FastAPI - Modern, fast web framework for building APIs <br/>
- SQLAlchemy - ORM for database management <br/>
- Alembic - Database migrations <br/>
- Pydantic - Data validation and serialization <br/>
- JWT (JSON Web Tokens) - Authentication <br/>
- Async SQLAlchemy with PostgreSQL - Efficient database interactions <br/>
- Pytest - Unit testing framework <br/>
- Docker - Containerized deployment <br/>

## 🛠️ Installation & Setup

1️⃣ Clone the Repository

```bash 
git clone https://github.com/Victor-Mannelli/Python-Music-API.git
# and
cd fastapi-music-playlist
```

2️⃣ Create Virtual Environment

```bash 
python -m venv venv
# or
source venv/bin/activate // On Windows use: venv\Scripts\activate
```

3️⃣ Install Dependencies

```bash 
pip install -r requirements.txt
```

4️⃣ Set Up Environment Variables

Create a .env file and use the .env.public to fill all that's needed!
Be carefull to check if your .env file is being correctly seen by the docker compose by running the command:

```bash
docker compose config
```

5️⃣ Run the docker compose to create the api and database containers

```bash
docker compose up --build
# or 
make compose
```

# Now the containers should be running!

The API will be available at: http://localhost:8000

# 📖 API Endpoints

While running the app you can check the end point documentation at http://localhost:8000/docs

# 🧪 Running Tests

To run the test suite, use:

```bash
pytest
```

# 💡 Lessons Learned

- SQLAlchemy and Alembic provide a powerful ORM and migration system
- Pydantic is a great tool for request validation and response serialization
- Dependency injection in FastAPI is different but just as powerful as NestJS decorators
- Python imports can be confusing and response type can change the actual response body
- Changing from Sync to Async SqlAlchemy request setup can change the whole project 
- Greenlet errors are really annoying

# 📜 License

This project is licensed under the MIT License. Feel free to use and modify it!

# ✨ Contributions & Feedback

If you have any suggestions, feel free to submit an issue or pull request. Contributions are always welcome! 🎉
