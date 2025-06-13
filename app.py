from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

# --- JSON Helper Functions (from previous step) ---
def read_data():
    """Reads data from DATA_FILE. Returns an empty dict if file doesn't exist or is invalid JSON."""
    if not os.path.exists(DATA_FILE):
        # Initialize data.json if it doesn't exist
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            # Handle empty file case
            content = f.read()
            if not content:
                return {}
            data = json.loads(content)
            return data
    except (IOError, json.JSONDecodeError):
        # If error, try to reset data.json to an empty state
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
        return {}

def write_data(data):
    """Writes the given Python dictionary to DATA_FILE."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False

# --- Nested Key Access Helper Functions ---
def get_nested_value(data_dict, key_path):
    """Accesses a value in a nested dictionary using a dot-separated key_path."""
    keys = key_path.split('.')
    current_level = data_dict
    for key in keys:
        if isinstance(current_level, dict) and key in current_level:
            current_level = current_level[key]
        else:
            return None  # Key not found or path is invalid
    return current_level

def set_nested_value(data_dict, key_path, value):
    """Sets a value in a nested dictionary using a dot-separated key_path.
       Creates intermediate dictionaries if they don't exist."""
    keys = key_path.split('.')
    current_level = data_dict
    for i, key in enumerate(keys[:-1]): # Iterate up to the second to last key
        if key not in current_level or not isinstance(current_level[key], dict):
            current_level[key] = {} # Create a new dict if key doesn't exist or not a dict
        current_level = current_level[key]
    current_level[keys[-1]] = value # Set the value at the final key

# --- MCP API Endpoints ---
@app.route('/mcp/query', methods=['POST'])
def mcp_query():
    try:
        query = request.get_json()
        if not query or 'type' not in query or 'key' not in query:
            return jsonify({"error": "Invalid MCP query format. 'type' and 'key' are required."}), 400

        query_type = query['type']
        key_path = query['key']
        all_data = read_data()

        if query_type == "read":
            value = get_nested_value(all_data, key_path)
            if value is not None:
                return jsonify({"key": key_path, "value": value}), 200
            else:
                return jsonify({"error": f"Key '{key_path}' not found."}), 404

        elif query_type == "write":
            if 'value' not in query:
                return jsonify({"error": "Invalid MCP write query. 'value' is required."}), 400

            new_value = query['value']
            set_nested_value(all_data, key_path, new_value)

            if write_data(all_data):
                return jsonify({"message": f"Key '{key_path}' successfully updated.", "key": key_path, "value": new_value}), 200
            else:
                return jsonify({"error": "Failed to write data to file."}), 500

        else:
            return jsonify({"error": f"Unsupported query type: {query_type}. Supported types are 'read' and 'write'."}), 400

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

@app.route('/mcp/dump', methods=['GET'])
def mcp_dump():
    all_data = read_data()
    return jsonify(all_data), 200

if __name__ == '__main__':
    # Ensure data.json exists with an empty object {} if it's not there or empty
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)

    app.run(debug=True, host='0.0.0.0', port=5000)
