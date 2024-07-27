import customtkinter as ctk
from localStoragePy import localStoragePy

from main.gui.Settings.service_frame.template import create_notebook_frame
from main.modules.api import Load_API
from main.gui.Auth_Window import authwindow


def api():
    Load_API()


def create_services_frame(self, name="Services"):
    print(f"Calling Notebook Func for: {name}")
    notebook = create_notebook_frame(self, self.content_frame, name)

    # Main Tab
    main_tab = notebook.add("Main")
    create_main_tab(self, main_tab)

    # AniList Tab
    anilist_tab = notebook.add("AniList")
    create_anilist_tab(self, anilist_tab)

    print(f"Create Notebook for: {name}")


def create_main_tab(self, tab):
    ls_settings = localStoragePy("Settings", "json")
    ls = localStoragePy("Tanpopo Rewrite", "json")

    if ls.getItem('user_id') is None:
        ctk.CTkLabel(tab, text="Click the Button to Login").pack(anchor="w", pady=(5, 2))
        auth_button = ctk.CTkButton(tab, text="Login", font=ctk.CTkFont(size=12, weight="bold"),
                                    command=authwindow.ToplevelWindow)
        auth_button.pack(anchor="w", pady=(10, 5))
    else:
        ctk.CTkLabel(tab, text="User Information", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w",
                                                                                                  pady=(10, 5), padx=10)

        # Username and additional data display with padding
        user_frame = ctk.CTkFrame(tab)
        user_frame.pack(anchor="w", pady=(5, 10), padx=10, fill="x")
        ctk.CTkLabel(user_frame, text="Logged in as:", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(5, 2), padx=10)
        ctk.CTkLabel(user_frame, text=f"{ls.getItem('username')}   ", font=ctk.CTkFont(size=14, slant="italic")).pack(
            anchor="w", pady=(2, 5), padx=20)

        # Additional user data (placeholder)
        ctk.CTkLabel(user_frame, text="Additional User Data:", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(5, 2),
                                                                                               padx=10)
        ctk.CTkLabel(user_frame, text="Data Placeholder 1", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(2, 2),
                                                                                            padx=20)
        ctk.CTkLabel(user_frame, text="Data Placeholder 2", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(2, 2),
                                                                                            padx=20)

        # Refresh Button
        button_frame = ctk.CTkFrame(tab)
        button_frame.pack(anchor="w", pady=(5, 10), padx=10, fill="x")
        ctk.CTkButton(button_frame, text="Refresh Anilist", font=ctk.CTkFont(size=12, weight="bold"),
                      command=api).pack(anchor="center", pady=(10, 5))
        ctk.CTkLabel(button_frame, text="Fetching data may take a few seconds.", font=ctk.CTkFont(size=12)).pack(
            anchor="center", pady=(5, 2))

        # Logout and reload instructions
        instruction_frame = ctk.CTkFrame(tab)
        instruction_frame.pack(anchor="w", pady=(5, 10), padx=10, fill="x")
        ctk.CTkLabel(instruction_frame, text="Use 'Clear' to Logout", font=ctk.CTkFont(size=14)).pack(anchor="center",
                                                                                                      pady=(5, 2))


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
