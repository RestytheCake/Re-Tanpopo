# main/gui/anime_viewer.py
from customtkinter import CTkFrame
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
        self.master = master
        self.configure_master()
        self.main_frame = self.create_main_frame()
        self.init_frames()
        GlobalManager.set_animeviewer_instance(self)

    def configure_master(self):
        """Configure the master window."""
        self.master.title("Tanpopo")
        self.master.geometry("900x650")
        self.master.configure(fg_color=grey)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

    def create_main_frame(self):
        """Create and return the main frame."""
        main_frame = CTkFrame(self.master, fg_color=grey)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.rowconfigure(0, weight=0)  # Top frame row
        main_frame.rowconfigure(1, weight=1)  # Bottom frame row
        main_frame.columnconfigure(0, weight=1)
        return main_frame

    def init_frames(self):
        """Initialize top and bottom frames."""
        self.init_top_frame()
        self.init_bottom_frame()

    def init_top_frame(self):
        """Initialize the top frame."""
        top_frame_instance = Top_Frame(self.main_frame)
        GlobalManager.set_top_frame_instance(top_frame_instance)
        top_frame_instance.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

    def init_bottom_frame(self):
        """Initialize the bottom frame."""
        bottom_frame_instance = Bottom_Frame(self.main_frame)
        GlobalManager.set_bottom_frame_instance(bottom_frame_instance)
        bottom_frame_instance.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

    def details_frame(self, title, description, image, anime_id):
        """Display the details frame."""
        self.clear()
        details = AnimeDetails(
            self.main_frame,
            title=title,
            description=description,
            image=image,
            anime_id=anime_id
        )
        details.pack(fill="both", expand=True)
        GlobalManager.set_details_frame_instance(details)

    def reload(self):
        """Reload all components by clearing and reinitializing frames."""
        self.clear()
        self.init_frames()

    def clear(self):
        """Clear all widgets from the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()