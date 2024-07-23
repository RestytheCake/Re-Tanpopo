import customtkinter as ctk


def create_recognition_frame(self):
    recognition_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Recognition"] = recognition_frame
    ctk.CTkLabel(recognition_frame, text="Recognition", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
