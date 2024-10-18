from main.modules.api import load_anime_api
from main.modules.progress import Load_Progress_API


def load_APIs():
    print("Loading APIs...")
    Load_Progress_API()
    load_anime_api()
    return None  # Just calls the other Code
