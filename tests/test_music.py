from tests.test_helpers import (
    seed_music_in_playlist,
    seed_music_left_out,
    seed_user,
    get_token,
)


async def test_get_all_music(client):
    response = await client.get("/music/all")
    json_response = response.json()

    assert response.status_code == 200
    # Expect list with one music from seed
    assert len(json_response) == 2
    # Check if the seed music is in the response JSON
    assert json_response[0]["title"] == seed_music_in_playlist["title"]
    assert json_response[0]["artist"] == seed_music_in_playlist["artist"]
    assert json_response[0]["link"] == seed_music_in_playlist["link"]
    assert json_response[1]["title"] == seed_music_left_out["title"]
    assert json_response[1]["artist"] == seed_music_left_out["artist"]
    assert json_response[1]["link"] == seed_music_left_out["link"]


async def test_add_music(client):
    headers = await get_token(client)
    new_music_data = {
        "title": "Imagine",
        "artist": "John Lennon",
        "link": "https://example.com/imagine",
    }
    response = await client.post("/music", json=new_music_data, headers=headers)
    json_response = response.json()

    assert response.status_code == 201
    assert json_response["id"]
    assert json_response["added_by"] == seed_user["id"]
    assert json_response["title"] == new_music_data["title"]
    assert json_response["artist"] == new_music_data["artist"]
    assert json_response["link"] == new_music_data["link"]


async def test_get_music_list_added_by_user(client):
    response = await client.get(f"/music/from-user/{seed_user['id']}")
    json_response = response.json()

    assert response.status_code == 200

    assert len(json_response) == 2
    assert json_response[0]["title"] == seed_music_in_playlist["title"]
    assert json_response[0]["artist"] == seed_music_in_playlist["artist"]
    assert json_response[0]["link"] == seed_music_in_playlist["link"]
    assert json_response[1]["title"] == seed_music_left_out["title"]
    assert json_response[1]["artist"] == seed_music_left_out["artist"]
    assert json_response[1]["link"] == seed_music_left_out["link"]


async def test_update_music(client):
    updated_music_data = {
        "title": "updated title",
        "artist": "updated artist",
        "link": "https://example.com/link",
    }
    headers = await get_token(client)
    response = await client.put(
        f"/music/{seed_music_in_playlist['id']}",
        json=updated_music_data,
        headers=headers,
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["title"] == updated_music_data["title"]
    assert response_json["artist"] == updated_music_data["artist"]
    assert response_json["link"] == updated_music_data["link"]


async def test_delete_music(client):
    headers = await get_token(client)
    response = await client.delete(
        f"/music/{seed_music_in_playlist['id']}", headers=headers
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["title"] == seed_music_in_playlist["title"]
    assert response_json["artist"] == seed_music_in_playlist["artist"]
    assert response_json["link"] == seed_music_in_playlist["link"]
