import customtkinter as ctk

from main.gui.Settings.service_frame.template import create_notebook_frame


# TODO: still dont know what should be in here, library like the main page with watching ?. Makes no sense


def create_library_frame(self, name="Library"):
    print(f"Calling Notebook Func for: {name}")
    notebook = create_notebook_frame(self, self.content_frame, name)

    # {name} Tab / works like a charm (:
    recognition_tab = notebook.add(name)
    ctk.CTkLabel(recognition_tab, text="Tails Doing", font=ctk.CTkFont(size=16)).pack(anchor="w")
    print(f"Create Notebook for: {name}")
