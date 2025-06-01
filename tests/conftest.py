import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def test_user(client:TestClient):
    user_data={
        "username":"testuser1234",
        "email":"testuser@example.com",
        "password":"Test@123456",
        "profileImageUrl": ""
    }
    client.post("user/register",json=user_data)
    return user_data

@pytest.fixture(scope="module")
def token(client:TestClient,test_user):
    response=client.post("/user/login",json={"email":test_user["email"],"password":test_user["password"]})
    return response.json().get("token")
    
    


