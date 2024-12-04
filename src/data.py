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
    Extracts all values of the 'name' field from a JSON array of objects.

    Args:
        json_array (list): A list of JSON objects.

    Returns:
        list: A list of values corresponding to the 'name' field.
    """
    try:
        # Extrahiere die Werte des Felds 'name'
        names = [item["name"] for item in json_array if "name" in item]
        return names
    except (TypeError, KeyError) as e:
        print(f"An error occurred: {e}")
        return []


def is_version_greater(version: str, base_version: str = "1.14") -> bool:
    """
    Checks if a version is greater than a given base version.

    Args:
        version (str): The version to check (e.g., "1.15").
        base_version (str): The base version to compare against (default: "1.14").

    Returns:
        bool: True if `version` is greater than `base_version`, False otherwise.
    """
    # Split the versions into major and minor parts
    try:
        version_parts = list(map(int, version.split(".")))
        base_parts = list(map(int, base_version.split(".")))
    except ValueError:
        raise ValueError(f"Invalid version format: {version} or {base_version}")

    # Compare each part of the version numbers
    for v_part, b_part in zip(version_parts, base_parts):
        if v_part > b_part:
            return True
        elif v_part < b_part:
            return False

    # If we reach here, all compared parts are equal. Check length of parts.
    return len(version_parts) > len(base_parts)
