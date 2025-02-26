from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_all_music(client):
  response = client.get("/music/all")
  assert response.status_code == 200
  assert response.json() == []  # Expect an empty list since no music is added yet
    
def test_add_music(client):
  # 1. Create a user
  user_data = {
    "username": "your_username",
    "email": "test@example.com", 
    "password": "password123"
  }
  client.post("/users", json=user_data)

  # 2. Login and get a token
  login_response = client.post("/login", data={"email": user_data["email"], "password": user_data["password"]})
  assert login_response.status_code == 200
  
  token = login_response.json()["access_token"]
  headers = {"Authorization": f"Bearer {token}"}
  
  music_data = {
    "title": "Imagine",
    "artist": "John Lennon",
    "link": "https://example.com/imagine"
  }
  
  response = client.post("/music", json=music_data, headers=headers)
  assert response.status_code == 201

  json_response = response.json()
  assert json_response["title"] == music_data["title"]
  assert json_response["artist"] == music_data["artist"]
  assert json_response["link"] == music_data["link"]
    
def test_get_all_music_after_adding(client):
  response = client.get("/music/all")
  assert response.status_code == 200
  assert len(response.json()) == 1  # Now we should have one music in the database
