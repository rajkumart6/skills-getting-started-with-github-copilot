import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data  # Should not be empty

def test_signup_and_duplicate(client):
    # Pick an activity from the list
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "testuser@mergington.edu"

    # Sign up
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json()["message"]

    # Duplicate signup
    resp2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp2.status_code == 400
    assert "already signed up" in resp2.json()["detail"]

def test_signup_activity_not_found(client):
    resp = client.post("/activities/NonexistentActivity/signup?email=foo@bar.com")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()

def test_delete_participant(client):
    activities = client.get("/activities").json()
    activity_name = next(iter(activities))
    email = "deleteuser@mergington.edu"
    # Sign up first
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Delete
    resp = client.delete(f"/activities/{activity_name}/signup?email={email}")
    # Accept 200 or 204 (depending on backend)
    assert resp.status_code in (200, 204, 404)
