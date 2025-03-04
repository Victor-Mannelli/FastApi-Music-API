from tests.test_helpers import get_token, seed_user


# registration
async def test_create_user(client):
    new_user_data = {
        "username": "your_username",
        "email": "user@email.com",
        "password": "password123",
    }

    response = await client.post("/users", json=new_user_data)
    create_user_response = response.json()

    # Ensures user was created successfully
    assert response.status_code == 201
    assert create_user_response["username"] == new_user_data["username"]
    assert create_user_response["email"] == new_user_data["email"]


# login and store token
async def test_login(client):
    # headers = await get_token()
    login_data = {
        "email": "seed_user@email.com",
        "password": "password123",
    }
    # 1. Login with seeded account and get a token
    login_response = await client.post(
        "/users/login",
        json=login_data,
    )
    json_login_response = login_response.json()

    assert login_response.status_code == 200
    assert json_login_response["access_token"]  # Ensure token exists
    assert json_login_response["token_type"] == "bearer"


# user health check and data
async def test_get_me(client):
    headers = await get_token(client)
    response = await client.get("/users/me", headers=headers)
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["username"] == seed_user["username"]
    assert json_response["email"] == seed_user["email"]
    assert isinstance(json_response["id"], int)


# find all
async def test_get_users(client):
    response = await client.get("/users")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response == [
        {
            "id": 1,
            "username": seed_user["username"],
            "email": seed_user["email"],
        }
    ]


# find one
async def test_get_user_by_id(client):
    response = await client.get("/users/1")
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["username"] == seed_user["username"]
    assert json_response["email"] == seed_user["email"]


# update
async def test_update_user(client):
    headers = await get_token(client)
    updated_user_data = {
        "username": "updated_username",
        "email": "updated_email@email.com",
    }
    response = await client.put(
        f"/users/{seed_user['id']}", json=updated_user_data, headers=headers
    )
    json_response = response.json()

    assert response.status_code == 200
    assert json_response["username"] == updated_user_data["username"]
    assert json_response["email"] == updated_user_data["email"]


# delete
async def test_delete_user(client):
    headers = await get_token(client)
    response = await client.delete(f"/users/{seed_user['id']}", headers=headers)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["username"] == seed_user["username"]
    assert response_json["email"] == seed_user["email"]
