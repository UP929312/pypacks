import io
from pathlib import Path

from PIL import Image

from pypacks.utils import IMAGES_PATH

ICON_BASE = Path(IMAGES_PATH)/"reference_book_icons"/"icon_base.png"

SCALE_UP = 1.42
SCALE_DOWN = 0.5


def add_border(image_bytes: bytes, base_image_path: str | Path | None = None) -> bytes:
    # We need to make the item 70% of the total, meaning making the entire image 1.42x bigger
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    if image.width > 256*SCALE_DOWN or image.height > 256*SCALE_DOWN:
        # Scale down the image
        new_width = min(int(image.width*SCALE_DOWN), 256)
        new_height = min(int(image.height*SCALE_DOWN), 256)
        image = image.resize((new_width, new_height))

    # Create a new image that is 1.42x bigger than the original
    new_width = min(int(image.width*SCALE_UP), 256)
    new_height = min(int(image.height*SCALE_UP), 256)
    new_image = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))

    # Load the border image
    border = Image.open(base_image_path or ICON_BASE).convert("RGBA")
    # Scale it up to the full image_size
    border = border.resize((new_image.width, new_image.height), resample=Image.NEAREST)
    # Page the border on (no alpha channel)
    new_image.paste(border, (0, 0), border)

    # Paste the original image in the center
    x, y = (new_image.width - image.width) // 2, (new_image.height - image.height) // 2
    new_image.paste(image, (x, y), image)

    # Save the image to a byte array
    img_byte_arr_io = io.BytesIO()
    new_image.save(img_byte_arr_io, format='PNG')
    img_byte_arr = img_byte_arr_io.getvalue()
    return img_byte_arr
