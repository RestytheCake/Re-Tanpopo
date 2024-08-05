from main.modules.rpc import DiscordRPC

Debug = True


def main():
    if Debug:
        run()
    else:
        DiscordRPC()
        print("Loaded RPC")
        pip_check()


def pip_check():
    from main.modules.pip import check_and_install_requirements
    from main.modules.path import REQUIREMENTS
    check_and_install_requirements(REQUIREMENTS)
    run()


def run():
    from customtkinter import CTk
    from main.gui.AnimeViewer import AnimeViewer
    from main.modules.globalmanager import GlobalManager
    from main.modules.path import ensure_files_exist
    ensure_files_exist()
    print("Checked File Status")
    root = CTk()
    app = AnimeViewer(root)
    AnimeViewer_instance = AnimeViewer(root)
    GlobalManager.set_animeviewer_instance(AnimeViewer_instance)
    root.geometry("900x650")
    root.mainloop()


if __name__ == "__main__":
    main()
