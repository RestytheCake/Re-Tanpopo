import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Settings")
        self.geometry("600x500")

        # Main Frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Frame for categories
        categories_frame = ctk.CTkFrame(main_frame, width=50)
        categories_frame.pack(side="left", fill="y", padx=(0, 10))

        self.buttons = []
        self.create_category_buttons(categories_frame)

        # Right Frame for content
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Initialize frames dictionary
        self.frames = {}

        # Create all frames
        self.create_services_frame()
        self.create_library_frame()
        self.create_application_frame()
        self.create_recognition_frame()
        self.create_advanced_frame()
        self.create_version_frame()
        self.create_credits_frame()

        # Show initial frame
        self.show_frame("Services")

        # Button Frame for OK and Cancel buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="bottom", padx=10, pady=(0, 5), anchor="e")
        ctk.CTkButton(button_frame, text="OK", command=self.ok_button).pack(side="right", padx=10, pady=2)
        ctk.CTkButton(button_frame, text="Cancel", command=self.cancel_button).pack(side="right", padx=10, pady=2)

    def create_category_buttons(self, frame):
        buttons = ["Services", "Library", "Application", "Recognition", "Advanced", "Version", "Credits"]
        for button in buttons:
            btn = ctk.CTkButton(frame, text=button, anchor="w", command=lambda b=button: self.on_button_click(b))
            btn.pack(fill="x", pady=5, padx=7)
            self.buttons.append(btn)

    def on_button_click(self, button):
        self.show_frame(button)
        self.update_button_styles(button)

    def update_button_styles(self, selected_button):
        for btn in self.buttons:
            if btn.cget("text") == selected_button:
                btn.configure(fg_color="#a9a9d9", hover_color="#8080b0", text_color="white")
            else:
                btn.configure(fg_color=['#3B8ED0', '#1F6AA5'], text_color="white")

    def create_services_frame(self):
        services_frame = ctk.CTkFrame(self.content_frame)
        self.frames["Services"] = services_frame

        notebook = ctk.CTkTabview(services_frame)
        notebook.pack(fill="both", expand=True)

        # Main Tab
        main_tab = notebook.add("Main")
        self.create_main_tab(main_tab)

        # Other Tabs (MyAnimeList, Kitsu, AniList)
        myanimelist_tab = notebook.add("MyAnimeList")
        self.create_myanimelist_tab(myanimelist_tab)
        notebook.add("Kitsu")
        notebook.add("AniList")

    def create_library_frame(self):
        library_frame = ctk.CTkFrame(self.content_frame)
        self.frames["Library"] = library_frame
        ctk.CTkLabel(library_frame, text="Library", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

    def create_application_frame(self):
        application_frame = ctk.CTkFrame(self.content_frame)
        self.frames["Application"] = application_frame
        ctk.CTkLabel(application_frame, text="Application", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

    def create_recognition_frame(self):
        recognition_frame = ctk.CTkFrame(self.content_frame)
        self.frames["Recognition"] = recognition_frame
        ctk.CTkLabel(recognition_frame, text="Recognition", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

    def create_advanced_frame(self):
        advanced_frame = ctk.CTkFrame(self.content_frame)
        self.frames["Advanced"] = advanced_frame
        ctk.CTkLabel(advanced_frame, text="Advanced", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

    def create_version_frame(self):
        version_frame = ctk.CTkFrame(self.content_frame)
        self.frames["Version"] = version_frame
        notebook = ctk.CTkTabview(version_frame)
        notebook.pack(fill="both", expand=True)

        # Credits Tab
        version_tab = notebook.add("Version")

        ctk.CTkLabel(version_tab, text="Version -  Alpha", font=ctk.CTkFont(size=16)).pack(anchor="w")
        ctk.CTkLabel(version_tab, text="0.0.0.0.0.0.0.0.0.0.01").pack(anchor="w", pady=(5, 2))

    def create_credits_frame(self):
        credits_frame = ctk.CTkFrame(self.content_frame)
        self.frames["Credits"] = credits_frame
        notebook = ctk.CTkTabview(credits_frame)
        notebook.pack(fill="both", expand=True)

        # Credits Tab
        credits_tab = notebook.add("Credits")

        ctk.CTkLabel(credits_tab, text="Owner", font=ctk.CTkFont(size=16)).pack(anchor="w")
        ctk.CTkLabel(credits_tab, text="--- ninestails").pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(credits_tab, text="Maintainer", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
        ctk.CTkLabel(credits_tab, text="--- resty1337", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w",
                                                                                                       padx=10)
        ctk.CTkLabel(credits_tab, text="Designer", font=ctk.CTkFont(size=16)).pack(anchor="w")
        ctk.CTkLabel(credits_tab, text="resty", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10)

    def create_main_tab(self, tab):
        ctk.CTkLabel(tab, text="Synchronization", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

        ctk.CTkLabel(tab, text="Active service and metadata provider:").pack(anchor="w", pady=(5, 2))
        service_options = ["AniList", "MyAnimeList", "Kitsu"]
        self.service_var = ctk.StringVar(value="AniList")
        service_menu = ctk.CTkOptionMenu(tab, variable=self.service_var, values=service_options)
        service_menu.pack(anchor="w", pady=(0, 10))

        label = ctk.CTkLabel(
            tab,
            text="Note: Taiga is unable to synchronize multiple services at the same time."
        )
        label.pack(anchor="w", pady=(0, 20), fill="x")
        tab.bind("<Configure>", lambda event: label.configure(wraplength=event.width))

        self.sync_var = ctk.BooleanVar(value=True)
        sync_checkbox = ctk.CTkCheckBox(tab, text="Synchronize automatically at startup", variable=self.sync_var)
        sync_checkbox.pack(anchor="w", pady=(0, 20))

    def create_myanimelist_tab(self, tab):
        ctk.CTkLabel(tab, text="Select Watch Lists", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))

        self.watching_var = ctk.BooleanVar(value=True)
        watching_checkbox = ctk.CTkCheckBox(tab, text="Watching", variable=self.watching_var)
        watching_checkbox.pack(anchor="w", pady=(0, 20))

        self.planned_var = ctk.BooleanVar(value=True)
        planned_checkbox = ctk.CTkCheckBox(tab, text="Planned to Watch", variable=self.planned_var)
        planned_checkbox.pack(anchor="w", pady=(0, 20))

        self.rewatched_var = ctk.BooleanVar(value=True)
        rewatched_checkbox = ctk.CTkCheckBox(tab, text="Rewatching", variable=self.rewatched_var)
        rewatched_checkbox.pack(anchor="w", pady=(0, 20))

        self.dropped_var = ctk.BooleanVar(value=True)
        dropped_checkbox = ctk.CTkCheckBox(tab, text="Dropped", variable=self.dropped_var)
        dropped_checkbox.pack(anchor="w", pady=(0, 20))

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()
        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)
        self.update_button_styles(frame_name)

    def ok_button(self):
        print("OK button clicked")
        self.destroy()

    def cancel_button(self):
        print("Cancel button clicked")
        self.destroy()
