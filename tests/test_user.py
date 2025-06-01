import pytest
from src.security import bcryption

def test_register_success(client):
    response = client.post("/user/register", json={
        "username": "uniqueuser1234",
        "email": "uniqueuser@example.com",
        "password": "Unique@123456",
        "profileImageUrl": ""
    })
    assert response.status_code in (200, 201, 409)
    if response.status_code == 409:
        assert "Already exists" in response.json()["detail"]
    else:
        assert "Created Successfully" in response.json()["message"]

def test_register_existing_email(client, test_user):
    response = client.post("/user/register", json=test_user)
    assert response.status_code == 409

def test_login_success(client, test_user):
    response = client.post("/user/login", json={
        "email": test_user["email"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_wrong_password(client, test_user):
    response = client.post("/user/login", json={
        "email": test_user["email"],
        "password": "WrongPassword"
    })
    assert response.status_code == 200
    assert "invalid Password" in response.json()["message"]

def test_login_nonexistent_user(client):
    response = client.post("/user/login", json={
        "email": "nouser@example.com",
        "password": "AnyPassword"
    })
    assert response.status_code == 403

def test_get_user_details_success(client, token, test_user):
    response = client.get(
        "/user/user_data",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]

def test_get_user_details_invalid_token(client):
    response = client.get(
        "/user/user_data",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 403

@pytest.mark.parametrize("update_data", [
    {"username": "updateduser1234", "password": "NewPass@123"},
    {"username": "anotheruser5678", "password": "Another@456"}
])
def test_update_user_success(client, token, update_data):
    response = client.put(
        "/user/user_update/",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "updated Sucessfully" in response.json()["message"]

def test_update_user_invalid_token(client):
    response = client.put(
        "/user/user_update/",
        json={"username": "failuser", "password": "failpass"},
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 403

def test_delete_user_success(client, token):
    response = client.delete(
        "/user/user_delete/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]

def test_delete_user_invalid_token(client):
    response = client.delete(
        "/user/user_delete/",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 403

def test_upload_image(client, token, tmp_path):
    # Create a dummy image file
    img_path = tmp_path / "testimg.png"
    img_path.write_bytes(b"fakeimagedata")
    with open(img_path, "rb") as img_file:
        response = client.post(
            "/user/upload_image",
            files={"image": ("testimg.png", img_file, "image/png")},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert "imageUrl" in response.json()

def test_hash_and_verify_password():
    password = "MySecret@123"
    hashed = bcryption.hashPassword(password)
    assert bcryption.verifyPassword(password, hashed)
    assert not bcryption.verifyPassword("WrongPassword", hashed)