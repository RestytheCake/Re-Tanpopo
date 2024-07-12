import customtkinter as ctk


def create_category_buttons(self, frame):
    buttons = ["Services", "Library", "Application", "Recognition", "Advanced", "Player", "Version", "Credits", "Clear"]
    for button in buttons:
        btn = ctk.CTkButton(frame, text=button, anchor="w", command=lambda b=button: on_button_click(self, b))
        btn.pack(fill="x", pady=5, padx=7)
        self.buttons.append(btn)


def on_button_click(self, button):
    show_frame(self, button)
    update_button_styles(self, button)


def update_button_styles(self, selected_button):
    for btn in self.buttons:
        if btn.cget("text") == selected_button:
            btn.configure(fg_color="#a9a9d9", hover_color="#8080b0", text_color="white")
        else:
            btn.configure(fg_color=['#3B8ED0', '#1F6AA5'], text_color="white")


def show_frame(self, frame_name):
    for frame in self.frames.values():
        frame.pack_forget()
    frame = self.frames[frame_name]
    frame.pack(fill="both", expand=True)
    update_button_styles(self, frame_name)
