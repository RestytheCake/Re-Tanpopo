# main/gui/main_frame/top_frame/top_frame.py
import requests
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkFont
from localStoragePy import localStoragePy
from webbrowser import open as webopen

from main.gui.Settings.settings import SettingsWindow
from main.modules import helper
from main.modules.colors import grey
from main.modules.path import IMG_DIR
from main.modules.globalmanager import GlobalManager


class Top_Frame(CTkFrame):
    def __init__(self, master=None):
        super().__init__(master, fg_color=grey)
        self.avatar = None
        self.username_label = None
        self.avatar_frame = None
        self.button_frame = None
        self.setting_button = None
        self.grid(row=0, column=0, sticky="new")
        self.columnconfigure(0, weight=1, minsize=325)
        self.columnconfigure(1, weight=1, minsize=300)
        self.init()

    def open_settings(self):
        """Open the settings window."""
        settingswindow_instance = SettingsWindow(self)
        GlobalManager.set_settings_window_instance(settingswindow_instance)

    def button_func(self):
        """Create and configure the button frame."""
        self.button_frame = CTkFrame(self, fg_color=grey)
        self.button_frame.grid(row=0, column=1, pady=15, padx=15, sticky="nes")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.rowconfigure(0, weight=1)

        self.setting_button = CTkButton(
            self.button_frame,
            text="Settings",
            image=helper.load_file(IMG_DIR / "setting.png", (32, 32)),
            compound="left",
            font=CTkFont(size=32, weight="bold"),
            command=self.open_settings
        )
        self.setting_button.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    def avatar_frame_func(self):
        """Create and configure the avatar frame."""
        self.avatar_frame = CTkFrame(self, fg_color=grey)
        self.avatar_frame.grid(row=0, column=0, pady=10, padx=15, sticky="nw")

        ls = localStoragePy("Tanpopo Rewrite", "json")
        username = ls.getItem("username")

        if username is None:
            self.display_default_avatar()
            print("Raise Error: Not Logged in or Couldn't Load Avatar Image")
        else:
            try:
                self.display_user_avatar(username)
            except requests.exceptions.RequestException:
                print("Network error: Loading default avatar.")
                self.display_default_avatar()
                self.display_offline_mode()

    def display_default_avatar(self):
        """Display default avatar and message."""
        self.avatar = CTkLabel(
            self.avatar_frame,
            image=helper.load_file(IMG_DIR / "AniList.png", (125, 125)),
            text=""
        )
        self.avatar.grid(row=0, column=0, padx=10)

        self.username_label = CTkLabel(
            self.avatar_frame,
            text="Use Settings for Login",
            fg_color=grey,
            font=CTkFont(size=16, weight="bold")
        )
        self.username_label.grid(row=1, column=0, padx=10, pady=0)

    def display_user_avatar(self, username):
        """Display user's avatar and greeting."""

        ls = localStoragePy("Tanpopo Rewrite", "json")

        avatar_url = ls.getItem("avatar_url")

        self.avatar = CTkLabel(
            self.avatar_frame,
            image=helper.load_image_old(avatar_url, (125, 125)),
            text=""
        )

        self.avatar.bind("<Button-1>", lambda e: webopen(f"https://anilist.co/user/{username}"))

        self.avatar.grid(row=0, column=0, padx=10)

        self.username_label = CTkLabel(
            self.avatar_frame,
            text=f'Hello {username}!',
            fg_color=grey,
            font=CTkFont(size=16, weight="bold")
        )

        self.username_label.grid(row=1, column=0, padx=10, pady=0)

    def display_offline_mode(self):
        """Display offline mode message."""

        offline_label = CTkLabel(
            self.avatar_frame,
            text='Offline Mode',
            fg_color=grey,
            font=CTkFont(size=8, slant="italic")
        )

        offline_label.grid(row=2, column=0, padx=10, pady=0)

    def init(self):
        """Initialize the frame components."""

        # Clear existing frames before initializing new ones
        self.clear_frames()

        # Initialize the frames
        self.avatar_frame_func()

        # Initialize the buttons
        self.button_func()

    def clear_frames(self):
        """Clear all widgets from the top frame."""

        print("Clearing frames...")

        for widget in self.winfo_children():
            widget.destroy()
            print(f"Destroyed widget: {widget}")

    def update_settings(self):
        """Update settings and reinitialize components."""

        print("Updating settings...")

        # Reinitialize components after updating settings
        self.init()

        print("Reinitialized avatar frame content.")