# MCP Demo Server

[![Python CI](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/python-ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/python-ci.yml)

This project is a simple Python Flask server that demonstrates reading and writing to a JSON file (`data.json`) using an API designed to support Model Context Protocol (MCP) like queries.

## Features

-   Stores data in a local `data.json` file.
-   Provides an MCP-like `/mcp/query` endpoint for reading and writing data.
-   Supports nested key access for both read and write operations (e.g., `user.settings.theme`).
-   Includes a `/mcp/dump` endpoint to view the entire contents of `data.json` (for debugging).

## Setup and Installation

Follow these steps to set up and run the MCP Demo Server (which functions as a test-api-mcp server):

1.  **Clone this repository (if you haven't already):**
    ```bash
    # git clone <repository-url>
    # cd <repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### VSCode MCP Configuration

To configure VSCode to communicate with this server for Model Context Protocol (MCP) development:

1.  **Identify the MCP Server Endpoint:**
    *   This server (`MCP Demo Server`) exposes its MCP endpoint at `/mcp/query`.
    *   When running locally with default Flask settings, this will typically be `http://127.0.0.1:5000/mcp/query` or `http://0.0.0.0:5000/mcp/query`.

2.  **VSCode Settings (Example):**
    *   If you are using a VSCode extension that supports MCP, it might require you to configure the server endpoint in your VSCode `settings.json` file (usually found in your project's `.vscode/settings.json` or your global user settings).
    *   For example, you might add the following setting, replacing `"mcp.client.defaultEndpoint"` with the actual setting required by your chosen extension:
        ```json
        {
            "mcp.client.defaultEndpoint": "http://127.0.0.1:5000/mcp/query"
        }
        ```
    *   Ensure the server is running (`python app.py` or `flask run`) when your VSCode extension attempts to connect.

3.  **Relevant VSCode Extensions:**
    *   You may need a VSCode extension that can act as a generic HTTP/REST client to interact with the `/mcp/query` endpoint, or a specific extension designed for MCP if available. Search the VSCode Marketplace for terms like "REST client" or "MCP".


## Running the Server

To start the MCP Demo Server / `test-api-mcp` server (which is this Flask application):

```bash
python app.py
```

Or using the Flask CLI:

```bash
flask run
```

The server will typically start on `http://127.0.0.1:5000/` or `http://0.0.0.0:5000/`.

## API Endpoints


The server listens on `http://127.0.0.1:5000` by default.

### 1. MCP Query: Write and Read Data

-   **Endpoint:** `/mcp/query`
-   **Method:** `POST`
-   **Description:** Allows reading or writing data based on the provided JSON payload.
-   **Request Body (JSON):**
    -   `type` (string, required): Can be `"read"` or `"write"`.
    -   `key` (string, required): The dot-separated key path for the data (e.g., `"config.version"`, `"user.name"`).
    -   `value` (any, required for `type="write"`): The value to set for the specified key.


#### Example: Writing a Simple Key-Value Pair

This command writes the name "Jules" to `user.profile.name`.

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
    "type": "write",
    "key": "user.profile.name",
    "value": "Jules"
}' \
http://127.0.0.1:5000/mcp/query

```
**Response (Success):**
```json
{
    "message": "Key 'user.profile.name' successfully updated.",
    "key": "user.profile.name",
    "value": "Jules"
}
```


#### Example: Writing a More Complex Nested Structure

This command writes notification settings under `system.settings.notifications`.

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
    "type": "write",
    "key": "system.settings.notifications",
    "value": {
        "email": true,
        "sms": false,
        "push": {
            "enabled": true,
            "sound": "default"
        }
    }
}' \
http://127.0.0.1:5000/mcp/query
```
**Response (Success):**
```json
{
    "message": "Key 'system.settings.notifications' successfully updated.",
    "key": "system.settings.notifications",
    "value": {
        "email": true,
        "sms": false,
        "push": {
            "enabled": true,
            "sound": "default"
        }
    }
}
```
After these write operations, the `data.json` file might look like:

```json
{
    "user": {
        "profile": {
            "name": "Jules"
        }
    },
    "system": {
        "settings": {
            "notifications": {

                "email": true,
                "sms": false,
                "push": {
                    "enabled": true,
                    "sound": "default"
                }
            }
        }
    }
}
```

#### Example: Reading Data (Simple Key)

This command reads the value of `user.profile.name`.

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
    "type": "read",
    "key": "user.profile.name"
}' \
http://127.0.0.1:5000/mcp/query

```
**Response (Success):**
```json
{
    "key": "user.profile.name",
    "value": "Jules"
}
```

#### Example: Reading Data (Nested Key)

This command reads the value of `system.settings.notifications.push.sound`.

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
    "type": "read",
    "key": "system.settings.notifications.push.sound"
}' \
http://127.0.0.1:5000/mcp/query
```
**Response (Success):**
```json
{
    "key": "system.settings.notifications.push.sound",
    "value": "default"
}
```

#### Example: Reading a Non-Existent Key

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
    "type": "read",
    "key": "user.profile.nonexistent_key"
}' \
http://127.0.0.1:5000/mcp/query
```
**Response (Key Not Found):**
```json
{
    "error": "Key 'user.profile.nonexistent_key' not found."
}
```

### 2. Dump Data (for Debugging)


-   **Endpoint:** `/mcp/dump`
-   **Method:** `GET`
-   **Description:** Retrieves the entire content of `data.json`. Useful for debugging.

**Example:**
```bash
curl http://127.0.0.1:5000/mcp/dump
```

**Response (Example, after above writes):**

```json
{
    "user": {
        "profile": {
            "name": "Jules"
        }
    },
    "system": {
        "settings": {
            "notifications": {

                "email": true,
                "sms": false,
                "push": {
                    "enabled": true,
                    "sound": "default"
                }

            }
        }
    }
}
```

## To Do / Potential Improvements

-   More robust error handling.
-   Input validation for key names and values.
-   Support for other MCP operations (e.g., delete, list).
-   More comprehensive unit tests.

## Core Modeling Engine

This project includes a core modeling engine designed for flexible and extensible data processing and simulations. The engine is built around the concept of `ModelingComponent` objects, which can be chained together to create complex modeling pipelines.

### Structure

-   `core_modeling_engine/`: Directory containing all modules related to the core modeling engine.
    -   `base_component.py`: Defines the `ModelingComponent` base class, which provides a common interface for all modeling components.
-   `tests/core_modeling_engine/`: Contains unit tests for the core modeling engine components.
