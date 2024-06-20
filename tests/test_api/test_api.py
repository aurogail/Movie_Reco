import pytest
import pandas as pd
from fastapi.testclient import TestClient
from api_directory.api import app
from api_directory.generate_token import load_user_ids


client = TestClient(app)

# users = load_user_ids("fixtures/user_matrix_test.csv")
# df_content_tags = pd.read_csv("fixtures/movies_tags_test.csv")

@pytest.fixture(scope="module")
def test_login():
    response = client.post("/login", json={"user_id": 1000})
    assert response.status_code == 200
    return response.json().get('access_token')

@pytest.fixture(scope="module")
def auth_header(test_login):
    token = test_login
    return {"Authorization": f"Bearer {token}"}

def test_welcome(auth_header):
    response = client.get("/welcome", headers=auth_header)
    assert response.status_code == 200


def test_recommendations(auth_header):
    response = client.get("/recommendations", headers=auth_header)
    assert response.status_code == 200

"""
def test_preferences(auth_header):
    response = client.get("/preferences", headers=auth_header)
    assert response.status_code == 200


def test_hybrid(auth_header):
    response = client.get("/hybrid", headers=auth_header)
    assert response.status_code == 200"""