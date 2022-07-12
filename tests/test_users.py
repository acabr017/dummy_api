import pytest
from app import schemas
from jose import jwt
from app.config import settings


def test_root(client):

    res = client.get("/")
    print(res.json())
    assert res.json().get('message') == 'Home Page'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "abc@email.com", "password": "1234"})
    # The line below will create a new schema with the unpacked (hence the **) dictionary provided above
    # as the fields needed. That way we can test to make sure that the output matches everything
    new_test_user = schemas.UserResponse(**res.json())
    assert new_test_user.email == "abc@email.com"
    assert res.status_code == 201


def test_valid_login_user(client, test_user):
    # This would work, but isn't really very Pythonic
    # creating_user = client.post(
    #     "/users/", json={"email": "abc@email.com", "password": "1234"})
    # assert creating_user.status_code ==

    # This would work, but it will end up dropping and creating
    # my database twice, which is wasteful.
    # test_create_user(client)

    # A better method is done above: create a fixture that will create
    # a user, without dropping the databse.
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "Bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', '1234', 403),
    ('abc@email.com', 'wrongpassword', 403),
    ('wrongemail@email.com', 'wrongpassword', 403),
    (None, '1234', 422),
    ('abc@email.com', None, 422),
    (None, None, 422)
])
def test_invalid_login_user(client, test_user, email, password, status_code):
    # Here I hardcoded tests for invalid email by itself, invalid password by itself, and a blank
    # by itself. This is inefficient and not Pythonic.
    # Better code is to use parametrization
    # wrong_password_res = client.post(
    #     "/login", data={"username": test_user['email'], "password": "wrongpassword"})
    # assert wrong_password_res.status_code == 403
    # wrong_username_res = client.post(
    #     "/login", data={"username": "wrongusername", "password": test_user['password']})
    # assert wrong_username_res.status_code == 403
    # blank_res = client.post(
    #     "/login", data={"username": " ", "password": " "})
    # assert blank_res.status_code == 403

    # Here is the code that uses our parameters
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
