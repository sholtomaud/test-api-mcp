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

### Download and Install `test-api-mcp` Server

1.  **Download or Clone the `test-api-mcp` server:**
    *   Instructions to download/clone the server (e.g., `git clone <test-api-mcp-repository-url>`).
    *   Navigate into the server's directory: `cd <test-api-mcp-directory>`
2.  **Install server dependencies:**
    *   Provide commands for installing dependencies (e.g., `npm install`, `pip install -r requirements.txt`).
    *   Mention any prerequisites if known.
3.  **Run the `test-api-mcp` server:**
    *   Provide the command to start the server (e.g., `npm start`, `python server.py`).
    *   Note the default port it runs on if specified in its documentation.

*(Note: Please replace the placeholder instructions above with specific details for the `test-api-mcp` server.)*

### VSCode MCP Configuration

To configure VSCode to communicate with the `test-api-mcp` server for Model Context Protocol (MCP) development:

1.  **Identify the MCP Server Endpoint:**
    *   The `test-api-mcp` server, once running, should expose an endpoint for MCP queries. This is often `/mcp/query`.
    *   For this current project (MCP Demo Server), the equivalent endpoint is `http://127.0.0.1:5000/mcp/query` (or `http://0.0.0.0:5000/mcp/query`). You will need to find the corresponding URL for your `test-api-mcp` server.

2.  **VSCode Settings (Example):**
    *   If you are using a VSCode extension for MCP, it might require you to configure the server endpoint in your VSCode settings (`settings.json`).
    *   For example, you might add something like this (the exact setting depends on the extension):
        ```json
        {
            "mcp.server.endpoint": "http://<test-api-mcp-server-address>:<port>/mcp/query"
        }
        ```
    *   Replace `http://<test-api-mcp-server-address>:<port>/mcp/query` with the actual endpoint of your `test-api-mcp` server.

3.  **Relevant VSCode Extensions:**
    *   Consider searching the VSCode Marketplace for extensions that support MCP or provide a generic REST client interface if a specific MCP extension is not available.
    *   *(Placeholder: List any known/recommended VSCode extensions for MCP development here.)*

*(Note: The specifics of VSCode configuration can vary based on the `test-api-mcp` server's implementation and any VSCode extensions you choose to use.)*

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
