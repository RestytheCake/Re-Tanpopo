import json

import customtkinter as ctk
from customtkinter import filedialog
from localStoragePy import localStoragePy
import subprocess

from sub.modules.filepath import Player


def create_player_frame(self):
    player_frame = ctk.CTkFrame(self.content_frame)
    self.frames["Player"] = player_frame  # wont cap p fuck u vscode
    notebook = ctk.CTkTabview(player_frame)
    notebook.pack(fill="both", expand=True)

    # Player Tab
    mvp_player_tab = notebook.add("MPV Player")
    mpv_player(self, mvp_player_tab)


# TODO: Add more Video Player Options
def play_test_video():
    ls_settings = localStoragePy("Settings", "json")
    playerloc = ls_settings.getItem("mpv")
    print(playerloc)
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(playerloc + " " + youtube_url)
    try:
        subprocess.run([playerloc, youtube_url])
    except Exception as e:
        print(f"An error occurred: {e}")


def mpv_player(self, tab):
    self.btn = ctk.CTkButton(tab, text="choose player", anchor="w", command=set_mpv_player)
    self.btn.pack(fill="x", pady=5, padx=7)
    self.btn = ctk.CTkButton(tab, text="play test video", anchor="w", command=play_test_video)
    self.btn.pack(fill="x", pady=5, padx=7)


def set_mpv_player():
    print("selecting video player")
    selectfile("mpv")


def selectfile(playername: str):
    # Open the file dialog and filter for exe files
    if playername == "mpv":
        playerloc = filedialog.askopenfilename(
            title="Select an EXE file",
            filetypes=[("Executable files", "*.exe")]
        )
    else:
        playerloc = None
        print("Not Supported")

    if playerloc:
        print(playerloc)

        # Load the JSON file
        with open(Player, 'r') as file:
            data = json.load(file)

        # Update the "player" key with the selected file location
        data[playername] = playerloc

        # Write the updated JSON data back to the file
        with open(Player, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Updated mpc location: {playerloc} in {Player}")

        print("Here comes the cool Part")
        ls_settings = localStoragePy("Settings", "json")
        ls_settings.setItem(playername, playerloc)
        print(f"Saved: {playername} with the location: {ls_settings.getItem(playername)} in {[ls_settings]}")
