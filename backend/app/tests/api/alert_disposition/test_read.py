import uuid

from fastapi import status


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/alert/disposition/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/alert/disposition/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client):
    # Create some objects
    client.post("/api/alert/disposition/", json={"rank": 1, "value": "test"})
    client.post("/api/alert/disposition/", json={"rank": 2, "value": "test2"})

    # Read them back
    get = client.get("/api/alert/disposition/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_empty(client):
    get = client.get("/api/alert/disposition/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []
