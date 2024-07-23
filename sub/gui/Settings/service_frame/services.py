import customtkinter as ctk
from localStoragePy import localStoragePy
from sub.modules.api import Load_API
from sub.gui.Auth_Window import authwindow


def api():
    Load_API()


def create_services_frame(self):
    services_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Services"] = services_frame

    notebook = ctk.CTkTabview(services_frame)
    notebook.pack(fill="both", expand=True)

    # Main Tab
    main_tab = notebook.add("Main")
    create_main_tab(self, main_tab)

    # AniList Tab
    anilist_tab = notebook.add("AniList")
    create_anilist_tab(self, anilist_tab)


def create_main_tab(self, tab):
    ls_settings = localStoragePy("Settings", "json")
    ls = localStoragePy("Tanpopo Rewrite", "json")
    ctk.CTkLabel(tab, text="Anime List", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

    if ls.getItem('user_id') is None:
        ctk.CTkLabel(tab, text="Click the Button to Login").pack(anchor="w", pady=(5, 2))
        auth_button = ctk.CTkButton(tab, text="Login", font=ctk.CTkFont(size=12, weight="bold"),
                                    command=authwindow.ToplevelWindow)
        auth_button.pack(anchor="w", pady=(10, 5))
    else:
        button = ctk.CTkButton(tab, text="Refresh Anilist", font=ctk.CTkFont(size=12, weight="bold"),
                               command=api)
        button.pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(tab, text="It will take some seconds to fetch the Data").pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(tab, text="~~~~~~~~~~~~~~~~~~~").pack(anchor="w", pady=(10, 2))
        ctk.CTkLabel(tab, text="Use Clear to Logout").pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(tab, text="Reload afterwarts").pack(anchor="w", pady=(5, 2))


def create_anilist_tab(self, tab):
    ls_settings = localStoragePy("Settings", "json")
    ls = localStoragePy("Tanpopo Rewrite", "json")
    ctk.CTkLabel(tab, text="Select Watch Lists", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

    self.watching_var = ctk.BooleanVar(value=ls_settings.getItem("AniList/watching"))
    watching_checkbox = ctk.CTkCheckBox(tab, text="Watching", variable=self.watching_var)
    watching_checkbox.pack(anchor="w", pady=(0, 20))

    self.planned_var = ctk.BooleanVar(value=ls_settings.getItem("AniList/planned"))
    planned_checkbox = ctk.CTkCheckBox(tab, text="Planned to Watch", variable=self.planned_var)
    planned_checkbox.pack(anchor="w", pady=(0, 20))

    self.rewatched_var = ctk.BooleanVar(value=ls_settings.getItem("AniList/rewatched"))
    rewatched_checkbox = ctk.CTkCheckBox(tab, text="Rewatching", variable=self.rewatched_var)
    rewatched_checkbox.pack(anchor="w", pady=(0, 20))

    self.completed_var = ctk.BooleanVar(value=ls_settings.getItem("AniList/completed"))
    completed_checkbox = ctk.CTkCheckBox(tab, text="Completed", variable=self.completed_var)
    completed_checkbox.pack(anchor="w", pady=(0, 20))



