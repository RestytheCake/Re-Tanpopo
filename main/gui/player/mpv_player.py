import os
from main.modules.path import get_project_root

# Add the directory containing mpv DLLs to PATH
dll_directory = rf"{get_project_root()}/mpv"  # Replace with the actual path to your mpv DLLs
print(dll_directory)
os.environ["PATH"] = dll_directory + os.pathsep + os.environ["PATH"]

import tkinter as tk
import customtkinter as ctk
from mpv import MPV


class MPVPlayerWindow:
    def __init__(self, parent, episode_path):
        # Create a new Toplevel window
        self.player_window = tk.Toplevel(parent)
        self.player_window.title("MPV Player")
        self.player_window.geometry("800x600")  # Set window size

        # Create a frame in the new window to embed MPV
        self.video_frame = tk.Frame(self.player_window, width=800, height=500, bg="black")
        self.video_frame.pack(pady=20)

        # Initialize MPV player with the frame widget ID
        self.mpv_player = MPV(wid=str(self.video_frame.winfo_id()))

        # Play the selected episode
        self.mpv_player.play(episode_path)