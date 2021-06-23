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
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client, key, value):
    update = client.put(f"/api/event/remediation/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client):
    update = client.put("/api/event/remediation/1", json={"value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_update_duplicate_unique_fields(client, key):
    # Create some objects
    create1_json = {"value": "test"}
    client.post("/api/event/remediation/", json=create1_json)

    create2_json = {"value": "test2"}
    create2 = client.post("/api/event/remediation/", json=create2_json)

    # Ensure you cannot update a unique field to a value that already exists
    update = client.put(create2.headers["Content-Location"], json={key: create1_json[key]})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_nonexistent_uuid(client):
    update = client.put(f"/api/event/remediation/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", "test"),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client, key, initial_value, updated_value):
    # Create the object
    create_json = {"value": "test"}
    create_json[key] = initial_value
    create = client.post("/api/event/remediation/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == initial_value

    # Update it
    update = client.put(create.headers["Content-Location"], json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == updated_value
