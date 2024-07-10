import json


def print_cover_images(json_file_path='media_info.json', watchtype=""):
    urllist = []
    with open(json_file_path, "r") as file:
        data = json.load(file)

        currently_watching = data.get(watchtype, [])
        for item in currently_watching:
            cover_image = item.get("CoverImage")
            if cover_image:
                urllist.append(cover_image)
        return urllist


def print_names(json_file_path='media_info.json'):
    urllist = []
    with open(json_file_path, "r") as file:
        data = json.load(file)

        currently_watching = data.get("Currently Watching", [])
        for item in currently_watching:
            cover_image = item["Titles"]["Romaji"]
            if cover_image:
                urllist.append(cover_image)
        print(urllist)
        return urllist
