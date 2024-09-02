import pytest
import json
from app import app


@pytest.fixture()
def client():
    client = app.test_client()
    yield client

def test_up_and_running(client):
    response = client.get("/up")
    # Verify the request was successful
    assert response.status_code == 200

    # Verify it returned data
    assert b"All systems go! Up and running" in response.data

def test_no_of_view_endpoint(client):
    response = client.get("/no_of_views")

    # Verify the request was successful
    assert response.status_code == 200
    data = json.loads(response.data)

    # Verify response is not empty
    assert "no_of_views" in data

def test_current_image_endpoint(client):
    response = client.get("/currentimage")

    # Verify the request was successful
    assert response.status_code == 200
    
    # Verify the content type is an image (change as needed, e.g., image/jpeg)
    assert response.headers["Content-Type"] == "image/gif"

    # Verify that the image data is not empty
    assert len(response.data) > 0




