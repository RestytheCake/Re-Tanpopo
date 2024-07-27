import customtkinter as ctk


# TODO: Add a Template for bad coder


def create_notebook_frame(self, tab, name):
    print(f"Creating Notebook Template for: {name}")
    notebook_frame = ctk.CTkFrame(tab)
    self.frames[name] = notebook_frame
    notebook = ctk.CTkTabview(notebook_frame)
    notebook.pack(fill="both", expand=True)
    print(f"Finished Notebook Template: {name}")
    return notebook


