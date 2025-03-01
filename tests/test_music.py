import httpx
import pytest


async def test_get_all_music(client):
    response = await client.get("/music/all")
    assert response.status_code == 200
    assert response.json() == []  # Expect an empty list since no music is added yet


async def test_add_music(client):
    # 1. Create a user
    user_data = {
        "username": "your_username",
        "email": "test@example.com",
        "password": "password123",
    }
    create_user_response = await client.post("/users", json=user_data)
    assert (
        create_user_response.status_code == 201
    )  # Ensure user is created successfully

    # 2. Login and get a token
    login_data = {
        "email": "test@example.com",
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


async def test_get_all_music_after_adding(client):
    response = await client.get("/music/all")
    assert response.status_code == 200
    assert len(response.json()) == 1  # Now we should have one music in the database
