from tests.test_helpers import (
    seed_music_in_playlist,
    seed_music_left_out,
    private_seed_playlist,
    public_seed_playlist,
    seed_user,
    get_token,
)


async def test_create_playlist(client):
    new_playlist_data = {
        "name": "New Private Playlist",
        "private": True,
    }
    headers = await get_token(client)
    response = await client.post("/playlist", json=new_playlist_data, headers=headers)
    json_response = response.json()

    assert response.status_code == 201
    assert json_response["id"]
    assert json_response["name"] == new_playlist_data["name"]
    assert json_response["private"] == new_playlist_data["private"]
    assert json_response["owner_id"] == seed_user["id"]


async def test_get_user_playlists_as_owner(client):
    headers = await get_token(client)
    response = await client.get(
        f"/playlist/from-user/{seed_user['id']}",
        headers=headers,
    )
    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response) == 2
    assert json_response[0]["name"] == public_seed_playlist["name"]
    assert json_response[0]["private"] == public_seed_playlist["private"]
    assert json_response[1]["name"] == private_seed_playlist["name"]
    assert json_response[1]["private"] == private_seed_playlist["private"]


async def test_get_user_playlists_as_random(client):
    response = await client.get(
        f"/playlist/from-user/{seed_user['id']}",
    )
    json_response = response.json()

    assert response.status_code == 200
    assert len(json_response) == 1
    assert json_response[0]["name"] == public_seed_playlist["name"]
    assert json_response[0]["private"] == public_seed_playlist["private"]


async def test_add_left_out_music_to_playlist(client):
    headers = await get_token(client)
    response = await client.post(
        f"/playlist/{public_seed_playlist['id']}/add-music/{seed_music_left_out['id']}",
        headers=headers,
    )
    json_response = response.json()

    assert response.status_code == 201
    assert json_response["id"] == seed_music_left_out["id"]
    assert json_response["artist"] == seed_music_left_out["artist"]
    assert json_response["title"] == seed_music_left_out["title"]
    assert json_response["link"] == seed_music_left_out["link"]
    assert json_response["added_by"] == seed_music_left_out["added_by"]


async def test_add_already_added_music_to_playlist(client):
    headers = await get_token(client)
    response = await client.post(
        f"/playlist/{public_seed_playlist['id']}/add-music/{seed_music_in_playlist['id']}",
        headers=headers,
    )
    assert response.status_code == 409


async def test_get_musics_from_public_playlist_as_unknown(client):
    response = await client.get(f"/playlist/{public_seed_playlist['id']}/musics")
    json_response = response.json()

    assert response.status_code == 200

    assert json_response["name"] == public_seed_playlist["name"]
    assert json_response["private"] == public_seed_playlist["private"]
    assert json_response["owner_id"] == public_seed_playlist["owner_id"]
    assert len(json_response["musics"]) == 1
    assert json_response["musics"] == [
        {
            "id": seed_music_in_playlist["id"],
            "title": seed_music_in_playlist["title"],
            "artist": seed_music_in_playlist["artist"],
            "link": seed_music_in_playlist["link"],
            "added_by": seed_music_in_playlist["added_by"],
        }
    ]


async def test_get_musics_from_private_playlist_as_unknown(client):
    response = await client.get(f"/playlist/{private_seed_playlist['id']}/musics")

    assert response.status_code == 401


async def test_get_musics_from_private_playlist_as_owner(client):
    headers = await get_token(client)
    response = await client.get(
        f"/playlist/{private_seed_playlist['id']}/musics",
        headers=headers,
    )
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == private_seed_playlist["name"]
    assert json_response["private"] == private_seed_playlist["private"] == True
    assert json_response["owner_id"] == private_seed_playlist["owner_id"]
    assert json_response["id"] == private_seed_playlist["id"]
    assert json_response["musics"] == [seed_music_in_playlist]


async def test_update_playlist(client):
    headers = await get_token(client)
    updated_data = {
        "name": "updated_name",
        "private": False,
    }
    response = await client.put(
        f"/playlist/{private_seed_playlist['id']}",
        json=updated_data,
        headers=headers,
    )
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == updated_data["name"]
    assert json_response["private"] == updated_data["private"]
    assert json_response["id"] == private_seed_playlist["id"]


async def test_delete_playlist(client):
    headers = await get_token(client)
    response = await client.delete(
        f"/playlist/{private_seed_playlist['id']}",
        headers=headers,
    )
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["name"] == private_seed_playlist["name"]
    assert json_response["private"] == private_seed_playlist["private"]
    assert json_response["owner_id"] == private_seed_playlist["owner_id"]


async def test_remove_music_from_playlist(client):
    headers = await get_token(client)
    response = await client.put(
        f"/playlist/{public_seed_playlist['id']}/remove-music/{seed_music_in_playlist['id']}",
        headers=headers,
    )
    json_response = response.json()

    response.status_code == 200
    assert json_response["id"] == seed_music_in_playlist["id"]
    assert json_response["title"] == seed_music_in_playlist["title"]
    assert json_response["artist"] == seed_music_in_playlist["artist"]
    assert json_response["link"] == seed_music_in_playlist["link"]
    assert json_response["added_by"] == seed_music_in_playlist["added_by"]
