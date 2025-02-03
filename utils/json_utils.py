"""Module For Json File Operations."""
import json


def load_ship_json(file_name: str) -> str:
    """
    Function to deserialize json.
    """
    ship_json = ""
    try:
        with open(file_name, "r", encoding="utf-8") as json_obj:
            ship_json = json.loads(json_obj.read())
    except OSError:
        print(f"load_ship_json: Could not open/read json file: {file_name}")

    return ship_json
