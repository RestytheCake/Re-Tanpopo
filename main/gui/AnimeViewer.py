from customtkinter import *
from localStoragePy import localStoragePy  # Database

# ~~~ SUB ~~~
from main.gui.main_frame.bottom_frame.bottom_frame import Bottom_Frame
from main.gui.main_frame.top_frame.top_frame import Top_Frame
from main.modules.colors import grey, darkgrey
from main.modules.globalmanager import GlobalManager

# Initialize Database
ls = localStoragePy("Tanpopo Rewrite", "json")

# Initialize global variable
global_bottom_frame_instance = None


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

    def init_frames(self):
        # Initialize Top Frame
        self.top_frame = CTkFrame(self.main_frame, fg_color=grey)
        top_frame_instance = Top_Frame(self.top_frame)
        GlobalManager.set_top_frame_instance(top_frame_instance)

        # Initialize Bottom Frame
        self.video_frame = CTkFrame(self.main_frame, fg_color=darkgrey)
        bottom_frame_instance = Bottom_Frame(self.video_frame)
        GlobalManager.set_bottom_frame_instance(bottom_frame_instance)

    def reload(self):
        # Clear the main_frame and reinitialize all components
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.init_frames()
