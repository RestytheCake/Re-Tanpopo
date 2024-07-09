import tkinter as tk
from customtkinter import CTkLabel, CTkToplevel


class HoverLabel(CTkLabel):
    def __init__(self, *args, anime_name="", **kwargs):
        super().__init__(*args, **kwargs)
        self.label = None
        self.frame = None
        self.anime_name = anime_name
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Motion>", self.on_motion)
        self.tooltip = None

    def on_enter(self, event):
        if not self.tooltip:
            self.tooltip = CTkToplevel(self)
            self.tooltip.overrideredirect(True)
            self.tooltip.attributes('-topmost', True)

            # Tooltip frame
            self.frame = tk.Frame(self.tooltip, bg="#212121", padx=10, pady=5)
            self.frame.pack()

            # Tooltip label
            self.label = tk.Label(self.frame, text=self.anime_name, bg="#212121", fg="white", font=("Arial", 12, "bold"))
            self.label.pack()

            # Position the tooltip initially
            self.update_tooltip_position(event)

    def on_motion(self, event):
        if self.tooltip:
            # Update the position of the tooltip to follow the mouse
            self.update_tooltip_position(event)

    def on_leave(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def update_tooltip_position(self, event):
        x = event.x_root + 20
        y = event.y_root + 20
        self.tooltip.geometry(f"+{x}+{y}")

