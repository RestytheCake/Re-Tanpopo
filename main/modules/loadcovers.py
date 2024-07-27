import json
from main.modules.path import anilist_info


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


def print_names(watchtype=""):
    print(f"Function print_names called with watchtype: {watchtype}")
    urllist = []
    print("Initialized urllist as an empty list")

    with open(anilist_info, "r") as file:
        print(f"Opened file: {anilist_info}")
        data = json.load(file)
        print("Loaded JSON data from file")

        currently_watching = data.get(watchtype, [])
        print(f"Retrieved currently watching list for '{watchtype}': {currently_watching}")

        for item in currently_watching:
            cover_image = item["Titles"]["Romaji"]
            if cover_image:
                urllist.append(cover_image)
                print(f"Appended cover image to urllist: {cover_image}")

    print(f"Returning urllist: {urllist}")
    return urllist

