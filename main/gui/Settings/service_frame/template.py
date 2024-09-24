import customtkinter as ctk


# TODO: Add a Template for bad coder


def create_notebook_frame(self, tab, name):
    print(f"Creating Notebook Template for: {name}")
    notebook_frame = ctk.CTkFrame(tab)  # Create a frame for the notebook
    self.frames[name] = notebook_frame # Add the frame to the frames dictionary
    notebook = ctk.CTkTabview(notebook_frame) # Create a notebook
    notebook.pack(fill="both", expand=True) # Pack the notebook
    print(f"Finished Notebook Template: {name}") # Print a message to the console
    return notebook # Return the notebook


