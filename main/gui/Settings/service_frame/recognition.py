import customtkinter as ctk

from main.gui.Settings.service_frame.template import create_notebook_frame


# TODO: What does this even mean??
def create_recognition_frame(self, name="Recognition"):
    print(f"Calling Notebook Func for: {name}")
    notebook = create_notebook_frame(self, self.content_frame, name)

    # Recognition Tab
    recognition_tab = notebook.add(name)
    ctk.CTkLabel(recognition_tab, text="Tails Doing", font=ctk.CTkFont(size=16)).pack(anchor="w")
    print(f"Create Notebook for: {name}")

