import customtkinter as ctk

from main.gui.Settings.service_frame.template import create_notebook_frame


# TODO: Same as advanced.py
def create_application_frame(self, name="Application"):
    print(f"Calling Notebook Func for: {name}")
    notebook = create_notebook_frame(self, self.content_frame, name)

    # Version Tab
    application_tab = notebook.add(name)
    ctk.CTkLabel(application_tab, text="Tails Doing", font=ctk.CTkFont(size=16)).pack(anchor="w")
    print(f"Create Notebook for: {name}")