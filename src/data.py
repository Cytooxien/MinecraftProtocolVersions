import json
import os

def load_version_file(version_type: str):
    version_file = get_file_path(version_type)

    if not os.path.exists(version_file):
        return []

    with open(version_file, 'r') as f:
        return json.load(f)

def save_version_file(version_type: str, data: dict):
    with open(get_file_path(version_type), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_file_path(version_type: str):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    version_file = f'{version_type}.json'
    return os.path.join(project_root, version_file)

def extract_names_from_json(json_array):
    """
    Extracts all 'name' and, if applicable, 'id' values from a JSON array of objects,
    returning a list of strings. Includes 'id' only if it exists and is not the same as 'name'.

    Args:
        json_array (list): A list of JSON objects.

    Returns:
        list: A list of strings containing 'name' and optionally 'id'.
    """
    try:
        result = []
        for item in json_array:
            if "name" in item:
                result.append(item["name"])
                if "id" in item and item["id"] != item["name"]:
                    result.append(item["id"])
        return result
    except (TypeError, KeyError) as e:
        print(f"An error occurred: {e}")
        return []
