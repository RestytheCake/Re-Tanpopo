import json

def print_cover_images(json_file_path):
    urllist = []
    with open(json_file_path, "r") as file:
        data = json.load(file)

        currently_watching = data.get("Currently Watching", [])
        for item in currently_watching:
                cover_image = item.get("CoverImage")
                if cover_image:
                    urllist.append(cover_image)
                    print(cover_image)
        return urllist