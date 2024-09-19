import tkinter as tk
from localStoragePy import localStoragePy
from main.gui.Settings.buttons.buttons import *
from main.gui.Settings.service_frame.advanced import create_advanced_frame
from main.gui.Settings.service_frame.application import create_application_frame
from main.gui.Settings.service_frame.clear import create_clear_frame
from main.gui.Settings.service_frame.credits import create_credits_frame
from main.gui.Settings.service_frame.library import create_library_frame
from main.gui.Settings.service_frame.player import create_player_frame
from main.gui.Settings.service_frame.recognition import create_recognition_frame
from main.gui.Settings.service_frame.services import create_services_frame
from main.gui.Settings.service_frame.version import create_version_frame
from main.modules.globalmanager import GlobalManager

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Local storage initialization
ls_settings_init = localStoragePy("Settings", "json")


class SettingsWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rewatched_var = ctk.BooleanVar()
        self.planned_var = ctk.BooleanVar()
        self.watching_var = ctk.BooleanVar()
        self.completed_var = ctk.BooleanVar()

        self.title("Settings")
        self.geometry("600x505")
        self.resizable(False, False)
        # TODO: fix needed for Linux
        #self.grab_set()

        # Call the method to build the window
        self.build_window()

    def build_window(self):
        # Clear the current grid layout if it exists
        for widget in self.winfo_children():
            widget.grid_forget()

        # Main Frame for content and categories
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0, 5))

        # Left Frame for categories
        categories_frame = ctk.CTkFrame(main_frame, width=200)
        categories_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=(18, 0))

        self.buttons = []
        create_category_buttons(self, categories_frame)

        # Right Frame for content
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Initialize frames dictionary
        self.frames = {}

        # Create all frames
        create_services_frame(self)
        create_library_frame(self)
        create_application_frame(self)
        create_recognition_frame(self)
        create_advanced_frame(self)
        create_player_frame(self)
        create_version_frame(self)
        create_credits_frame(self)
        create_clear_frame(self)

        # Show initial frame
        show_frame(self, "Services")
        self.load_initial_settings()

        # Configure row and column weights for main_frame
        main_frame.grid_rowconfigure(0, weight=1)  # Content area should expand
        main_frame.grid_columnconfigure(0, weight=0)  # Fixed width for categories_frame
        main_frame.grid_columnconfigure(1, weight=1)  # Expandable content_frame

        # Button Frame for OK and Cancel buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))

        ctk.CTkButton(button_frame, text="OK", command=self.ok_button).pack(side="right", padx=10, pady=2)
        ctk.CTkButton(button_frame, text="Cancel", command=self.cancel_button).pack(side="right", padx=10, pady=2)

        # Ensure button_frame spans all columns and adjust its weight
        self.grid_rowconfigure(0, weight=1)  # Allow main content area to expand
        self.grid_rowconfigure(1, weight=0)  # Keep button_frame at the bottom

        # Configure column weight to ensure button_frame spans the entire width
        self.grid_columnconfigure(0, weight=1)

    def save_settings(self):
        print("save")
        ls_settings = localStoragePy("Settings", "json")
        ls_settings.setItem("AniList/watching", self.watching_var.get())
        ls_settings.setItem("AniList/planned", self.planned_var.get())
        ls_settings.setItem("AniList/rewatched", self.rewatched_var.get())
        ls_settings.setItem("AniList/completed", self.completed_var.get())
        bottom_frame_instance = GlobalManager.get_bottom_frame_instance()
        if bottom_frame_instance:
            bottom_frame_instance.update_settings()
        else:
            print("Bottom_Frame instance is not initialized")

    def load_initial_settings(self):
        print("load init")
        try:
            self.watching_var.set(ls_settings_init.getItem("AniList/watching"))
            self.planned_var.set(ls_settings_init.getItem("AniList/planned"))
            self.rewatched_var.set(ls_settings_init.getItem("AniList/rewatched"))
            self.completed_var.set(ls_settings_init.getItem("AniList/completed"))
        except:
            print("Not Logged in AniList")

    def ok_button(self):
        self.save_settings()
        print("OK button clicked: Settings saved.")
        self.destroy()

    def cancel_button(self):
        self.load_initial_settings()
        print("Cancel button clicked: Settings reverted.")
        self.destroy()

    def update_settings(self):
        print("Reloading settings window...")
        # Destroy current widgets and rebuild the window
        for widget in self.winfo_children():
            widget.destroy()
        self.build_window()
