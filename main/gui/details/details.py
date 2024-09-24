import json
import os
import re
import subprocess
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import CTkListbox
from PIL import Image
from main.modules.globalmanager import GlobalManager
from main.modules.path import Player, series_locations


def back_to_main():
    animeviewer_instance = GlobalManager.get_animeviewer_instance()
    if animeviewer_instance:
        animeviewer_instance.reload()
    else:
        print("AnimeViewer instance is not initialized")


class AnimeDetails(ctk.CTkFrame):
    IMAGE_SIZE = (200, 150)
    DESCRIPTION_WRAP_LENGTH = 300
    PADDING = 10
    BORDER_WIDTH = 2

    # Define the player variable
    Player = "path/to/media/player"  # Replace with the actual path or command

    def __init__(self, frame, title=None, description=None, image=None, anime_id=None, **kwargs):
        super().__init__(frame, **kwargs)
        self.title = title
        self.description = description
        self.image = ctk.CTkImage(light_image=image, dark_image=image, size=self.IMAGE_SIZE)
        self.anime_id = anime_id
        self.description_visible = False

        self.left_frame = None
        self.right_frame = None
        self.top_right_frame = None
        self.bottom_right_frame = None
        self.description_frame = None
        self.description_label = None
        self.episode_list = None
        self.episode_files = []  # Store episode file paths

        self._create_widgets()
        self.update_episode_list()

    def _create_widgets(self):
        self._setup_layout()
        self._create_left_frame()
        self._create_right_frame()

    def _setup_layout(self):
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=2, uniform="a")
        self.grid_rowconfigure(0, weight=1)

    def _create_left_frame(self):
        self.left_frame = ctk.CTkFrame(
            self, fg_color="transparent", border_width=self.BORDER_WIDTH, border_color="grey", corner_radius=10
        )
        self.left_frame.grid(row=0, column=0, padx=self.PADDING, pady=self.PADDING, sticky="nsew")

        self._create_cover_label()
        self._create_title_label()
        self._create_id_label()
        self._create_episode_list()

    def _create_cover_label(self):
        cover_label = ctk.CTkLabel(self.left_frame, image=self.image, text="", corner_radius=10)
        cover_label.grid(row=0, column=0, pady=(self.PADDING, 5), padx=self.PADDING, sticky="nw")

    def _create_title_label(self):
        title_label = ctk.CTkLabel(
            self.left_frame, text=self.title, font=ctk.CTkFont(size=20, weight="bold"), text_color="#333333"
        )
        title_label.grid(row=1, column=0, pady=(5, 3), padx=self.PADDING, sticky="nw")

    def _create_id_label(self):
        id_label = ctk.CTkLabel(
            self.left_frame, text=f"ID: {self.anime_id}", font=ctk.CTkFont(size=12, slant="italic"), text_color="grey"
        )
        id_label.grid(row=2, column=0, padx=self.PADDING, pady=(3, 10), sticky="nw")

    def _create_episode_list(self):
        self.episode_list = CTkListbox.CTkListbox(self.left_frame, width=200, height=250)
        self.episode_list.grid(row=3, column=0, pady=10, padx=self.PADDING, sticky="nw")
        self.episode_list.bind("<<ListboxSelect>>", self.play_selected_episode)

    def _create_right_frame(self):
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, padx=self.PADDING, pady=self.PADDING, sticky="nsew")

        self._create_top_right_frame()
        self._create_bottom_right_frame()

    def _create_top_right_frame(self):
        self.top_right_frame = ctk.CTkFrame(
            self.right_frame, fg_color="transparent", border_width=self.BORDER_WIDTH, border_color="grey",
            corner_radius=10
        )
        self.top_right_frame.grid(row=0, column=0, sticky="nsew", padx=self.PADDING, pady=(0, 5))

        back_button = ctk.CTkButton(
            self.top_right_frame, text="Back to Main", command=back_to_main, corner_radius=10
        )
        back_button.grid(row=0, column=0, pady=self.PADDING, padx=self.PADDING, sticky="nw")

    def _create_bottom_right_frame(self):
        self.bottom_right_frame = ctk.CTkFrame(
            self.right_frame, fg_color="transparent", border_width=self.BORDER_WIDTH, border_color="grey",
            corner_radius=10
        )
        self.bottom_right_frame.grid(row=1, column=0, sticky="nsew", padx=self.PADDING, pady=(5, 0))

        set_location_button = ctk.CTkButton(
            self.bottom_right_frame, text="Set Folder Location", command=self.set_folder_location, corner_radius=10
        )
        set_location_button.grid(row=0, column=0, pady=self.PADDING, padx=self.PADDING, sticky="new")

        toggle_description_button = ctk.CTkButton(
            self.bottom_right_frame, text="Show Description", command=self.toggle_description, corner_radius=10
        )
        toggle_description_button.grid(row=1, column=0, pady=self.PADDING, padx=self.PADDING, sticky="new")

        self._create_description_frame()

    def _create_description_frame(self):
        self.description_frame = ctk.CTkFrame(self.bottom_right_frame, fg_color="transparent")
        self.description_frame.grid(row=2, column=0, pady=self.PADDING, padx=self.PADDING, sticky="n")
        self.description_frame.grid_remove()

        description_label_title = ctk.CTkLabel(
            self.description_frame, text="Description:", font=ctk.CTkFont(size=16, weight="bold"), text_color="#333333"
        )
        description_label_title.grid(row=0, column=0, pady=5, sticky="w")

        self.description_label = ctk.CTkLabel(
            self.description_frame, text=self.description, wraplength=self.DESCRIPTION_WRAP_LENGTH, justify="left",
            text_color="#666666"
        )
        self.description_label.grid(row=1, column=0, pady=5, sticky="w")

    def update_episode_list(self):
        if self.episode_list.size() > 0:
            self.episode_list.delete("all")

        directory = self.read_file_location(self.anime_id)
        if directory:
            episodes = self.get_episodes_from_directory(directory)
            self.episode_files = []  # Clear previous episode files
            for episode in episodes:
                self.episode_list.insert(tk.END, episode['display'])
                self.episode_files.append(episode['file'])  # Populate episode_files list
            print(f"Episode files: {self.episode_files}")  # Debugging statement
        else:
            print("No directory found for the anime ID.")

    def read_file_location(self, anime_id):
        try:
            with open(series_locations, "r") as file:
                data = json.load(file)
                return data.get(str(anime_id))
        except (FileNotFoundError, json.JSONDecodeError):
            print("series_locations.json not found or empty.")
        return None

    def get_episodes_from_directory(self, directory):
        episode_pattern = re.compile(r'[Ee][Pp]?(\d{1,3})')
        episodes = []

        for filename in os.listdir(directory):
            match = episode_pattern.search(filename)
            if match:
                episode_number = match.group(1)
                episodes.append({
                    'display': f"Episode {int(episode_number)}",
                    'file': os.path.join(directory, filename)
                })

        episodes.sort(key=lambda x: int(re.search(r'\d+', x['display']).group()))
        return episodes

    def play_selected_episode(self, event):
        selection = self.episode_list.curselection()
        print(f"Selection: {selection}")  # Debugging statement
        if selection:
            index = selection
            print(f"Selected index: {index}")  # Debugging statement

            # Check if index is within bounds of episode_files
            if 0 <= index < len(self.episode_files):
                episode_path = self.episode_files[index]
                print(f"Playing episode at: {episode_path}")  # Debugging statement

                # Run the player with the episode path
                with open(Player, 'r') as file:
                    data = json.load(file)

                # Extract the value associated with the "mpv" key
                player_path = data.get('mpv')

                if player_path:
                    print(f"MPV Path: {player_path}")
                else:
                    print("Key 'mpv' not found in the JSON file. The Player MPV was not set in the settings page")
                subprocess.run([player_path, episode_path])
            else:
                print(f"Index {index} is out of range for episode files.")
        else:
            print("No selection detected.")

    def set_folder_location(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            with open(series_locations, "r+") as file:
                data = json.load(file)
                data[str(self.anime_id)] = folder_path
                file.seek(0)
                json.dump(data, file, indent=4)

    def toggle_description(self):
        if self.description_visible:
            self.description_frame.grid_remove()
        else:
            self.description_frame.grid()
        self.description_visible = not self.description_visible


import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog

