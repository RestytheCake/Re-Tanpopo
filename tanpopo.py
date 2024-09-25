import asyncio

# Set event loop policy for Windows compatibility
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def main():
    from customtkinter import CTk
    from main.gui.AnimeViewer import AnimeViewer
    root = CTk()
    AnimeViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
