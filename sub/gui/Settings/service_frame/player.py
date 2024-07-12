import customtkinter as ctk


def create_player_frame(self):
    player_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Player"] = player_frame  # wont cap p fuck u vscode
    notebook = ctk.CTkTabview(player_frame)
    notebook.pack(fill="both", expand=True)

    # Player Tab
    credits_tab = notebook.add("Player")

    btn = ctk.CTkButton(credits_tab, text="choose player", anchor="w", command=set_player)  # cap c in choose
    btn.pack(fill="x", pady=5, padx=7)


def set_player():
    print("selecting video player")