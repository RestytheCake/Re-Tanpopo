import customtkinter as ctk
import requests
from PIL import Image, UnidentifiedImageError
import asyncio
import aiohttp
from io import BytesIO
import tkinter as tk
from customtkinter import CTkLabel, CTkFrame, CTkFont
from main.gui.details.details import AnimeDetails
from main.modules import loaddata
from main.gui.Hover.Hover import HoverLabel
from main.modules.colors import grey, darkgrey
from main.modules.loaddata import get_anime_data
from main.modules.refresher import change_page_to_detail


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
                return img
        except (aiohttp.ClientError, UnidentifiedImageError) as e:
            print(f"Error loading image from {url}: {e}")
            return None

# Function to replace shimmer label with "Failed loading" label
def handle_image_loading_error(frame, shimmer_label):
    error_label = ctk.CTkLabel(master=frame, text="Failed loading", font=ctk.CTkFont(size=16, weight="bold"), text_color="white", fg_color="black")
    error_label.grid(row=shimmer_label.grid_info()['row'], column=shimmer_label.grid_info()['column'], padx=10, pady=10)
    shimmer_label.destroy()

# Function to update the UI with loaded images
def update_ui_with_images(frame, size, shimmer_labels, watchtype):
    async def load_images():
        anime_data = loaddata.get_anime_data(watchtype=watchtype)  # Retrieve all anime data
        print("DATA")
        print(anime_data)
        anime_id = anime_data["ID"]
        print("Print Anime ID")
        print(anime_id)
        cover_images = anime_data["cover_images"]
        anime_titles = anime_data["titles"]
        anime_descriptions = anime_data["descriptions"]

        for i, (url, shimmer_label) in enumerate(zip(cover_images, shimmer_labels)):
            img = await load_image_async(url, size)
            image = ctk.CTkImage(light_image=img, dark_image=img, size=size)
            if image:  # Check if image loading was successful
                anime_title = anime_titles[i]  # Get the corresponding anime title
                anime_description = anime_descriptions[i]  # Get the corresponding anime description

                double_frame = CTkFrame(frame, fg_color=darkgrey)
                double_frame.grid(row=0, column=i, padx=5, sticky="n")

                # Create a frame for each image and its label
                img_frame = CTkFrame(double_frame, fg_color=darkgrey)
                img_frame.grid(row=0, column=i, padx=10, pady=(10, 0), sticky="n")

                # Create the image label
                img_label = CTkLabel(
                    master=img_frame,
                    text="",
                    fg_color=grey,
                    image=image,
                )
                img_label.image = image  # Keep a reference to avoid garbage collection
                img_label.pack()

                # Truncate the title if it's too long
                max_length = 30
                if len(anime_title) > max_length:
                    truncated_title = anime_title[:max_length - 3] + "..."
                else:
                    truncated_title = anime_title

                # Create the text label for the anime title
                text_label = CTkLabel(
                    master=img_frame,
                    text=truncated_title,
                    font=CTkFont(size=11),
                    text_color="white",
                    wraplength=size[0],  # Ensure text wraps within the width of the image
                    justify="center",
                    pady=5
                )
                text_label.pack()

                # Add click event to open details page
                img_label.bind("<Button-1>", lambda e, t=anime_title, d=anime_description, i=img, ai=anime_id: change_page_to_detail(t, d, i, ai))

                shimmer_label.destroy()  # Remove the shimmer label
                print(f"Image loaded and HoverLabel created for: {anime_title}")
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