import pytest

new_user_data = {
    "username": "your_username",
    "email": "user@email.com",
    "password": "password123",
}
login_data = {
    "email": new_user_data["email"],
    "password": new_user_data["password"],
}
headers = None  # Global variable


# registration
async def test_create_user(client):
    response = await client.post("/users", json=new_user_data)
    create_user_response = response.json()

    # Ensures user was created successfully
    assert response.status_code == 201
    assert create_user_response["username"] == new_user_data["username"]
    assert create_user_response["email"] == new_user_data["email"]


# login and store token
async def test_login(client):
    global headers  # Declares that we are using the global 'headers' variable

    login_response = await client.post("/users/login", json=login_data)

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Ensure token exists
    assert token
    # Modify the global 'headers' variable
    headers = {"Authorization": f"Bearer {token}"}


# user health check and data
async def test_get_me(client):
    response = await client.get("/users/me", headers=headers)
    json_response = response.json()

    print(response)
    print(json_response)

    assert response.status_code == 200
    assert json_response["username"] == new_user_data["username"]
    assert json_response["email"] == new_user_data["email"]
    assert isinstance(json_response["id"], int)


# find all
async def test_get_users(client):
    response = await client.get("/users")
    json_response = response.json()

    # Expect list with one user from seed
    assert len(json_response) == 2


# find one
async def test_get_user_by_id(client):
    response = await client.get("/users/1")
    json_response = response.json()

    # Expect to receive only the seed user
    assert json_response["username"] == "seed_user"
    assert json_response["email"] == "seed_user@email.com"


# update
async def test_update_user(client):
    # * start update test
    updated_data = {"username": "updated_username", "email": "updated_email@.com"}
    response = await client.put("users/2", json=updated_data, headers=headers)
    json_response = response.json()

    # Expect update to be successfull
    assert response.status_code == 200
    # Expect values to be updated
    assert json_response["username"] == "updated_username"
    assert json_response["email"] == "updated_email@.com"


# delete
async def test_delete_user(client):
    # get token
    login_data_after_update = {
        "email": "updated_email@.com",
        "password": login_data["password"],
    }
    login_response = await client.post(
        "/users/login",
        json=login_data_after_update,
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    assert token  # Ensure token exists
    headers = {"Authorization": f"Bearer {token}"}

    check_user_response = await client.get("/users/me", headers=headers)
    assert check_user_response
    user = check_user_response.json()

    assert user["email"] == login_data_after_update["email"]

    # * start delete test
    response = await client.delete(f"/users/{user['id']}", headers=headers)
    response_json = response.json()

    assert response.status_code == 200
    assert response_json["username"] == "updated_username"
    assert response_json["email"] == login_data_after_update["email"]
