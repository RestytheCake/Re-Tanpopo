import customtkinter as ctk


# TODO: still dont know what should be in here, library like the main page with watching ?. Makes no sense
def create_library_frame(self):
    library_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Library"] = library_frame
    ctk.CTkLabel(library_frame, text="Library", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
