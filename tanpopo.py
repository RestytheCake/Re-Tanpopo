from main.modules.rpc import DiscordRPC

Debug = True


def main():
    if Debug:
        run()
    else:
        DiscordRPC()
        print("Loaded RPC")
        run()


def run():
    from customtkinter import CTk
    from main.gui.AnimeViewer import AnimeViewer
    from main.modules.globalmanager import GlobalManager
    from main.modules.path import ensure_files_exist
    ensure_files_exist()
    print("Checked File Status")
    root = CTk()
    AnimeViewer_instance = AnimeViewer(root)
    root.geometry("900x650")
    root.mainloop()


if __name__ == "__main__":
    main()
