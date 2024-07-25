import customtkinter as ctk

# TODO: IDK What to add here, your Job
def create_advanced_frame(self):
    advanced_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Advanced"] = advanced_frame
    ctk.CTkLabel(advanced_frame, text="Advanced", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
