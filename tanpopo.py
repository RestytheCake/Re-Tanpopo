from customtkinter import CTk

from main.gui.AnimeViewer import AnimeViewer
from main.modules.globalmanager import GlobalManager
from main.modules.path import ensure_files_exist
from main.modules.rpc import DiscordRPC

if __name__ == "__main__":
    ensure_files_exist()
    print("Checked File Status")
    # DiscordRPC() // comment for production, if not, can cause lags because discord doesn't handle the rpc enough
    print("Loaded RPC")
    root = CTk()
    app = AnimeViewer(root)
    AnimeViewer_instance = AnimeViewer(root)
    GlobalManager.set_animeviewer_instance(AnimeViewer_instance)
    root.geometry("900x650")
    root.mainloop()
