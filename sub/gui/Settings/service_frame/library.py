import customtkinter as ctk

def create_library_frame(self):
    library_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Library"] = library_frame
    ctk.CTkLabel(library_frame, text="Library", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
