import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# テスト用の初期状態
@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update({
        "Soccer Team": {
            "description": "Outdoor soccer team practices and league matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "nina@mergington.edu"]
        }
    })


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Mergington High School" in response.text


def test_signup():
    response = client.post(
        "/activities/Soccer Team/signup",
        params={"email": "test@mergington.edu"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Signed up test@mergington.edu for Soccer Team"


def test_unregister():
    response = client.delete(
        "/activities/Soccer Team/unregister",
        params={"email": "alex@mergington.edu"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully unregistered alex@mergington.edu from Soccer Team"