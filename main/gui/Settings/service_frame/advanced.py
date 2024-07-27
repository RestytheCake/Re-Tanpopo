import customtkinter as ctk

from main.gui.Settings.service_frame.template import create_notebook_frame


# TODO: IDK What to add here, your Job
def create_advanced_frame(self, name="Advanced"):
    print(f"Calling Notebook Func for: {name}")
    notebook = create_notebook_frame(self, self.content_frame, name)

    # Version Tab
    advanced_tab = notebook.add(name)
    ctk.CTkLabel(advanced_tab, text="Tails Doing", font=ctk.CTkFont(size=16)).pack(anchor="w")
    print(f"Create Notebook for: {name}")



