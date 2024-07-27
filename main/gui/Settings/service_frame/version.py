import customtkinter as ctk

from main.gui.Settings.service_frame.template import create_notebook_frame


def create_version_frame(self, name="Version"):
    print(f"Calling Notebook Func for: {name}")
    notebook = create_notebook_frame(self, self.content_frame, name)

    # Version Tab
    version_tab = notebook.add(name)
    ctk.CTkLabel(version_tab, text="Version - Pre Alpha", font=ctk.CTkFont(size=16)).pack(anchor="w")
    ctk.CTkLabel(version_tab, text="0.0.0.0.0.0.0.2").pack(anchor="w", pady=(5, 2))
    print(f"Create Notebook for: {name}")


