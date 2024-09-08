# json_utils.py
import json

def load_json(filename):
    """Loads JSON data from a file."""
    with open(filename, 'r') as file:
        return json.load(file)

def save_json(filename, data):
    """Saves JSON data to a file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)