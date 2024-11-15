from PIL import Image

from .utils import PYPACKS_ROOT

def add_icon_to_base(image_path: str, output_path_directory: str) -> None:
    image = Image.open(image_path)
    # Resize image to be 12x12, but don't antialias
    image = image.resize((12, 12), Image.NEAREST)
    # Remove background
    image = image.convert("RGBA")
    # load base
    base = Image.open(f"{PYPACKS_ROOT}/assets/images/icon_base.png")
    # Put image on base, but not the image background (alpha channel)
    base.paste(image, (2, 2), image)
    # Save
    base.save(output_path_directory)
