import pytest

headers = None  # Global variable
login_data = {
    "email": "seed_user@email.com",
    "password": "password123",
}
new_music_data = {
    "title": "Imagine",
    "artist": "John Lennon",
    "link": "https://example.com/imagine",
}
updated_music_data = {
    "title": "updated title",
    "artist": "updated artist",
    "link": "https://example.com/link",
}


async def get_token(client):
    global headers

    # 1. Login with seeded account and get a token
    login_response = await client.post(
        "/users/login",
        json=login_data,
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    assert token  # Ensure token exists

    # saves token in header at global variable
    headers = {"Authorization": f"Bearer {token}"}


async def test_get_all_music(client):
    await get_token(client)

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
    response = await client.post("/music", json=new_music_data, headers=headers)
    assert response.status_code == 201

    json_response = response.json()
    assert json_response["title"] == new_music_data["title"]
    assert json_response["artist"] == new_music_data["artist"]
    assert json_response["link"] == new_music_data["link"]


async def test_get_music_added_by_user(client):
    response = await client.get("/music/1")
    json_response = response.json()

    assert response.status_code == 200
    # Expect seed + added music
    assert len(json_response) == 2

    assert json_response[0]["title"] == "Seed Song"
    assert json_response[0]["artist"] == "Seed Artist"
    assert json_response[0]["link"] == "https://example.com/seed"

    assert json_response[1]["title"] == "Imagine"
    assert json_response[1]["artist"] == "John Lennon"
    assert json_response[1]["link"] == "https://example.com/imagine"


async def test_update_added_music(client):
    response = await client.put("/music/2", json=updated_music_data, headers=headers)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["title"] == updated_music_data["title"]
    assert response_json["artist"] == updated_music_data["artist"]
    assert response_json["link"] == updated_music_data["link"]


async def test_delete_music(client):
    response = await client.delete("/music/2", headers=headers)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["title"] == updated_music_data["title"]
    assert response_json["artist"] == updated_music_data["artist"]
    assert response_json["link"] == updated_music_data["link"]
