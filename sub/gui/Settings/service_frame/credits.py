import customtkinter as ctk


def create_credits_frame(self):
    credits_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Credits"] = credits_frame
    notebook = ctk.CTkTabview(credits_frame)
    notebook.pack(fill="both", expand=True)

    # Credits Tab
    credits_tab = notebook.add("Credits")
    ctk.CTkLabel(credits_tab, text="Owner", font=ctk.CTkFont(size=16)).pack(anchor="w")
    ctk.CTkLabel(credits_tab, text="--- ninestails").pack(anchor="w", pady=(5, 2))
    ctk.CTkLabel(credits_tab, text="Maintainer", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
    ctk.CTkLabel(credits_tab, text="--- resty1337", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w",
                                                                                                   padx=10)
    ctk.CTkLabel(credits_tab, text="Designer", font=ctk.CTkFont(size=16)).pack(anchor="w")
    ctk.CTkLabel(credits_tab, text="resty", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10)
