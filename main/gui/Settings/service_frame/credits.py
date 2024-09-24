import customtkinter as ctk

from main.gui.Settings.service_frame.template import create_notebook_frame


def create_credits_frame(self, name="Credits"):
    print(f"Calling Notebook Func for: {name}")
    notebook = create_notebook_frame(self, self.content_frame, name)

    # TODO: Update the names and styles
    # Credits Tab
    credits_tab = notebook.add("Credits")
    ctk.CTkLabel(credits_tab, text="Owner", font=ctk.CTkFont(size=16)).pack(anchor="w")
    ctk.CTkLabel(credits_tab, text="--- ninestails").pack(anchor="w", pady=(5, 2))
    ctk.CTkLabel(credits_tab, text="Maintainer", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
    ctk.CTkLabel(credits_tab, text="--- resty1337", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w",padx=10)
    ctk.CTkLabel(credits_tab, text="Designer", font=ctk.CTkFont(size=16)).pack(anchor="w")
    ctk.CTkLabel(credits_tab, text="resty", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10)
    ctk.CTkLabel(credits_tab, text="Frenchy making Fixes", font=ctk.CTkFont(size=16)).pack(anchor="w")
    ctk.CTkLabel(credits_tab, text="Nixuge", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10)

    print(f"Create Notebook for: {name}")