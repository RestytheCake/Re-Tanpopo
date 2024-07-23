import customtkinter as ctk


def create_version_frame(self):
    version_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Version"] = version_frame
    notebook = ctk.CTkTabview(version_frame)
    notebook.pack(fill="both", expand=True)

    # Version Tab
    version_tab = notebook.add("Version")
    ctk.CTkLabel(version_tab, text="Version - Alpha", font=ctk.CTkFont(size=16)).pack(anchor="w")
    ctk.CTkLabel(version_tab, text="0.0.0.0.0.0.0.0.0.0.01").pack(anchor="w", pady=(5, 2))
