# Content from /home/arthur/Code/PycharmProjects/Tanpopo rewrite/main/gui/AnimeViewer.py
from customtkinter import *
from localStoragePy import localStoragePy  # Database
from main.gui.details.details import AnimeDetails
from main.gui.main_frame.bottom_frame.bottom_frame import Bottom_Frame
from main.gui.main_frame.top_frame.top_frame import Top_Frame
from main.modules.colors import grey, darkgrey
from main.modules.globalmanager import GlobalManager

# Initialize Database
ls = localStoragePy("Tanpopo Rewrite", "json")

class AnimeViewer:
    def __init__(self, master):
        self.top_frame = None
        self.video_frame = None
        print("Anime Viewer")
        self.master = master
        self.master.title("Tanpopo")
        self.master.configure(fg_color=grey)
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        # Make the main window resizable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.main_frame = CTkFrame(self.master, fg_color=grey)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.init_frames()
        GlobalManager.set_animeviewer_instance(self)  # Ensure the instance is set here

    def init_frames(self):
        # Initialize Top Frame
        self.top_frame = CTkFrame(self.main_frame, fg_color=grey)
        top_frame_instance = Top_Frame(self.top_frame)
        GlobalManager.set_top_frame_instance(top_frame_instance)
        self.top_frame.grid(row=0, column=0, sticky="ew")

        # Initialize Bottom Frame
        self.video_frame = CTkFrame(self.main_frame, fg_color=darkgrey)
        bottom_frame_instance = Bottom_Frame(self.video_frame)
        GlobalManager.set_bottom_frame_instance(bottom_frame_instance)
        self.video_frame.grid(row=1, column=0, sticky="nsew")

    def details_frame(self, title, description, image, anime_id):
        self.clear()  # Clear the main_frame
        details_frame_instance = AnimeDetails(self.main_frame, title=title, description=description, image=image, anime_id=anime_id)
        details_frame_instance.pack(fill="both", expand=True)
        GlobalManager.set_details_frame_instance(details_frame_instance)

    def reload(self):
        # Clear the main_frame and reinitialize all components
        self.clear()
        self.init_frames()

    def clear(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Content from /home/arthur/Code/PycharmProjects/Tanpopo rewrite/main/gui/details/details.py
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
            self.top_right_frame, text="Back to Main", command=self.back_to_main, corner_radius=10
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

    def back_to_main(self):
        animeviewer_instance = GlobalManager.get_animeviewer_instance()
        if animeviewer_instance:
            animeviewer_instance.reload()
        else:
            print("AnimeViewer instance is not initialized")


# Content from /home/arthur/Code/PycharmProjects/Tanpopo rewrite/main/modules/refresher.py
from main.gui.details.details import AnimeDetails
from main.modules.globalmanager import GlobalManager


def refresh_global():
    bottom_frame_instance = GlobalManager.get_bottom_frame_instance()
    top_frame_instance = GlobalManager.get_top_frame_instance()
    settings_instance = GlobalManager.get_settings_window_instance()

    if bottom_frame_instance:
        bottom_frame_instance.update_settings()
    if top_frame_instance:
        top_frame_instance.update_settings()
    if settings_instance:
        settings_instance.update_settings()
    else:
        print("Refresh Frame instance is not initialized")
    print("Refresh done!")


def clear_main():
    animeviewer_instance = GlobalManager.get_animeviewer_instance()
    if animeviewer_instance:
        animeviewer_instance.clear()
    else:
        print("Clear Frame instance is not initialized")
    print("Clear done!")


def change_page_to_detail(title, desc, img, anime_id):
    animeviewer_instance = GlobalManager.get_animeviewer_instance()
    if animeviewer_instance:
        clear_main()
        animeviewer_instance.details_frame(title, desc, img, anime_id)
    else:
        print("AnimeViewer instance is not initialized")


# Content from /home/arthur/Code/PycharmProjects/Tanpopo rewrite/main/modules/globalmanager.py
class GlobalManager:
    _instance = None
    animeviewer_instance = None
    bottom_frame_instance = None
    top_frame_instance = None
    settings_window_instance = None
    details_frame_instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_animeviewer_instance(cls):
        return cls.animeviewer_instance

    @classmethod
    def set_animeviewer_instance(cls, AnimeViewer_instance):
        cls.animeviewer_instance = AnimeViewer_instance

    @classmethod
    def get_bottom_frame_instance(cls):
        return cls.bottom_frame_instance

    @classmethod
    def set_bottom_frame_instance(cls, instance):
        cls.bottom_frame_instance = instance

    @classmethod
    def get_top_frame_instance(cls):
        return cls.top_frame_instance

    @classmethod
    def set_top_frame_instance(cls, instance):
        cls.top_frame_instance = instance

    @classmethod
    def get_settings_window_instance(cls):
        return cls.settings_window_instance

    @classmethod
    def set_settings_window_instance(cls, instance):
        cls.settings_window_instance = instance

    @classmethod
    def get_details_frame_instance(cls):
        return cls.details_frame_instance

    @classmethod
    def set_details_frame_instance(cls, instance):
        cls.details_frame_instance = instance

# Content from /home/arthur/Code/PycharmProjects/Tanpopo rewrite/main/modules/helper.py
import customtkinter as ctk
import requests
from PIL import Image, UnidentifiedImageError
import asyncio
import aiohttp
from io import BytesIO
import tkinter as tk
from customtkinter import CTkLabel, CTkFrame, CTkFont
from main.gui.details.details import AnimeDetails
from main.modules import loaddata
from main.gui.Hover.Hover import HoverLabel
from main.modules.colors import grey, darkgrey
from main.modules.loaddata import get_anime_data
from main.modules.refresher import change_page_to_detail


def load_file(url, size):
    img = Image.open(url)
    return ctk.CTkImage(img, size=size)


def load_image_old(url, size):
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return ctk.CTkImage(img, size=size)


# Function to load image from URL and resize it asynchronously
async def load_image_async(url, size):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                img_data = await response.read()
                img = Image.open(BytesIO(img_data))
                return img
        except (aiohttp.ClientError, UnidentifiedImageError) as e:
            print(f"Error loading image from {url}: {e}")
            return None

# Function to replace shimmer label with "Failed loading" label
def handle_image_loading_error(frame, shimmer_label):
    error_label = ctk.CTkLabel(master=frame, text="Failed loading", font=ctk.CTkFont(size=16, weight="bold"), text_color="white", fg_color="black")
    error_label.grid(row=shimmer_label.grid_info()['row'], column=shimmer_label.grid_info()['column'], padx=10, pady=10)
    shimmer_label.destroy()

# Function to update the UI with loaded images
def update_ui_with_images(frame, size, shimmer_labels, watchtype):
    async def load_images():
        anime_data = loaddata.get_anime_data(watchtype=watchtype)  # Retrieve all anime data
        print("DATA")
        print(anime_data)
        anime_id = anime_data["ID"]
        print("Print Anime ID")
        print(anime_id)
        cover_images = anime_data["cover_images"]
        anime_titles = anime_data["titles"]
        anime_descriptions = anime_data["descriptions"]

        for i, (url, shimmer_label) in enumerate(zip(cover_images, shimmer_labels)):
            img = await load_image_async(url, size)
            image = ctk.CTkImage(light_image=img, dark_image=img, size=size)
            if image:  # Check if image loading was successful
                anime_title = anime_titles[i]  # Get the corresponding anime title
                anime_description = anime_descriptions[i]  # Get the corresponding anime description

                double_frame = CTkFrame(frame, fg_color=darkgrey)
                double_frame.grid(row=0, column=i, padx=5, sticky="n")

                # Create a frame for each image and its label
                img_frame = CTkFrame(double_frame, fg_color=darkgrey)
                img_frame.grid(row=0, column=i, padx=10, pady=(10, 0), sticky="n")

                # Create the image label
                img_label = CTkLabel(
                    master=img_frame,
                    text="",
                    fg_color=grey,
                    image=image,
                )
                img_label.image = image  # Keep a reference to avoid garbage collection
                img_label.pack()

                # Truncate the title if it's too long
                max_length = 30
                if len(anime_title) > max_length:
                    truncated_title = anime_title[:max_length - 3] + "..."
                else:
                    truncated_title = anime_title

                # Create the text label for the anime title
                text_label = CTkLabel(
                    master=img_frame,
                    text=truncated_title,
                    font=CTkFont(size=11),
                    text_color="white",
                    wraplength=size[0],  # Ensure text wraps within the width of the image
                    justify="center",
                    pady=5
                )
                text_label.pack()

                # Add click event to open details page
                img_label.bind("<Button-1>", lambda e, t=anime_title, d=anime_description, i=img, ai=anime_id: change_page_to_detail(t, d, i, ai))

                shimmer_label.destroy()  # Remove the shimmer label
                print(f"Image loaded and HoverLabel created for: {anime_title}")
            else:
                handle_image_loading_error(frame, shimmer_label)

    asyncio.run(load_images())

# Create shimmer effect label
def create_shimmer_label(master, width, height):
    canvas = tk.Canvas(master, width=width, height=height, bg="black", highlightthickness=0)
    shimmer_rect = canvas.create_rectangle(-width, -height, -width + 50, -height + 50, fill="#333333")
    canvas.grid_propagate(False)
    canvas.pack_propagate(False)
    canvas.grid(row=0, column=0, padx=10, pady=10)

    def animate():
        x0, y0, x1, y1 = canvas.coords(shimmer_rect)
        if x1 < width * 2 and y1 < height * 2:
            canvas.move(shimmer_rect, 10, 10)
        else:
            canvas.coords(shimmer_rect, -width, -height, -width + 50, -height + 50)
        master.after(20, animate)  # Faster speed

    animate()
    return canvas

