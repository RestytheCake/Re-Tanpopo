import threading
from customtkinter import *
from localStoragePy import localStoragePy  # Database
import json
from webbrowser import open as webopen

# ~~~ SUB ~~~
import authwindow
import sub.helper as helper
import api
import sub.loadcovers
#import sub.discordpresence
#for some reason that's bugged if uncommentied will just run thatpresence script nothing else.

# Initialize Database
ls = localStoragePy("Tanpopo Rewrite", "json")



# Color
grey = "#242424"
darkgrey = "#191919"


class AnimeViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Tanpopo")
        self.master.configure(fg_color=grey)

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.toplevel_window = None

        # Call the function to print cover images
        self.recently_updated_urls = sub.loadcovers.print_cover_images()
        # Make the main window resizable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.main_frame = CTkFrame(self.master, fg_color=grey)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Top frame containing avatar and buttons
        self.top_frame = CTkFrame(self.main_frame, fg_color=grey)
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.top_frame.columnconfigure(0, weight=1, minsize=325)
        self.top_frame.columnconfigure(1, weight=1, minsize=300)

        self.avatar_frame = CTkFrame(self.top_frame, fg_color=grey)
        self.avatar_frame.grid(row=0, column=0, pady=15, padx=15, sticky="nw")

        # Button frame with buttons aligned to the right
        self.button_frame = CTkFrame(self.top_frame, fg_color=grey)
        self.button_frame.grid(row=0, column=1, pady=15, padx=15, sticky="nes")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)
        self.button_frame.rowconfigure(2, weight=1)

        # ---- Buttons
        self.button = CTkButton(
            self.button_frame,
            text="Refresh Anilist",
            font=CTkFont(size=12, weight="bold"),
            command=api.Load_API,
        )
        self.button.grid(row=0, column=0, pady=5, padx=5, sticky="e")

        self.auth_button = CTkButton(
            self.button_frame,
            text="Refresh Authentication",
            font=CTkFont(size=12, weight="bold"),
            command=authwindow.ToplevelWindow,
        )
        self.auth_button.grid(row=1, column=0, pady=5, padx=5, sticky="e")

        self.mpv_button = CTkButton(
            self.button_frame,
            text="Set MPV location",
            font=CTkFont(size=12, weight="bold"),
        )
        self.mpv_button.grid(row=2, column=0, pady=5, padx=5, sticky="e")

        # Watching frame for displaying continue watching content
        self.video_frame = CTkFrame(self.main_frame, fg_color=darkgrey)
        self.video_frame.grid(row=1, column=0, sticky="nsew")
        self.video_frame.rowconfigure(0, weight=1)
        self.video_frame.columnconfigure(0, weight=1)

        # Avatar Image
        try:
            username = ls.getItem("username")
            self.avatar = CTkLabel(
                self.avatar_frame,
                125,
                125,
                0,
                "transparent",
                image=helper.load_image_old(ls.getItem("avatar_url"), (125, 125)),
                text="",
            )
            self.avatar.bind("<Button-1>", lambda e: webopen(f"https://anilist.co/user/{username}"))
            self.avatar.grid(row=0, column=0, padx=10)
        except:
            print("Raise Error: Not Logged in or Couldn't Load Avatar Image")
            self.avatar = CTkLabel(
                self.avatar_frame,
                150,
                150,
                0,
                "transparent",
                image=helper.load_file("img/AniList.png", (125, 125)),
                text="",
            )
            self.avatar.grid(row=0, column=0, padx=10)

        # Username Check
        username = ls.getItem("username")
        if username is None:
            self.username_label = CTkLabel(
                self.avatar_frame,
                text=f"Log In",
                fg_color=grey,
                padx=10,
                font=CTkFont(size=16, weight="bold"),
            )
            self.username_label.grid(row=1, column=0, padx=10)
        else:
            self.username_label = CTkLabel(
                self.avatar_frame,
                text=f'Hello {ls.getItem("username")}!',
                fg_color=grey,
                font=CTkFont(size=16, weight="bold"),
            )
            self.username_label.grid(row=1, column=0, padx=10)

        # Top End ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Recently Updated Frame
        self.watching_frame = CTkFrame(master=self.video_frame, fg_color=grey)
        self.watching_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.watching_frame.grid_columnconfigure(0, weight=1)

        # Watching Text
        self.recently_text = CTkLabel(
            master=self.watching_frame,
            text="Continue Watching",
            font=CTkFont(size=18, weight="bold"),
            text_color="white",
            fg_color=grey,
        )
        self.recently_text.grid(row=0, column=0, padx=5, sticky="nw")

        # Watching Shows
        self.recently_video_frame = CTkScrollableFrame(
            master=self.watching_frame,
            fg_color=grey,
            orientation="horizontal",
            height=120,
        )
        self.recently_video_frame.grid(row=1, column=0, padx=10, sticky="new")

        # URLS for Effects don't touch it
        self.recently_updated_shimmer_labels = []
        for i in range(len(self.recently_updated_urls)):
            shimmer_label = helper.create_shimmer_label(self.recently_video_frame, 80, 115)
            shimmer_label.grid(row=0, column=i, padx=10)
            self.recently_updated_shimmer_labels.append(shimmer_label)

        threading.Thread(
            target=helper.update_ui_with_images,
            args=(
                self.recently_updated_urls,
                self.recently_video_frame,
                (80, 115),
                self.recently_updated_shimmer_labels,
            ),
        ).start()
        # threading for Python Multitasking, so that python doesn't lag when loading the images with poor WI-FI or bad server

        """
        # ~~~ Planned ~~~
        self.planned_frame = CTkFrame(master=self.video_frame, fg_color="#191919")
        self.planned_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.planned_frame.grid_columnconfigure(0, weight=1)

        self.planned_text = CTkLabel(master=self.planned_frame, text="Planned Watching", font=CTkFont(size=18, weight="bold"), text_color="white")
        self.planned_text.grid(row=0, column=0, padx=5, sticky="nw")

        self.planned_video_frame = CTkFrame(master=self.planned_frame, fg_color="#191919")
        self.planned_video_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.planned_video_frame.grid_columnconfigure(0, weight=1)

        # ~~~ Paused ~~~

        self.paused_frame = CTkFrame(master=self.video_frame, fg_color="#191919")
        self.paused_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.paused_frame.grid_columnconfigure(0, weight=1)

        self.paused_text = CTkLabel(master=self.paused_frame, text="Paused",
                                     font=CTkFont(size=18, weight="bold"), text_color="white")
        self.paused_text.grid(row=0, column=0, padx=5, sticky="nw")

        self.paused_video_frame = CTkFrame(master=self.paused_frame, fg_color="#191919")
        self.paused_video_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.paused_video_frame.grid_columnconfigure(0, weight=1)
        """

        # Bottom End ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        version_text = CTkLabel(
            self.master,
            text="ver 0.0.7",
            text_color="#FFFFFF",
            fg_color="#121212",
            padx="10",
        )
        version_text.place(relx=1.0, rely=1.0, anchor="se")


if __name__ == "__main__":
    root = CTk()
    app = AnimeViewer(root)
    root.geometry("800x600")
    root.mainloop()