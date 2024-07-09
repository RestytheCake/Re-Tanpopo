import customtkinter as ctk
import requests
from PIL import Image, UnidentifiedImageError
import asyncio
import aiohttp
from io import BytesIO
import tkinter as tk
from customtkinter import CTkLabel

from sub import loadcovers
from sub.Hover import HoverLabel

grey = "#242424"
darkgrey = "#191919"

def load_file(url, size):
    img = Image.open(url)
    return ctk.CTkImage(img, size=size)


def load_image_old(url, size):
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    return ctk.CTkImage(img, size=size)


# Function to load image from URL and resize it asynchronously
async def load_image_async(url, size):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                img_data = await response.read()
                img = Image.open(BytesIO(img_data))
                img = img.resize(size, Image.LANCZOS)
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except (aiohttp.ClientError, UnidentifiedImageError) as e:
            print(f"Error loading image from {url}: {e}")
            return None


# Function to replace shimmer label with "Failed loading" label
def handle_image_loading_error(frame, shimmer_label):
    error_label = ctk.CTkLabel(master=frame, text="Failed loading", font=ctk.CTkFont(size=16, weight="bold"),
                               text_color="white", fg_color="black")
    error_label.grid(row=shimmer_label.grid_info()['row'], column=shimmer_label.grid_info()['column'], padx=10, pady=10)
    shimmer_label.destroy()


# Function to update the UI with loaded images
def update_ui_with_images(urls, frame, size, shimmer_labels):
    async def load_images():
        anime_names = loadcovers.print_names()  # Retrieve anime names
        for i, (url, shimmer_label) in enumerate(zip(urls, shimmer_labels)):
            img = await load_image_async(url, size)
            if img:  # Check if image loading was successful
                anime_name = anime_names[i]  # Get the corresponding anime name
                img_label = HoverLabel(
                    master=frame,
                    text="",
                    fg_color=grey,
                    image=img,
                    anime_name=anime_name  # Pass the anime name to the HoverLabel
                )
                img_label.image = img  # Keep a reference to avoid garbage collection
                img_label.grid(row=0, column=i, padx=10)
                shimmer_label.destroy()  # Remove the shimmer label
                print(f"Image loaded and HoverLabel created for: {anime_name}")
            else:
                handle_image_loading_error(frame, shimmer_label)

    asyncio.run(load_images())


# Create shimmer effect label
def create_shimmer_label(master, width, height):
    canvas = tk.Canvas(master, width=width, height=height, bg="black", highlightthickness=0)
    shimmer_rect = canvas.create_rectangle(-width, -height, -width + 50, -height + 50, fill="#333333")
    canvas.grid_propagate(False)
    canvas.pack_propagate(False)
    canvas.grid(row=0, column=0, padx=10, pady=10)

    def animate():
        x0, y0, x1, y1 = canvas.coords(shimmer_rect)
        if x1 < width * 2 and y1 < height * 2:
            canvas.move(shimmer_rect, 10, 10)
        else:
            canvas.coords(shimmer_rect, -width, -height, -width + 50, -height + 50)
        master.after(20, animate)  # Faster speed

    animate()
    return canvas