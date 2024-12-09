import io
from PIL import Image

from pypacks.utils import IMAGES_PATH
from .recipe_image_data import *

ICON_BASE = f"{IMAGES_PATH}/reference_book_icons/icon_base.png"


def add_centered_overlay(
    image_bytes: bytes, base_image_path: str | None = None, resize_to_16x16: bool = True,
) -> bytes:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    # If the image is bigger than 16x16, resize it
    if resize_to_16x16 and (image.width > 16 or image.height > 16):
        image.thumbnail((16, 16))

    # Load base image
    base = Image.open(base_image_path or ICON_BASE).convert("RGBA")

    # Put image on base, but not the image background (alpha channel), and center it
    x, y = (base.width - image.width) // 2, (base.height - image.height) // 2
    base.paste(image, (x, y), image)

    # Save the image to a byte array
    img_byte_arr_io = io.BytesIO()
    base.save(img_byte_arr_io, format='PNG')
    img_byte_arr = img_byte_arr_io.getvalue()
    return img_byte_arr
