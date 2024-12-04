import argparse
from data import load_version_file
from download import *
from src.data import extract_names_from_json, save_version_file

parser = argparse.ArgumentParser(description='Minecraft Server Protocol Version Fetcher')
parser.add_argument(
    "type",
    choices=["release", "snapshot"],
    help="Version Type (release or snapshot)."
)


def run(version_type: str):
    version_data = load_version_file(version_type)
    versions = fetch_minecraft_version_by_version(version_type)

    print(__file__)

    version_names = extract_names_from_json(version_data)
    missing_versions = {version:url for version, url in versions.items() if version not in version_names}
    missing_version_names = list(missing_versions.keys())

    print("Found {} minecraft versions.".format(len(versions)))
    print("Missing minecraft versions: {}".format(missing_version_names))

    if len(missing_versions) == 0:
        exit(0)

    for (version, url) in missing_versions.items():
        print("Downloading minecraft version {}...".format(version))
        version_data.append(download_client_version(version, url))

    added_versions = ",".join(missing_versions)
    os.system(f"echo Added Versions: {added_versions} >> $GITHUB_STEP_SUMMARY")
    os.system(f"echo ::set-output name=ADDED_VERSIONS::{added_versions}")

    save_version_file(version_type, version_data)

if __name__ == "__main__":
    args = parser.parse_args()
    run(args.type)