from customtkinter import CTk

from sub.gui.AnimeViewer import AnimeViewer
from sub.modules.filepath import ensure_files_exist
from sub.modules.rpc import DiscordRPC

if __name__ == "__main__":
    ensure_files_exist()
    print("Checked File Status")
    #DiscordRPC() // comment for production, if not, can cause lags because discord dosnt handle the rpc enough
    print("Loaded RPC")
    root = CTk()
    app = AnimeViewer(root)
    root.geometry("800x600")
    root.mainloop()
