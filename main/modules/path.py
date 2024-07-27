import json
from pathlib import Path
import shutil


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


# User Data Path
TANPOPO_DIR = Path.home() / 'AppData/Roaming/Tanpopo'
MEDIA_INFO_DIR = TANPOPO_DIR / 'media_info'
anilist_info = MEDIA_INFO_DIR / 'anilist.json'
kitsu_info = MEDIA_INFO_DIR / 'kitsu.json'
myanimelist_info = MEDIA_INFO_DIR / 'myanimelist.json'
series_locations = TANPOPO_DIR / 'series_locations.json'
Player = MEDIA_INFO_DIR / 'player.json'

# Folder Paths
IMG_DIR = get_project_root() / "main" / "img"


def ensure_files_exist():
    """Ensure that all necessary directories and files exist. Create them if they don't."""
    print(f"Current working directory: {Path.home()}")

    # Define the files to check and their default content
    files = {
        anilist_info: {},
        kitsu_info: {},
        myanimelist_info: {},
        series_locations: {},
        Player: {}
    }

    # Ensure the main directory and media_info directory exist
    if not TANPOPO_DIR.exists():
        try:
            TANPOPO_DIR.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {TANPOPO_DIR}")
        except Exception as e:
            print(f"Error creating directory {TANPOPO_DIR}: {e}")

    if not MEDIA_INFO_DIR.exists():
        try:
            MEDIA_INFO_DIR.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {MEDIA_INFO_DIR}")
        except Exception as e:
            print(f"Error creating directory {MEDIA_INFO_DIR}: {e}")

    # Check and create files as needed
    for file_path, default_content in files.items():
        if not file_path.exists():
            try:
                # Create an empty file with default content
                with open(file_path, 'w') as file:
                    json.dump(default_content, file)
                    file.close()
                print(f"Created file: {file_path}")
            except Exception as e:
                print(f"Error creating file {file_path}: {e}")


def remove_files_and_directories():
    """Remove all created files and directories."""
    files = [
        anilist_info,
        kitsu_info,
        myanimelist_info,
        series_locations,
        Player
    ]

    # Remove files
    for file_path in files:
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Removed file: {file_path}")
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")

    # Remove directories if empty
    if MEDIA_INFO_DIR.exists() and not any(MEDIA_INFO_DIR.iterdir()):
        try:
            MEDIA_INFO_DIR.rmdir()
            print(f"Removed directory: {MEDIA_INFO_DIR}")
        except Exception as e:
            print(f"Error removing directory {MEDIA_INFO_DIR}: {e}")

    if TANPOPO_DIR.exists() and not any(TANPOPO_DIR.iterdir()):
        try:
            TANPOPO_DIR.rmdir()
            print(f"Removed directory: {TANPOPO_DIR}")
        except Exception as e:
            print(f"Error removing directory {TANPOPO_DIR}: {e}")
