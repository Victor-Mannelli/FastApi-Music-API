from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_musics():
  response = client.get("/music/all")
  assert response.status_code == 200
  assert isinstance(response.json(), list)  # Ensure the response is a list of musics
  
