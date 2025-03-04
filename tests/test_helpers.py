seed_user = {
    "id": 1,
    "username": "seed_user",
    "email": "seed_user@email.com",
    "password": "$2a$12$TDJFaiwRleVEBYnvd/CVbuGIjbu/zVhImLgXuGlQgDrV8a734kK.2",
}
seed_music_in_playlist = {
    "id": 1,
    "title": "Seed Song",
    "artist": "Seed Artist",
    "link": "https://example.com/seed",
    "added_by": seed_user["id"],
}
seed_music_left_out = {
    "id": 2,
    "title": "When Orange is the Sky",
    "artist": "Fabrizio Paterlini",
    "link": "https://open.spotify.com/track/67u3IsSI1tmEsF7jZWPQWc?si=cbaf4b10c6de485c",
    "added_by": seed_user["id"],
}
public_seed_playlist = {
    "id": 1,
    "name": "Seed Playlist 1",
    "private": False,
    "owner_id": seed_user["id"],
    "musics": seed_music_in_playlist,
}
private_seed_playlist = {
    "id": 2,
    "name": "Seed Playlist 2",
    "private": True,
    "owner_id": seed_user["id"],
    "musics": seed_music_in_playlist,
}


async def get_token(client):
    login_data = {
        "email": "seed_user@email.com",
        "password": "password123",
    }

    # 1. Login with seeded account and get a token
    login_response = await client.post(
        "/users/login",
        json=login_data,
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    assert token  # Ensure token exists

    # saves token in header at global variable
    return {"Authorization": f"Bearer {token}"}
