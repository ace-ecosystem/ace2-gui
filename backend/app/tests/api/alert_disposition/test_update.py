import pytest
import uuid

from fastapi import status


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", 123),
        ("description", ""),
        ("rank", 1.234),
        ("rank", "123"),
        ("rank", None),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.patch(f"/api/alert/disposition/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client):
    update = client.patch("/api/alert/disposition/1", json={"value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("rank"),
        ("value"),
    ],
)
def test_update_duplicate_unique_fields(client, key):
    # Create some objects
    create1_json = {"rank": 1, "value": "test"}
    client.post("/api/alert/disposition/", json=create1_json)

    create2_json = {"rank": 2, "value": "test2"}
    create2 = client.post("/api/alert/disposition/", json=create2_json)

    # Ensure you cannot update a unique field to a value that already exists
    update = client.patch(create2.headers["Content-Location"], json={key: create1_json[key]})
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_uuid(client):
    update = client.patch(f"/api/alert/disposition/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", "test"),
        ("rank", 1, 2),
        ("rank", 1, 1),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client, key, initial_value, updated_value):
    # Create the object
    create_json = {"rank": 1, "value": "test"}
    create_json[key] = initial_value
    create = client.post("/api/alert/disposition/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == initial_value

    # Update it
    update = client.patch(create.headers["Content-Location"], json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == updated_value
