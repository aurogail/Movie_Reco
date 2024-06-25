import pytest
import pandas as pd
from fastapi.testclient import TestClient
from api_directory.api import app
import pandas as pd

client = TestClient(app)

@pytest.fixture(scope="module")
def test_login():
    response = client.post("/login", json={"user_id": 1000})
    assert response.status_code == 200
    return response.json().get('access_token')

def test_login_invalid_user():
    response = client.post("/login", json={"user_id": 9999999})  
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

@pytest.fixture(scope="module")
def auth_header(test_login):
    token = test_login
    return {"Authorization": f"Bearer {token}"}

def test_welcome(auth_header):
    response = client.get("/welcome", headers=auth_header)
    assert response.status_code == 200

def test_welcome_unauthenticated():
    response = client.get("/welcome")
    assert response.status_code == 403
'''
def test_recommendations(auth_header, svd_model_fixture):
    response = client.get("/recommendations", headers=auth_header)
    assert response.status_code == 200
'''
def test_recommendations_unauthenticated():
    response = client.get("/recommendations")
    assert response.status_code == 403

'''
def test_preferences(auth_header):
    response = client.get("/preferences", headers=auth_header)
    assert response.status_code == 200
'''

'''
def test_hybrid(auth_header, svd_model_fixture):
    request_body = {"titre": "Toy Story (1995)"}  
    response = client.post("/hybrid", json=request_body, headers=auth_header)
    assert response.status_code == 200
'''
def test_hybrid_invalid_movie(auth_header):
    request_body = {"titre": "Invalid Movie"}  
    response = client.post("/hybrid", json=request_body, headers=auth_header)
    assert response.status_code == 404


def test_hybrid_recommendations_unauthenticated():
    request_body = {"titre": "Toy Story (1995)"}  
    response = client.post("/hybrid", json=request_body)
    assert response.status_code == 403

