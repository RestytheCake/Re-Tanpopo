from tanpopo_rewrite import *

set_appearance_mode("System")
set_default_color_theme("blue")


class SettingsWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Settings")
        self.geometry("600x500")

        # Main Frame
        main_frame = CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Frame for categories
        categories_frame = CTkFrame(main_frame, width=150)
        categories_frame.pack(side="left", fill="y", padx=(0, 10))

        self.create_category_buttons(categories_frame)

        # Right Frame for content
        content_frame = CTkFrame(main_frame)
        content_frame.pack(side="right", fill="both", expand=True)

        self.create_services_frame(content_frame)

    def create_category_buttons(self, frame):
        buttons = ["Services", "Library", "Application", "Recognition", "Sharing", "Torrents", "Advanced"]
        for button in buttons:
            CTkButton(frame, text=button, anchor="w").pack(fill="x", pady=5)

    def create_services_frame(self, frame):
        services_frame = CTkFrame(frame)
        services_frame.pack(fill="both", expand=True)

        notebook = CTkTabview(services_frame)
        notebook.pack(fill="both", expand=True)

        # Main Tab
        main_tab = notebook.add("Main")
        self.create_main_tab(main_tab)

        # Other Tabs (MyAnimeList, Kitsu, AniList)
        notebook.add("MyAnimeList")
        notebook.add("Kitsu")
        notebook.add("AniList")

    def create_main_tab(self, tab):
        CTkLabel(tab, text="Synchronization", font=CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

        CTkLabel(tab, text="Active service and metadata provider:").pack(anchor="w", pady=(5, 2))
        service_options = ["AniList", "MyAnimeList", "Kitsu"]
        self.service_var = StringVar(value="AniList")
        service_menu = CTkOptionMenu(tab, variable=self.service_var, values=service_options)
        service_menu.pack(anchor="w", pady=(0, 10))

        CTkLabel(tab, text="Note: Taiga is unable to synchronize multiple services at the same time.").pack(anchor="w",
                                                                                                            pady=(
                                                                                                            0, 20))

        self.sync_var = BooleanVar(value=True)
        sync_checkbox = CTkCheckBox(tab, text="Synchronize automatically at startup", variable=self.sync_var)
        sync_checkbox.pack(anchor="w", pady=(0, 20))

        # OK and Cancel buttons
        button_frame = CTkFrame(tab)
        button_frame.pack(fill="x", pady=(10, 0))
        CTkButton(button_frame, text="OK", command=self.ok_button).pack(side="right", padx=(0, 10))
        CTkButton(button_frame, text="Cancel", command=self.cancel_button).pack(side="right", padx=(0, 10))

    def ok_button(self):
        print("OK button clicked")
        self.destroy()

    def cancel_button(self):
        print("Cancel button clicked")
        self.destroy()
