import pytest

headers = None  # Global variable
login_data = {
    "email": "seed_user@email.com",
    "password": "password123",
}
new_playlist_data = {
    "name": "New Private Playlist",
    "private": True,
}
updated_playlist_data = {
    "name": "updated_name",
    "private": False,
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


# Create playlist
async def test_create_playlist(client):
    await get_token(client)
    response = await client.post("/playlist", json=new_playlist_data, headers=headers)
    json_response = response.json()

    assert response.status_code == 201
    assert json_response["name"] == new_playlist_data["name"]
    assert json_response["private"] == new_playlist_data["private"]
    assert json_response["owner_id"] == 1  # user id from seed


async def test_get_user_playlist_as_owner(client):
    response = await client.get("/playlist/from-user/1", headers=headers)
    json_response = response.json()

    assert response.status_code == 200

    assert len(json_response) == 2

    assert json_response[0]["name"] == "Seed Playlist"
    assert json_response[0]["private"] == False

    assert json_response[1]["name"] == new_playlist_data["name"]
    assert json_response[1]["private"] == new_playlist_data["private"]


async def test_get_user_playlist_as_random(client):
    response = await client.get("/playlist/from-user/1")
    json_response = response.json()

    assert response.status_code == 200

    assert len(json_response) == 1

    assert json_response[0]["name"] == "Seed Playlist"
    assert json_response[0]["private"] == False


# async def test_add_music_to_playlist(client):
#     # first add a music
#     new_music_data = {
#         "title": "Imagine",
#         "artist": "John Lennon",
#         "link": "https://example.com/imagine",
#     }
#     create_music_response = await client.post(
#         "/music", json=new_music_data, headers=headers
#     )
#     assert create_music_response.status_code == 201

#     music_json_response = create_music_response.json()
#     assert music_json_response["title"] == new_music_data["title"]
#     assert music_json_response["artist"] == new_music_data["artist"]
#     assert music_json_response["link"] == new_music_data["link"]

#     # add new music to seed playlist
#     playlist_id = 1  # seed playlist id
#     new_music_id = music_json_response["id"]
#     add_music_response = await client.post(
#         f"/playlist/{playlist_id}/add-music/{new_music_id}", headers=headers
#     )
#     add_music_json_response = add_music_response.json()

# assert add_music_response.status_code == 201
# assert add_music_json_response["id"] == music_json_response["id"]
# assert add_music_json_response["artist"] == music_json_response["artist"]
# assert add_music_json_response["title"] == music_json_response["title"]
# assert add_music_json_response["link"] == music_json_response["link"]
# assert add_music_json_response["added_by"] == music_json_response["added_by"]


async def test_get_musics_from_public_playlist_as_unknown(client):
    playlist_id = 1  # seed playlist id that should have the seed music
    response = await client.get(f"/playlist/{playlist_id}/musics")
    json_response = response.json()

    assert response.status_code == 200

    assert json_response["name"] == "Seed Playlist"
    assert json_response["private"] == False
    assert json_response["owner_id"] == 1  # seed user id
    assert len(json_response["musics"]) == 1
    assert json_response["musics"] == [
        {
            "artist": "Seed Artist",
            "link": "https://example.com/seed",
            "title": "Seed Song",
        }
    ]


async def test_get_musics_from_private_playlist_as_unknown(client):
    playlist_id = 2  # private playlist created
    response = await client.get(f"/playlist/{playlist_id}/musics")

    assert response.status_code == 401


async def test_get_musics_from_private_playlist_as_owner(client):
    playlist_id = 2  # private playlist created
    response = await client.get(f"/playlist/{playlist_id}/musics", headers=headers)
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == new_playlist_data["name"]
    assert json_response["private"] == new_playlist_data["private"] == True
    assert json_response["owner_id"] == 1  # seed user id
    assert json_response["id"] == 2  # second playlist created
    assert len(json_response["musics"]) == 0


async def test_update_playlist_as_unknown(client):
    playlist_id = 2  # private playlist created
    updated_data = {
        "name": "updated_name",
        "private": False,
    }
    response = await client.put(
        f"/playlist/{playlist_id}",
        json=updated_data,
        headers=headers,
    )
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == updated_data["name"]
    assert json_response["private"] == updated_data["private"]
    assert json_response["id"] == playlist_id


async def test_delete_playlist(client):
    playlist_id = 2  # private playlist created
    response = await client.delete(f"/playlist/{playlist_id}", headers=headers)
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == updated_playlist_data["name"]
    assert json_response["private"] == updated_playlist_data["private"]
    # id 1 from the seed user, used to create the new playlist
    assert json_response["owner_id"] == 1  # seed user
