import json
import customtkinter as ctk
import tkinter as tk
import CTkListbox
from PIL.Image import Image
from main.modules.globalmanager import GlobalManager

class AnimeDetails(ctk.CTkFrame):
    IMAGE_SIZE = (200, 150)
    DESCRIPTION_WRAP_LENGTH = 300
    PADDING = 10
    BORDER_WIDTH = 2

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

        self._create_widgets()

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
        episode_list = CTkListbox.CTkListbox(self.left_frame, width=200, height=250)
        episode_list.grid(row=3, column=0, pady=10, padx=self.PADDING, sticky="nw")
        episode_list.insert(0, "Episode 1")
        episode_list.insert(1, "Episode 2")
        episode_list.insert(2, "Episode 3")

    def _create_right_frame(self):
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, padx=self.PADDING, pady=self.PADDING, sticky="nsew")

        self._create_top_right_frame()
        self._create_bottom_right_frame()

    def _create_top_right_frame(self):
        self.top_right_frame = ctk.CTkFrame(
            self.right_frame, fg_color="transparent", border_width=self.BORDER_WIDTH, border_color="grey", corner_radius=10
        )
        self.top_right_frame.grid(row=0, column=0, sticky="nsew", padx=self.PADDING, pady=(0, 5))

        back_button = ctk.CTkButton(
            self.top_right_frame, text="Back to Main", command=self.back_to_main, corner_radius=10
        )
        back_button.grid(row=0, column=0, pady=self.PADDING, padx=self.PADDING, sticky="nw")

    def _create_bottom_right_frame(self):
        self.bottom_right_frame = ctk.CTkFrame(
            self.right_frame, fg_color="transparent", border_width=self.BORDER_WIDTH, border_color="grey", corner_radius=10
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
            self.description_frame, text=self.description, wraplength=self.DESCRIPTION_WRAP_LENGTH, justify="left", text_color="#666666"
        )
        self.description_label.grid(row=1, column=0, pady=5, sticky="w")

    def set_folder_location(self):
        folder_path = tk.filedialog.askdirectory()
        if folder_path:
            print(f"Folder location for {self.title}: {folder_path}")

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

    def browse_file(self):
        file_path = ctk.filedialog.askdirectory()
        if file_path:
            with open("series_locations.json", "r+") as file:
                data = json.load(file)
                data[str(self.anime_id)] = file_path
                file.seek(0)
                json.dump(data, file, indent=4)

    def update_file_location(self):
        directory = self.read_file_location(self.anime_id)
        if directory:
            pass

    def read_file_location(self, anime_id):
        file_location = None
        try:
            with open("series_locations.json", "r") as file:
                data = json.load(file)
                file_location = data.get(str(anime_id))
        except FileNotFoundError:
            print("series_locations.json not found.")
        return file_location
