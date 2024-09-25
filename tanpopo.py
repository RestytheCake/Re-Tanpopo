


def main():
    from customtkinter import CTk
    from main.gui.AnimeViewer import AnimeViewer
    from main.modules.path import TANPOPO_DIR
    from main.modules.path import ensure_files_exist
    print(f"±±User data directory: {TANPOPO_DIR}")
    ensure_files_exist()
    root = CTk()
    AnimeViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
