import json

import customtkinter as ctk
from localStoragePy import localStoragePy
from sub.modules.filepath import anilist_info
from sub.modules.globalmanager import GlobalManager


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

    bottom_frame_instance = GlobalManager.get_bottom_frame_instance()
    top_frame_instance = GlobalManager.get_top_frame_instance()
    settings_instance = GlobalManager.get_settings_window_instance()

    if bottom_frame_instance:
        bottom_frame_instance.update_settings()
    if top_frame_instance:
        top_frame_instance.update_settings()
    if settings_instance:
        settings_instance.update_settings()
    else:
        print("Frame instance is not initialized")


    print("Done!!!")

