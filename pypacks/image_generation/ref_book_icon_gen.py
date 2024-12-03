import io
# from typing import TYPE_CHECKING

from PIL import Image

# from ..utils import PYPACKS_ROOT, resolve_default_item_image, pascal_to_snake
from .recipe_image_data import *

# if TYPE_CHECKING:
#     from ..resources.custom_item import CustomItem
#     from ..resources.custom_recipe import Recipe

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
    base = Image.open(f"{PYPACKS_ROOT}/assets/images/reference_book_icons/icon_base.png")

    # Put image on base, but not the image background (alpha channel), and center it
    x, y = (base.width - image.width) // 2, (base.height - image.height) // 2
    base.paste(image, (x, y), image)

    # Save the image to a byte array
    img_byte_arr_io = io.BytesIO()
    base.save(img_byte_arr_io, format='PNG')
    img_byte_arr = img_byte_arr_io.getvalue()
    return img_byte_arr

# def generate_recipe_usage_image(recipe: "Recipe") -> None:
#     from .resources.custom_item import CustomItem
#     lower_recipe_type = pascal_to_snake(recipe.__class__.__name__)
#     ingredients, result = recipe.ingredients, recipe.result
#     textures = []
#     for ingredient in ingredients+[result]:
#         if isinstance(ingredient, CustomItem) and ingredient.texture_path:
#             with open(ingredient.texture_path, "rb") as file:
#                 image_bytes = file.read()
#         elif isinstance(ingredient, CustomItem):
#             with open(resolve_default_item_image(ingredient.base_item), "rb") as file:
#                 image_bytes = file.read()
#         else:
#             with open(resolve_default_item_image(ingredient), "rb") as file:
#                 image_bytes = file.read()
#             textures.append(image_bytes)
#     textures, result = textures[:-1], textures[-1]
#     for i, texture in enumerate(textures):
#         pass
#     # textures is now a list of images (in the form of bytes)
