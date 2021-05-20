import uuid


"""
NOTE: There are no tests for the foreign key constraints, namely deleting a NodeThreatActor that is tied to a Node.
The DELETE endpoint will need to be updated once the Node endpoints are in place in order to account for this.
"""


#
# CREATE
#


def test_create_node_threat_actor(client):
    # Create a node threat actor
    create = client.post("/api/node/threat_actor/", json={"value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_node_threat_actor_with_uuid(client):
    # Create a node threat actor and specify the UUID it should use
    u = str(uuid.uuid4())
    create = client.post("/api/node/threat_actor/", json={"uuid": u, "value": "default"})
    assert create.status_code == 201
    assert create.headers["Content-Location"]

    # Read it back using the UUID
    get = client.get(f"/api/node/threat_actor/{u}")
    assert get.status_code == 200
    assert get.json()["uuid"] == u
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_create_node_threat_actor_duplicate_value(client):
    # Create a node threat actor
    client.post("/api/node/threat_actor/", json={"value": "default"})

    # Ensure you cannot create another node threat actor with the same value
    create = client.post("/api/node/threat_actor/", json={"value": "default"})
    assert create.status_code == 409


def test_create_node_threat_actor_invalid_value(client):
    create = client.post("/api/node/threat_actor/", json={"value": {"asdf": "asdf"}})
    assert create.status_code == 422


def test_create_node_threat_actor_missing_value(client):
    create = client.post("/api/node/threat_actor/", json={})
    assert create.status_code == 422


#
# READ
#


def test_get_all_node_threat_actors(client):
    # Create some node threat actors
    client.post("/api/node/threat_actor/", json={"value": "default"})
    client.post("/api/node/threat_actor/", json={"value": "intel"})

    # Read them back
    get = client.get("/api/node/threat_actor/")
    assert get.status_code == 200
    assert len(get.json()) == 2


def test_get_all_node_threat_actors_empty(client):
    get = client.get("/api/node/threat_actor/")
    assert get.status_code == 200
    assert get.json() == []


def test_get_nonexistent_node_threat_actor(client):
    get = client.get(f"/api/node/threat_actor/{uuid.uuid4()}")
    assert get.status_code == 404


#
# UPDATE
#


def test_update_node_threat_actor(client):
    # Create a node threat actor
    create = client.post("/api/node/threat_actor/", json={"value": "default"})

    # Update a single field
    update = client.put(create.headers["Content-Location"], json={"value": "test"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "test"


def test_update_node_threat_actor_multiple_fields(client):
    # Create a node threat actor
    create = client.post("/api/node/threat_actor/", json={"value": "default"})

    # Update multiple fields
    update = client.put(
        create.headers["Content-Location"],
        json={"description": "Test", "value": "test"},
    )
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] == "Test"
    assert get.json()["value"] == "test"


def test_udpate_node_threat_actor_same_value(client):
    # Create a node threat actor
    create = client.post("/api/node/threat_actor/", json={"value": "default"})

    # Update a field to the same value
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 204
    assert update.headers["Content-Location"]

    # Read it back
    get = client.get(update.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["description"] is None
    assert get.json()["value"] == "default"


def test_update_node_threat_actor_duplicate_value(client):
    # Create some node threat actors
    client.post("/api/node/threat_actor/", json={"value": "default"})
    create = client.post("/api/node/threat_actor/", json={"value": "intel"})

    # Ensure you cannot update a node threat actor value to one that already exists
    update = client.put(create.headers["Content-Location"], json={"value": "default"})
    assert update.status_code == 400


def test_update_node_threat_actor_invalid_value(client):
    # Create a node threat actor
    create = client.post("/api/node/threat_actor/", json={"value": "default"})

    # Ensure you cannot update a value to an invalid value
    update = client.put(
        create.headers["Content-Location"], json={"value": {"asdf": "asdf"}}
    )
    assert update.status_code == 422


def test_update_node_threat_actor_none_value(client):
    # Create a node threat actor
    create = client.post("/api/node/threat_actor/", json={"value": "default"})

    # Ensure you cannot update a node threat actor value to None
    update = client.put(create.headers["Content-Location"], json={"value": None})
    assert update.status_code == 400


def test_update_nonexistent_node_threat_actor(client):
    update = client.put(f"/api/node/threat_actor/{uuid.uuid4()}", json={"value": "default"})
    assert update.status_code == 404


#
# DELETE
#


def test_delete_node_threat_actor(client):
    # Create a node threat actor
    create = client.post("/api/node/threat_actor/", json={"value": "default"})

    # Delete it
    delete = client.delete(create.headers["Content-Location"])
    assert delete.status_code == 204

    # Make sure it is gone
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 404


def test_delete_nonexistent_node_threat_actor(client):
    delete = client.delete(f"/api/node/threat_actor/{uuid.uuid4()}")
    assert delete.status_code == 400
