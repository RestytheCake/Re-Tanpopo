def main():
    from customtkinter import CTk
    from main.gui.AnimeViewer import AnimeViewer
    root = CTk()
    AnimeViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
