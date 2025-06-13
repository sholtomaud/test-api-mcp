import pytest
import json
import os
# Ensure the app module can be found, especially if tests are in a subfolder or run differently
# For this structure, direct import should be fine.
from app import app as flask_app

@pytest.fixture
def app_instance(): # Renamed to avoid conflict with 'app' module/variable if any confusion
    # Configure the app for testing
    flask_app.config.update({
        "TESTING": True,
    })

    original_data_file = getattr(flask_app, 'DATA_FILE_ORIGINAL', 'data.json') # Store original if not already stored
    if not hasattr(flask_app, 'DATA_FILE_ORIGINAL'):
        flask_app.DATA_FILE_ORIGINAL = original_data_file

    test_data_file = "test_data.json"

    # This global variable is used by helper functions read_data and write_data in app.py
    # We need to change it for the duration of the test.
    import app as app_module
    app_module.DATA_FILE = test_data_file

    # Ensure the test data file is clean before each test
    if os.path.exists(test_data_file):
        os.remove(test_data_file)
    with open(test_data_file, 'w') as f:
        json.dump({}, f)

    yield flask_app

    # Clean up: remove the test data file and restore original DATA_FILE path
    if os.path.exists(test_data_file):
        os.remove(test_data_file)
    app_module.DATA_FILE = flask_app.DATA_FILE_ORIGINAL


@pytest.fixture
def client(app_instance): # Use the renamed fixture
    return app_instance.test_client()

def test_read_empty_dump(client):
    response = client.get('/mcp/dump')
    assert response.status_code == 200
    assert response.json == {}

def test_write_and_read_simple(client):
    write_payload = {"type": "write", "key": "greeting", "value": "Hello"}
    response = client.post('/mcp/query', json=write_payload)
    assert response.status_code == 200
    assert response.json.get("key") == "greeting"
    assert response.json.get("value") == "Hello"

    read_payload = {"type": "read", "key": "greeting"}
    response = client.post('/mcp/query', json=read_payload)
    assert response.status_code == 200
    assert response.json.get("key") == "greeting"
    assert response.json.get("value") == "Hello"

def test_write_and_read_nested(client):
    write_payload = {"type": "write", "key": "config.user.name", "value": "TestUser"}
    response = client.post('/mcp/query', json=write_payload)
    assert response.status_code == 200
    assert response.json.get("key") == "config.user.name"
    assert response.json.get("value") == "TestUser"

    read_payload = {"type": "read", "key": "config.user.name"}
    response = client.post('/mcp/query', json=read_payload)
    assert response.status_code == 200
    assert response.json.get("key") == "config.user.name"
    assert response.json.get("value") == "TestUser"

    read_payload_parent = {"type": "read", "key": "config.user"}
    response_parent = client.post('/mcp/query', json=read_payload_parent)
    assert response_parent.status_code == 200
    assert response_parent.json.get("key") == "config.user"
    assert response_parent.json.get("value") == {"name": "TestUser"}

def test_read_non_existent_key(client):
    read_payload = {"type": "read", "key": "non.existent.key"}
    response = client.post('/mcp/query', json=read_payload)
    assert response.status_code == 404
    assert "error" in response.json
    assert "not found" in response.json["error"]

def test_mcp_dump_after_writes(client):
    client.post('/mcp/query', json={"type": "write", "key": "item1", "value": "value1"})
    client.post('/mcp/query', json={"type": "write", "key": "item2.subitem", "value": "value2"})

    response = client.get('/mcp/dump')
    assert response.status_code == 200
    expected_data = {
        "item1": "value1",
        "item2": {
            "subitem": "value2"
        }
    }
    assert response.json == expected_data

def test_invalid_query_format(client):
    response = client.post('/mcp/query', json={"key": "somekey"}) # Missing type
    assert response.status_code == 400
    assert "error" in response.json
    assert "Invalid MCP query format" in response.json["error"]

    response = client.post('/mcp/query', json={"type": "read"}) # Missing key
    assert response.status_code == 400
    assert "error" in response.json
    assert "Invalid MCP query format" in response.json["error"]

def test_invalid_write_query_format(client):
    response = client.post('/mcp/query', json={"type": "write", "key": "somekey"}) # Missing value
    assert response.status_code == 400
    assert "error" in response.json
    assert "Invalid MCP write query" in response.json["error"]

def test_unsupported_query_type(client):
    response = client.post('/mcp/query', json={"type": "delete", "key": "somekey"})
    assert response.status_code == 400
    assert "error" in response.json
    assert "Unsupported query type" in response.json["error"]
