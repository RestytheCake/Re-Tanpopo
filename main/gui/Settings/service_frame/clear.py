import json

import customtkinter as ctk
from localStoragePy import localStoragePy
from main.modules.path import anilist_info
from main.modules.globalmanager import GlobalManager
from main.modules.refresher import refresh_global


def create_clear_frame(self):
    clear_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Clear"] = clear_frame
    notebook = ctk.CTkTabview(clear_frame)
    notebook.pack(fill="both", expand=True)

    # Credits Tab
    credits_tab = notebook.add("clear")

    btn = ctk.CTkButton(credits_tab, text="Clear All Data", anchor="w", command=clear_all)
    btn.pack(fill="x", pady=5, padx=7)


def clear_all():
    print("Start Cleaning Process")
    ls_settings = localStoragePy("Settings", "json")
    ls = localStoragePy("Tanpopo Rewrite", "json")
    ls_settings.clear()
    ls_settings.setItem("AniList/watching", False)
    ls_settings.setItem("AniList/planned", False)
    ls_settings.setItem("AniList/rewatched", False)
    ls_settings.setItem("AniList/completed", False)
    ls.clear()
    with open(anilist_info, 'w') as file:
        json.dump({}, file)
    refresh_global()

    print("Done!!!")

