import io

from PIL import Image

from .utils import PYPACKS_ROOT

def add_icon_to_base(image_path: str | None = None, image_bytes: bytes | None = None) -> bytes:

    if image_path is not None:
        # Load custom icon
        image = Image.open(image_path).convert("RGBA")
    else:
        assert image_bytes is not None, "Must provide image path or image bytes"
        image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    # If the image is bigger than 16x16, resize it
    if image.width > 16 or image.height > 16:
        image.thumbnail((16, 16))

    # Load base image
    base = Image.open(f"{PYPACKS_ROOT}/assets/images/icon_base.png")

    # Put image on base, but not the image background (alpha channel), and center it
    x, y = (base.width - image.width) // 2, (base.height - image.height) // 2
    base.paste(image, (x, y), image)

    # Save the image to a byte array
    img_byte_arr = io.BytesIO()
    base.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
