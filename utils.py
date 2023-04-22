import os
import json


def load_config(filename):
    # Check if the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Configuration file '{filename}' not found.")

    with open(filename, 'r') as file:
        return json.load(file)
