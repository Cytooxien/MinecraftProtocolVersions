import requests
import tempfile
import zipfile
import json
import os

def fetch_minecraft_version_manifest():
    """
    Fetches the JSON data from the Minecraft version manifest API.

    Returns:
        dict: The parsed JSON data from the API, or None if an error occurs.
    """
    url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Parse and return the JSON data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def fetch_minecraft_version_by_version(version_type: str):
    """
    Fetches a dictionary of Minecraft versions of a specific type (release or snapshot)
    from the version manifest.

    Args:
        version_type (str): The type of versions to fetch ('release' or 'snapshot').

    Returns:
        dict: A dictionary where keys are version names and values are their URLs.
    """

    try:
        # Fetch the manifest
        manifest = fetch_minecraft_version_manifest()

        # Filter the versions based on the type
        versions = manifest.get("versions", [])
        filtered_versions = {
            version["id"]: version["url"]
            for version in versions if version["type"] == version_type
        }

        return filtered_versions

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

def fetch_minecraft_client_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        version_manifest = response.json()
        return version_manifest['downloads']['client']['url']
    except requests.RequestException as e:
        print(f"Error fetching version manifest {url}: {e}")
        return None


def download_client_version(version_id, url):
    """
    Downloads the Minecraft client JAR, extracts the versions.json from the root directory,
    and returns its content. If the file does not exist, returns a fallback object.

    Args:
        version_id (str): The version ID of Minecraft.
        url (str): The URL to fetch the client JAR.

    Returns:
        dict: The content of the versions.json file or a fallback object with 'name'.
    """
    client_url = fetch_minecraft_client_url(url)
    if not client_url:
        return {"name": version_id}

    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Download the JAR file to a temporary file
            temp_file_path = os.path.join(temp_dir, f"{version_id}.jar")
            response = requests.get(client_url, stream=True)
            response.raise_for_status()

            with open(temp_file_path, 'wb') as temp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)

            # Extract and read the versions.json file
            with zipfile.ZipFile(temp_file_path, 'r') as jar_file:
                if "version.json" in jar_file.namelist():
                    with jar_file.open("version.json") as versions_file:
                        return json.load(versions_file)
                else:
                    print(f"version.json not found in {temp_file_path}")
                    return {"name": version_id}
        except requests.RequestException as e:
            print(f"Error downloading JAR from {client_url}: {e}")
            return {"id": version_id}
        except zipfile.BadZipFile as e:
            print(f"Error opening JAR file {temp_file_path}: {e}")
            return {"name": version_id}