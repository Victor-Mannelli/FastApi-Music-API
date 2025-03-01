import pytest


async def test_get_all_music(client):
    response = await client.get("/music/all")
    assert response.status_code == 200

    json_response = response.json()

    # Expect list with one music from seed
    assert len(json_response) == 1

    # Check if the expected music is in the response JSON
    assert json_response[0]["title"] == "Seed Song"
    assert json_response[0]["artist"] == "Seed Artist"
    assert json_response[0]["link"] == "https://example.com/seed"


async def test_add_music(client):
    # 1. Login with seeded account and get a token
    login_data = {
        "email": "seed_user@email.com",
        "password": "password123",
    }
    login_response = await client.post(
        "/users/login",
        json=login_data,
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    assert token  # Ensure token exists

    headers = {"Authorization": f"Bearer {token}"}

    music_data = {
        "title": "Imagine",
        "artist": "John Lennon",
        "link": "https://example.com/imagine",
    }

    response = await client.post("/music", json=music_data, headers=headers)
    assert response.status_code == 201

    json_response = response.json()
    assert json_response["title"] == music_data["title"]
    assert json_response["artist"] == music_data["artist"]
    assert json_response["link"] == music_data["link"]


async def test_get_music_added_by_user(client):
    response = await client.get("/music/1")
    assert response.status_code == 200
    json_response = response.json()
    # Expect seed + added music
    assert len(json_response) == 2
    print(json_response)
    assert json_response[0]["title"] == "Seed Song"
    assert json_response[0]["artist"] == "Seed Artist"
    assert json_response[0]["link"] == "https://example.com/seed"
    assert json_response[1]["title"] == "Imagine"
    assert json_response[1]["artist"] == "John Lennon"
    assert json_response[1]["link"] == "https://example.com/imagine"
