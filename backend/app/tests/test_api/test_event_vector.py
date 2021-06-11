import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints, namely deleting an EventVector that is tied to an Event.
The DELETE endpoint will need to be updated once the Node endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_event_vector(client):
    # Create an event vector
    create = client.post("/api/event/vector/", json={"value": "default"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_vector_with_uuid(client):
    # Create an event vector and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/event/vector/", json={"uuid": u, "value": "default"})
    assert create.status_code == status.HTTP_201_CREATED
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/event/vector/{u}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_event_vector_duplicate_value(client):
    # Create an event vector
    client.post("/api/event/vector/", json={"value": "default"})

    # Ensure you cannot create another event vector with the same value
    create = client.post("/api/event/vector/", json={"value": "default"})
    assert create.status_code == status.HTTP_409_CONFLICT


def test_create_event_vector_invalid_uuid(client):
    create = client.post("/api/event/vector/", json={"uuid": 1, "value": "default"})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_event_vector_invalid_value(client):
    create = client.post("/api/event/vector/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_event_vector_missing_value(client):
    create = client.post("/api/event/vector/", json={})
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# READ
#


def test_get_all_event_vectors(client):
    # Create some event vectors
    client.post("/api/event/vector/", json={"value": "default"})
    client.post("/api/event/vector/", json={"value": "intel"})

    # Read them back
    get = client.get("/api/event/vector/")
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 2


def test_get_all_event_vectors_empty(client):
    get = client.get("/api/event/vector/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json() == []


def test_get_invalid_event_vector(client):
    get = client.get("/api/event/vector/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_event_vector(client):
    get = client.get(f"/api/event/vector/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# UPDATE
#


def test_update_event_vector(client):
    # Create an event vector
    create = client.post("/api/event/vector/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_event_vector_multiple_fields(client):
    # Create an event vector
    create = client.post("/api/event/vector/", json={"value": "default"})

    # Update multiple fields
    update = client.put(
        create.headers["Content-Location"],
        json={"description": "Test", "value": "test"},
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] == "Test"
    assert get.json()["value"] == "test"


def test_udpate_event_vector_same_value(client):
    # Create an event vector
    create = client.post("/api/event/vector/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_event_vector_duplicate_value(client):
    # Create some event vectors
    client.post("/api/event/vector/", json={"value": "default"})
    create = client.post("/api/event/vector/", json={"value": "intel"})

    # Ensure you cannot update an event vector value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == status.HTTP_400_BAD_REQUEST


def test_update_event_vector_invalid_uuid(client):
    update = client.put("/api/event/vector/1", json={"value": "default"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_event_vector_invalid_value(client):
    update = client.put(f"/api/event/vector/{uuid.uuid4()}", json={"value": {"asdf": "asdf"}})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_event_vector_none_value(client):
    # Create an event vector
    create = client.post("/api/event/vector/", json={"value": "default"})

    # Ensure you cannot update an event vector value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_nonexistent_event_vector(client):
    update = client.put(f"/api/event/vector/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# DELETE
#


def test_delete_event_vector(client):
    # Create an event vector
    create = client.post("/api/event/vector/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_invalid_event_vector(client):
    delete = client.delete("/api/event/vector/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_event_vector(client):
    delete = client.delete(f"/api/event/vector/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND
