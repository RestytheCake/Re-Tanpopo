from datetime import datetime
from pypresence import Presence
import time
from localStoragePy import localStoragePy  # Database

# Initialize the local storage and retrieve the username
ls = localStoragePy("Tanpopo Rewrite", "json")
username = ls.getItem("username")
print(username)


class DiscordRPC:
    def __init__(self):
        print("Init rpc")
        self.rpc = Presence(client_id="827136996198580244")
        self.rpc.connect()
        self.menu()

    def menu(self):
        self.rpc.update(
            details="In Menu",
            state="Finding something to watch",
            large_image="anilist",
            small_image="anilist",
            large_text="AniList",
            small_text="anilist",
            start=int(datetime.now().timestamp()),
            buttons=[{"label": "Anilist", "url": f"https://anilist.co/user/{username}"},
                     {"label": "Tanpopo", "url": "https://github.com/snowythevulpix/Tanpopo"}]
        )

    def update(self, details, state, large_image, small_image, large_text, small_text):
        print("update rpc")
        self.rpc.update(
            details=details,
            state=state,
            large_image=large_image,
            small_image=small_image,
            large_text=large_text,
            small_text=small_text,
            start=int(datetime.now().timestamp()),
            buttons=[{"label": "Anilist", "url": f"https://anilist.co/user/{username}"},
                     {"label": "Tanpopo", "url": "https://github.com/snowythevulpix/Tanpopo"}]
        )

    def close(self):
        self.rpc.close()

