import customtkinter as ctk


def create_application_frame(self):
    application_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Application"] = application_frame
    ctk.CTkLabel(application_frame, text="Application", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
