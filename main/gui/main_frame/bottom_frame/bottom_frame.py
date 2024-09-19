# main/gui/main_frame/bottom_frame/bottom_frame.py
import threading
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkScrollableFrame
from localStoragePy import localStoragePy
from main.modules import helper, loaddata
from main.modules.colors import grey, darkgrey

# Initialize local storage for Tanpopo Rewrite
ls = localStoragePy("Tanpopo Rewrite", "json")
print(f"Initialized localStoragePy for Tanpopo Rewrite: {ls}")


class Bottom_Frame(CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, fg_color=darkgrey, **kwargs)
        print("Initializing Bottom_Frame...")

        self.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(0, weight=0)  # Set minimum size for rows
        self.rowconfigure(1, weight=0)  # Allow row to expand
        self.rowconfigure(2, weight=0)  # Allow row to expand
        self.rowconfigure(3, weight=0)  # Allow row to expand
        self.columnconfigure(0, weight=1)  # Allow column to expand
        self.row_counter = 0
        print(f"Initialized row_counter: {self.row_counter}")

        self.init_video_frame_content()
        print("Initialized video frame content.")

    def init_video_frame_content(self):
        """Initialize the content of the video frame."""

        ls_settings = localStoragePy("Settings", "json")
        print("Initializing video frame content...")

        # Clear existing frames before initializing new content
        self.clear_frames()

        print("Cleared existing frames.")

        # Retrieve settings from local storage
        w = ls_settings.getItem("AniList/watching")
        p = ls_settings.getItem("AniList/planned")
        r = ls_settings.getItem("AniList/rewatched")
        c = ls_settings.getItem("AniList/completed")

        # Create a dictionary of key-value pairs with their respective colors
        settings_dict = {
            "Currently Watching": (w, "#0096FF"),  # Bright Blue
            "Plan to Watch": (p, "#963567"),  # Pinkish Purple
            "Rewatching": (r, "#A9D3A7"),  # Soft Green
            "Completed": (c, "#FFD700")  # Gold
        }

        print(f"Created settings dictionary: {settings_dict}")

        # Iterate over the dictionary and create a frame for each "True" string value
        for key, (value, color) in settings_dict.items():
            if value == "True":
                print(f"Creating frame for: {key} with color: {color}")
                self.video_box(text=key, color=color)
                self.row_counter += 1
                print(f"Incremented row_counter to: {self.row_counter}")

    def video_box(self, text, color):
        """Create a video box for each setting."""

        print(f"Creating video box for: {text} with color: {color}")

        # Create a frame for each setting with the specified color
        frame_name = CTkFrame(master=self, fg_color=color)

        frame_name.grid(row=self.row_counter, column=0, padx=10, pady=5, sticky="ew")

        print(f"Created and placed frame_name in grid at row: {self.row_counter}")

        # Configure grid for frame_name
        frame_name.grid_rowconfigure(0, weight=0)  # Row with text label should not expand
        frame_name.grid_rowconfigure(1, weight=0)  # Row with scrollable frame should expand
        frame_name.grid_columnconfigure(0, weight=1)  # Ensure the frame content uses available width

        # Create a text label within this frame
        text_label = CTkLabel(master=frame_name, text=text, font=CTkFont(size=18, weight="bold"), text_color="white")

        text_label.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="nw")

        print(f"Created and placed text_label in frame_name with text: {text}")

        # Create a scrollable frame within this frame
        scrollable_frame = CTkScrollableFrame(master=frame_name, fg_color=grey, orientation="horizontal", height=157)

        scrollable_frame.grid(row=1, column=0, padx=0, pady=(0, 5), sticky="ew")

        print("Created and placed scrollable_frame in frame_name.")

        # List to hold shimmer labels
        anime_shimmer_labels = []

        cover_images = loaddata.print_cover_images(watchtype=text)

        print(f"Loaded cover images for watchtype '{text}': {cover_images}")

        for i in range(len(cover_images)):
            shimmer_label = helper.create_shimmer_label(scrollable_frame, 100, 150)
            shimmer_label.grid(row=0, column=i, padx=10)
            anime_shimmer_labels.append(shimmer_label)
            print(f"Created shimmer_label and placed in grid at column {i}.")

        # Start a thread to update the UI with images
        threading.Thread(
            target=helper.update_ui_with_images,
            args=(scrollable_frame, (90, 115), anime_shimmer_labels, text)
        ).start()

        print(f"Started thread to update UI with images for {text}.")

    def clear_frames(self):
        """Clear all widgets from the video frame."""

        print("Clearing frames...")

        for widget in self.winfo_children():
            widget.destroy()
            print(f"Destroyed widget: {widget}")

        self.row_counter = 0

        print(f"Reset row_counter to: {self.row_counter}")

    def update_settings(self):
        """Update settings and reinitialize components."""

        print("Updating settings...")

        self.init_video_frame_content()

        print("Reinitialized video frame content.")