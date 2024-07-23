from localStoragePy import localStoragePy

from sub.gui.Settings.buttons.buttons import *
from sub.gui.Settings.service_frame.advanced import create_advanced_frame
from sub.gui.Settings.service_frame.application import create_application_frame
from sub.gui.Settings.service_frame.clear import create_clear_frame
from sub.gui.Settings.service_frame.credits import create_credits_frame
from sub.gui.Settings.service_frame.library import create_library_frame
from sub.gui.Settings.service_frame.recognition import create_recognition_frame
from sub.gui.Settings.service_frame.services import create_services_frame
from sub.gui.Settings.service_frame.version import create_version_frame
from sub.modules.globalmanager import GlobalManager

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

ls_settings = localStoragePy("Settings", "json")


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.rewatched_var = None
        self.planned_var = None
        self.watching_var = None
        self.completed_var = None
        self.title("Settings")
        self.geometry("600x500")

        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Frame for categories
        categories_frame = ctk.CTkFrame(main_frame, width=50)
        categories_frame.pack(side="left", fill="y", padx=(0, 10))

        self.buttons = []
        create_category_buttons(self, categories_frame)

        # Right Frame for content
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Initialize frames dictionary
        self.frames = {}

        # Create all frames
        create_services_frame(self)
        create_library_frame(self)
        create_application_frame(self)
        create_recognition_frame(self)
        create_advanced_frame(self)
        create_version_frame(self)
        create_credits_frame(self)
        create_clear_frame(self)

        # Show initial frame
        show_frame(self, "Services")
        self.load_initial_settings()

        # Button Frame for OK and Cancel buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="bottom", padx=10, pady=(0, 5), anchor="e")
        ctk.CTkButton(button_frame, text="OK", command=self.ok_button).pack(side="right", padx=10, pady=2)
        ctk.CTkButton(button_frame, text="Cancel", command=self.cancel_button).pack(side="right", padx=10, pady=2)

    def save_settings(self):
        print("save")
        # Save AniList settings
        ls_settings.setItem("AniList/watching", self.watching_var.get())
        ls_settings.setItem("AniList/planned", self.planned_var.get())
        ls_settings.setItem("AniList/rewatched", self.rewatched_var.get())
        ls_settings.setItem("AniList/completed", self.completed_var.get())
        # Access the Bottom_Frame instance using the global manager
        bottom_frame_instance = GlobalManager.get_bottom_frame_instance()
        if bottom_frame_instance:
            bottom_frame_instance.update_settings()
        else:
            print("Bottom_Frame instance is not initialized")

    def load_initial_settings(self):
        print("load init")
        # Load AniList settings
        try:
            self.watching_var.set(ls_settings.getItem("AniList/watching"))
            self.planned_var.set(ls_settings.getItem("AniList/planned"))
            self.rewatched_var.set(ls_settings.getItem("AniList/rewatched"))
            self.completed_var.set(ls_settings.getItem("AniList/completed"))
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
