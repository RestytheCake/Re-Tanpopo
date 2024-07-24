from customtkinter import CTk, CTkLabel, CTkFont, CTkFrame, CTkButton
from localStoragePy import localStoragePy
from webbrowser import open as webopen

from sub.gui.Settings.settings import SettingsWindow
from sub.modules import helper
from sub.modules.colors import grey
from sub.modules.globalmanager import GlobalManager
from sub.modules.path import get_project_root


class Top_Frame(CTk):
    def __init__(self, top_frame, **kwargs):
        super().__init__(**kwargs)

        self.top_frame = top_frame
        self.top_frame.grid(row=0, column=0, sticky="ew")
        self.top_frame.columnconfigure(0, weight=1, minsize=325)
        self.top_frame.columnconfigure(1, weight=1, minsize=300)
        self.init()

    def open_settings(self):
        settingswindow_instance = SettingsWindow(self)
        GlobalManager.set_settings_window_instance(settingswindow_instance)

    def button_func(self):
        self.button_frame = CTkFrame(self.top_frame, fg_color=grey)
        self.button_frame.grid(row=0, column=1, pady=15, padx=15, sticky="nes")
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.setting_button = CTkButton(self.button_frame, text="Settings",
                                        image=helper.load_file(f"{get_project_root()}/img/setting.png", (32, 32)),
                                        compound="left",
                                        font=CTkFont(size=32, weight="bold"),
                                        command=self.open_settings)
        self.setting_button.grid(row=0, column=0, pady=5, padx=5, sticky="we")

    def avatar_frame_func(self):
        self.avatar_frame = CTkFrame(self.top_frame, fg_color=grey)
        self.avatar_frame.grid(row=0, column=0, pady=15, padx=15, sticky="nw")
        ls = localStoragePy("Tanpopo Rewrite", "json")

        un = ls.getItem("username")
        if un is None:
            print("Raise Error: Not Logged in or Couldn't Load Avatar Image")
            self.avatar = CTkLabel(self.avatar_frame, 150, 150, 0, "transparent",
                                   image=helper.load_file("img/AniList.png", (125, 125)), text="", )
            self.avatar.grid(row=0, column=0, padx=10)
            self.username_label = CTkLabel(self.avatar_frame, text="Reopen the Window after Settings Login",
                                           fg_color=grey, padx=10,
                                           font=CTkFont(size=16, weight="bold"))
            self.username_label.grid(row=1, column=0, padx=10)
        else:
            self.avatar = CTkLabel(self.avatar_frame, 125, 125, 0,
                                   image=helper.load_image_old(ls.getItem("avatar_url"), (125, 125)), text="", )
            self.avatar.bind("<Button-1>", lambda e: webopen(f"https://anilist.co/user/{un}"))
            self.avatar.grid(row=0, column=0, padx=10)
            self.username_label = CTkLabel(self.avatar_frame, text=f'Hello {ls.getItem("username")}!', fg_color=grey,
                                           font=CTkFont(size=16, weight="bold"))
            self.username_label.grid(row=1, column=0, padx=10)

    def init(self):
        self.clear_frames()
        self.avatar_frame_func()
        self.button_func()

    def clear_frames(self):
        print("Clearing frames...")
        for widget in self.top_frame.winfo_children():
            widget.destroy()
            print(f"Destroyed widget: {widget}")

    def update_settings(self):
        print("Updating settings...")
        self.init()
        print("Reinitialized avatar frame content.")
