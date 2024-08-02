# Content from C:\Users\Morga\PycharmProjects\Tanpopo rewrite\main\gui\AnimeViewer.py
from customtkinter import *
from localStoragePy import localStoragePy  # Database

from main.gui.details.details import AnimeDetails
# ~~~ SUB ~~~
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
        #self.details_frame()

    def init_frames(self):
        # Initialize Top Frame
        self.top_frame = CTkFrame(self.main_frame, fg_color=grey)
        top_frame_instance = Top_Frame(self.top_frame)
        GlobalManager.set_top_frame_instance(top_frame_instance)

        # Initialize Bottom Frame
        self.video_frame = CTkFrame(self.main_frame, fg_color=darkgrey)
        bottom_frame_instance = Bottom_Frame(self.video_frame)
        GlobalManager.set_bottom_frame_instance(bottom_frame_instance)

    def details_frame(self):
        details_frame_instance = AnimeDetails(self.main_frame)
        GlobalManager.set_details_frame_instance(details_frame_instance)

    def reload(self):
        # Clear the main_frame and reinitialize all components
        self.clear()
        self.init_frames()

    def clear(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


# Content from C:\Users\Morga\PycharmProjects\Tanpopo rewrite\main\gui\details\details.py
import customtkinter as ctk
import tkinter as tk


class AnimeDetails(ctk.CTk):
    def __init__(self, frame, title=None, description=None, image=None, **kwargs):
        super().__init__(**kwargs)
        self.master = frame
        self.title = title
        print(self.title)
        self.description = description
        print(self.description)
        self.image = image
        print(self.image)
        self.create_widgets()

    def create_widgets(self):
        # Display anime cover
        cover_label = ctk.CTkLabel(self, image=self.image)
        cover_label.image = self.image  # Keep a reference to avoid garbage collection
        cover_label.pack(pady=10)

        # Display anime title
        title_label = ctk.CTkLabel(self, text=self.title, font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=10)

        # Display anime description
        description_label = ctk.CTkLabel(self, text=self.description, wraplength=500)
        description_label.pack(pady=10)

        # Button to set folder location
        set_location_button = ctk.CTkButton(self, text="Set Folder Location",
                                            command=self.set_folder_location)
        set_location_button.pack(pady=10)

        # Placeholder for episode list
        self.episodes_frame = ctk.CTkFrame(self)
        self.episodes_frame.pack(pady=10, fill="both", expand=True)

        # Load and display episodes
        self.load_episodes()

    def set_folder_location(self):
        folder_path = tk.filedialog.askdirectory()
        if folder_path:
            print(f"Folder location for {self.title}: {folder_path}")
            # Save the folder location for the anime (implement saving logic here)

    def load_episodes(self):
        # Placeholder for loading episodes from the folder
        episodes = ["Episode 1", "Episode 2", "Episode 3"]  # Replace with actual episode loading logic
        for episode in episodes:
            episode_button = ctk.CTkButton(self.episodes_frame, text=episode)
            episode_button.pack(pady=5)


# Content from C:\Users\Morga\PycharmProjects\Tanpopo rewrite\main\modules\globalmanager.py
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
    def get_top_frame_instance(cls):  # Getter method for the new variable
        return cls.top_frame_instance

    @classmethod
    def set_top_frame_instance(cls, instance):  # Setter method for the new variable
        cls.top_frame_instance = instance

    @classmethod
    def get_settings_window_instance(cls):  # Getter for settings window instance
        return cls.settings_window_instance

    @classmethod
    def set_settings_window_instance(cls, instance):  # Setter for settings window instance
        cls.settings_window_instance = instance

    @classmethod
    def get_details_frame_instance(cls):  # Getter for settings window instance
        return cls.details_frame_instance

    @classmethod
    def set_details_frame_instance(cls, instance):
        cls.details_frame_instance = instance





# Content from C:\Users\Morga\PycharmProjects\Tanpopo rewrite\main\modules\helper.py
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


# I really need to rewrite this crap

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
                img = img.resize(size, Image.LANCZOS)
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except (aiohttp.ClientError, UnidentifiedImageError) as e:
            print(f"Error loading image from {url}: {e}")
            return None


# Function to replace shimmer label with "Failed loading" label
def handle_image_loading_error(frame, shimmer_label):
    error_label = ctk.CTkLabel(master=frame, text="Failed loading", font=ctk.CTkFont(size=16, weight="bold"),
                               text_color="white", fg_color="black")
    error_label.grid(row=shimmer_label.grid_info()['row'], column=shimmer_label.grid_info()['column'], padx=10, pady=10)
    shimmer_label.destroy()


# Function to update the UI with loaded images
def update_ui_with_images(frame, size, shimmer_labels, watchtype):
    async def load_images():
        anime_data = loaddata.get_anime_data(watchtype=watchtype)  # Retrieve all anime data
        cover_images = anime_data["cover_images"]
        anime_titles = anime_data["titles"]
        anime_descriptions = anime_data["descriptions"]

        for i, (url, shimmer_label) in enumerate(zip(cover_images, shimmer_labels)):
            image = await load_image_async(url, size)
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
                img_label.bind("<Button-1>",
                               lambda e: change_page_to_detail(anime_title, anime_descriptions, image))
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


# Content from C:\Users\Morga\PycharmProjects\Tanpopo rewrite\main\modules\refresher.py
from main.gui.details.details import AnimeDetails
from main.modules.globalmanager import GlobalManager

animeviewer_instance = GlobalManager.get_animeviewer_instance()
bottom_frame_instance = GlobalManager.get_bottom_frame_instance()
top_frame_instance = GlobalManager.get_top_frame_instance()
settings_instance = GlobalManager.get_settings_window_instance()
details_frame_instance = GlobalManager.get_details_frame_instance()


def refresh_global():
    if bottom_frame_instance:
        bottom_frame_instance.update_settings()
    if top_frame_instance:
        top_frame_instance.update_settings()
    if settings_instance:
        settings_instance.update_settings()
    else:
        print("refresh Frame instance is not initialized")
    print("Refresh done!")


def clear_main():
    if animeviewer_instance:
        animeviewer_instance.clear()
    else:
        print("Clear Frame instance is not initialized")
    print("Clear done!")


def change_page_to_detail(title, desc, img):
    clear_main()
    AnimeDetails(title, desc, img)


