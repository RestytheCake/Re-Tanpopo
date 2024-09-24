import json
from main.modules.path import anilist_info

import json


def get_anime_data(watchtype=""):
    print(f"Function get_anime_data called with watchtype: {watchtype}")
    anime_data = {
        "cover_images": [],
        "titles": [],
        "descriptions": [],
        "ID": [],
    }
    print("Initialized anime_data as an empty dictionary with keys: cover_images, titles, descriptions, ID")

    with open(anilist_info, "r") as file:
        print(f"Opened file: anilist_info.json")
        data = json.load(file)
        print("Loaded JSON data from file")

        currently_watching = data.get(watchtype, [])
        print(f"Retrieved currently watching list for '{watchtype}': {currently_watching}")

        for item in currently_watching:
            cover_image = item.get("CoverImage")
            titles = item.get("Titles", {}).get("English", item.get("Titles", {}).get("Romaji", ""))
            description = item.get("Description")
            id = item.get("ID")

            if cover_image:
                anime_data["cover_images"].append(cover_image)
                print(f"Appended cover image to anime_data['cover_images']: {cover_image}")
            if titles:
                anime_data["titles"].append(titles)
                print(f"Appended title to anime_data['titles']: {titles}")
            if description:
                anime_data["descriptions"].append(description)
                print(f"Appended description to anime_data['descriptions']: {description}")
            if id:
                anime_data["ID"].append(id)
                print(f"Appended ID to anime_data['ID']: {id}")

    print(f"Returning anime_data: {anime_data}")
    return anime_data


def print_cover_images(watchtype=""):
    print(f"Function print_cover_images called with watchtype: {watchtype}")
    urllist = []
    print("Initialized urllist as an empty list")

    with open(anilist_info, "r") as file:
        print(f"Opened file: {anilist_info}")
        data = json.load(file)
        print("Loaded JSON data from file")

        currently_watching = data.get(watchtype, [])
        print(f"Retrieved currently watching list for '{watchtype}': {currently_watching}")

        for item in currently_watching:
            cover_image = item.get("CoverImage")
            if cover_image:
                urllist.append(cover_image)
                print(f"Appended cover image to urllist: {cover_image}")

    print(f"Returning urllist: {urllist}")
    return urllist