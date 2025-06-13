# MCP Demo Server

[![Python CI](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/python-ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/actions/workflows/python-ci.yml)

This project is a simple Python Flask server that demonstrates reading and writing to a JSON file (`data.json`) using an API designed to support Model Context Protocol (MCP) like queries.

## Features

-   Stores data in a local `data.json` file.
-   Provides an MCP-like `/mcp/query` endpoint for reading and writing data.
-   Supports nested key access for both read and write operations (e.g., `user.settings.theme`).
-   Includes a `/mcp/dump` endpoint to view the entire contents of `data.json` (for debugging).

## Setup and Installation

1.  **Clone the repository (if you haven't already):**
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

## Running the Server

To start the Flask development server:

```bash
python app.py
```

Or using the Flask CLI:

```bash
flask run
```

The server will typically start on `http://127.0.0.1:5000/` or `http://0.0.0.0:5000/`.

## API Endpoints

### 1. MCP Query

-   **Endpoint:** `/mcp/query`
-   **Method:** `POST`
-   **Description:** Allows reading or writing data based on the provided JSON payload.
-   **Request Body (JSON):**
    -   `type` (string, required): Can be `"read"` or `"write"`.
    -   `key` (string, required): The dot-separated key path for the data (e.g., `"config.version"`, `"user.name"`).
    -   `value` (any, required for `type="write"`): The value to set for the specified key.

#### Example: Writing Data

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "type": "write",
    "key": "user.profile.name",
    "value": "Jules"
}' http://127.0.0.1:5000/mcp/query
```
**Response (Success):**
```json
{
    "message": "Key 'user.profile.name' successfully updated.",
    "key": "user.profile.name",
    "value": "Jules"
}
```

#### Example: Writing Nested Data

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "type": "write",
    "key": "system.settings.notifications.email",
    "value": true
}' http://127.0.0.1:5000/mcp/query
```

After this, `data.json` might look like:
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
                "email": true
            }
        }
    }
}
```

#### Example: Reading Data

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "type": "read",
    "key": "user.profile.name"
}' http://127.0.0.1:5000/mcp/query
```
**Response (Success):**
```json
{
    "key": "user.profile.name",
    "value": "Jules"
}
```

**Response (Key Not Found):**
```json
{
    "error": "Key 'user.profile.nonexistent_key' not found."
}
```

### 2. Dump Data

-   **Endpoint:** `/mcp/dump`
-   **Method:** `GET`
-   **Description:** Retrieves the entire content of `data.json`. Useful for debugging.

**Example:**
```bash
curl http://127.0.0.1:5000/mcp/dump
```
**Response (Example):**
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
                "email": true
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
